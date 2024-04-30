#!/usr/bin/env python3

import os
import subprocess
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


INPUT_PATH="/etc/netplan/50-cloud-init.yaml"
OUTPUT_PATH="/etc/netplan/50-cloud-init-derived.yaml"

def setup_ovs():
  try:
    with open(INPUT_PATH, "rt") as stream:
      data = load(stream, Loader=Loader)
  except FileNotFoundError:
    with open(INPUT_PATH + ".old", "rt") as stream:
      data = load(stream, Loader=Loader)


  network = data["network"]
  bonds = network["bonds"]
  bond0 = bonds["bond0"]
  bond0_addresses = bond0.pop("addresses")
  bond0_routes = bond0.pop("routes")

  network["openvswitch"] = {}
  bridges = network.setdefault("bridges", {})
  bridges["br-ex"] = {
    "addresses": bond0_addresses,
    "interfaces": ["bond0"],
    "openvswitch": {},
    "routes": bond0_routes,
    "nameservers": {
        "addresses": ["147.204.9.200", "147.204.9.201"]
      }
    }


  with open(OUTPUT_PATH, "wt") as stream:
    dump(data, stream, Dumper=Dumper)
  os.chmod(OUTPUT_PATH, 0o600)

  try:
    os.replace(INPUT_PATH, INPUT_PATH + ".old")
  except FileNotFoundError:
    pass


def setup_memory():
  RESERVED_MEMORY_MB=32768
  with open('/proc/meminfo') as file:
    for line in file:
        if 'MemTotal' in line:
            mem_total_kb = int(line.split()[1])
            break

  nr_hugepages = ((mem_total_kb // 1024) - RESERVED_MEMORY_MB) // 2
  with open("/etc/kernel/cmdline.d/60-hugepages.cfg", "wt") as stream:
    stream.write(f'CMDLINE_LINUX="$CMDLINE_LINUX hugepages={nr_hugepages}"\n')
  subprocess.run("update-bootloaders", shell=True)


setup_ovs()
setup_memory()