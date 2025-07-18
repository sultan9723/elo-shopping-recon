def parse_nmap_results(filepath):
    open_ports = []

    with open(filepath, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "/tcp" in line and "open" in line:
                open_ports.append(line.strip())

    return open_ports


def parse_gobuster_results(filepath):
    valid_paths = []

    with open(filepath, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "Status: 200" in line or "Status: 301" in line or "Status: 302" in line:
                valid_paths.append(line.strip())

    return valid_paths