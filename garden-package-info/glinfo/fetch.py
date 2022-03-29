#!/usr/bin/env python3

import sys
import yaml
import click
import os
import requests
import re
import glinfo.common as glinfo

def get_debian_sectrack_info(package):
    pass



def get_feature_pkg_dict(pkg_include_dict):

    feature_pkg_dict = dict()
    for feature in pkg_include_dict:
        fpath = pkg_include_dict[feature]
        feature_pkg_dict.setdefault(feature, [])
        with open(fpath, 'r') as fp:
            for line in fp:
                if line.startswith('#') or line.isspace():
                    continue
                feature_pkg_dict[feature].append(line.strip())
    return feature_pkg_dict


def get_pkg_include_paths_dict(feature_root):

    pkg_include_dict = dict()
    for feature_dir in os.listdir(feature_root):
        cur_pkg_include_candidate = os.path.join(feature_root, feature_dir, "pkg.include")
        if os.path.isfile(cur_pkg_include_candidate):
            pkg_include_dict[feature_dir] = cur_pkg_include_candidate
    return pkg_include_dict


def gen_dict_from_package_list(packages_list, arch, keyfilter):
    packages_dict = dict()

    if packages_list == None:
        return packages_dict
    for line in packages_list.splitlines():
        if line.startswith("Package: "):
            cur_package_name = line.split("Package: ", 2)[1].strip()
            cur_package_name = cur_package_name.replace("${arch}", arch)
            packages_dict[cur_package_name] = dict()
            packages_dict[cur_package_name]["required-by-feature"] = "None"
        else:
            split = line.split(": ", 2)
            if len(split) < 2:
                continue
            key = split[0].strip()
            if key in keyfilter:
                continue
            value = split[1].strip()

            # Next, write value of this package_dict entry
            write_packages_dict_value(key, value, cur_package_name, packages_dict)

    return packages_dict


def write_packages_dict_value(key, value, package_name, packages_dict):
    """
    Write specific key value combos to the packages_dict.
    Before doing this, process some keys to modify
    the resulting dictionary (e.g convert strings to lists)
    """
    # Modify packages_dict by "Version"
    if "Version" in key:
        if re.search("garden", value, re.IGNORECASE):
            packages_dict[package_name]["Gardenlinux-Package"] = "yes"
        else:
            packages_dict[package_name]["Gardenlinux-Package"] = "no"

    # Modify packages_dict by "Build-Depends"
    elif "Build-Depends" in key:
        value = value.split(", ")

    # Modify packages_dict by "Architecture"
    elif "Architecture" in key:
        value = value.split(" ")

    # Modify packages_dict by "Binary"
    elif "Binary" in key:
        value = value.split(", ")

    # Finally set value
    packages_dict[package_name][key] = value


def merge_package_and_source_list(package_list, source_list, arch):
    """
    Merge package and source list together
    """
    # First, we will create a source package
    # list. This makes the merge much quicker.
    source_pkg_list = dict()
    for source_name, source in source_list.items():
        binaries = source["Binary"]
        for binary in binaries:
            source_pkg_list[binary] = source
            source_pkg_list[binary]["Merged-Source"] = source_name

    # Then, we iterate through all packages from the packages
    # list and merge the source package information together.
    for package_name, package in package_list[arch].items():
        source = source_pkg_list.get(package_name)

        # If we can not find a source package for our package
        # we must skip it here.
        if not source:
            continue

        # Finally, we can not simply merge source and binary package together
        # because we would unintendently overwrite specific values. Therefore,
        # we do it explicitly.
        package["Build-Depends"] = source.get("Build-Depends", []).copy()
        package["Merged-Source"] = source.get("Merged-Source", "")


def download_repo_pkg_file(arch, version):
    """
    Downloads the Package file of a repo.
    """
    url = f"http://repo.gardenlinux.io/gardenlinux/dists/{version}/main/binary-{arch}/Packages"
    return glinfo.download_file(url)


def download_repo_source_file(base_url, version):
    """
    Downloads the Sources file of a repo.
    """
    url = f"{base_url}/dists/{version}/main/source/Sources.gz"
    return glinfo.download_archive_file(url)


@click.command()
@click.option('--feature-folder', default="../features", type=click.Path(exists=True), help='gardenlinux/feature folder containing subfolders with pkg.include files')
@click.option('--output', default="packages.yaml", type=click.Path(exists=False), help='Path to file where package.yaml will be written to')
@click.option('--required-only', is_flag=True,  default=False, help='If flag is set, only packages that are required by a feature will be included on output yaml')
@click.option('--add-sources', is_flag=True,  default=False, help='If flag is set, source information are added to output yaml')
def fetch(feature_folder, output, required_only, add_sources):


    keyfilter = ['MD5sum', 'SHA1', 'SHA256', 'SHA512', 'Description-Md5',
                 'Breaks', 'Depends', 'Homepage', 'Maintainer', 'Tag', 'Built-Using', 'Build-Ids']

    print("### dumping package dicts to yaml")

    packages_dict = dict()
    for arch in glinfo.GLINFO_ARCHICTECTURES:
        packages_dict[arch] = gen_dict_from_package_list(
            download_repo_pkg_file(arch, "dev"),
            arch,
            keyfilter
        )

    print("### Extend package dicts with sources")
    if add_sources:
        list_content = download_repo_source_file("http://deb.debian.org/debian", "bookworm")
        for arch in glinfo.GLINFO_ARCHICTECTURES:
            source_list = gen_dict_from_package_list(
                list_content,
                arch,
                keyfilter
            )
            merge_package_and_source_list(packages_dict, source_list, arch)

    print("### reading features")
    pkg_include_dict = get_pkg_include_paths_dict(feature_folder)
    feature_pkg_dict = get_feature_pkg_dict(pkg_include_dict)

    print("### cross referencing available packages to feature pkg.include")

    for feature in feature_pkg_dict:
        print(f"cross referencing packages from feature: {feature}")
        for pkg in feature_pkg_dict[feature]:
            # print(f"feature: {feature} has package: {pkg}")
                for arch in packages_dict:
                    arch_pkg = pkg.replace('${arch}',arch)
                    print(arch_pkg)
                    if arch_pkg in packages_dict[arch]:
                        packages_dict[arch][arch_pkg]["required-by-feature"] = feature

    if required_only:
        for arch in packages_dict:
            for pkg in list(packages_dict[arch]):
                if packages_dict[arch][pkg]["required-by-feature"] == "None":
                    del packages_dict[arch][pkg]

    print("### Debug: output files")
    with open("../feature_packages.yaml", 'w') as outfile:
        yaml.dump(feature_pkg_dict, outfile)

    with open(output, 'w') as outfile:
        yaml.dump(packages_dict, outfile)

