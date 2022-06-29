import string


def machine_id(client):
    """Test if /etc/machine_id exists and is not initialized"""
    (exit_code, output, error) = client.execute_command(
        "[[ ! -s /etc/machine-id ]] || cat /etc/machine-id", quiet=True)

    machine_id = output.strip(string.whitespace)

    assert exit_code == 0 and ( machine_id == "uninitialized" or
            machine_id == ""), "machine-id doesn't exist or is not empty!"


def machine_id_powered_on(client):
    """Test if /etc/machine_id exists and is initialized"""
    # Validate that systemd unit is started
    systemd_unit = "systemd-machine-id-commit"
    cmd = f"systemctl status {systemd_unit}.service"
    (rc, out, err) = client.execute_command(
        cmd, quiet=True)

    # Validate output lines of systemd-unit
    for line in out.splitlines():
        if "Active:" in line:
            assert not "dead" in line, f"systemd-unit: {systemd_unit} did not start."

    # Validate content of generated output
    # from systemd-machine-id-commit unit
    machine_id_file = "/etc/machine-id"
    cmd = f"cat {machine_id_file}"
    (rc, out, err) = client.execute_command(
        cmd, quiet=True)
    assert not (out == "" or out == "uninitialized"), f"machine-id is uninitialized in {machine_id_file}"
