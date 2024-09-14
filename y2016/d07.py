def parse(stream) -> list:
    results = []
    for line in stream:
        line = line.strip()
        results.append(line)
    return results


def supports_tls(ip: str) -> bool:
    abba = False
    brackets = False
    for i, ch in enumerate(ip):
        if ch == '[':
            brackets = True
        elif ch == ']':
            brackets = False
        elif i >= 3:
            if (ip[i] == ip[i - 3] and
                    ip[i - 2] == ip[i - 1] and
                    ip[i - 1] != ip[i]):
                if brackets:
                    return False
                else:
                    abba = True
    return abba


def supports_ssl(ip: str) -> bool:
    abas = set()
    babs = set()
    brackets = False
    for i, ch in enumerate(ip):
        if ch == '[':
            brackets = True
        elif ch == ']':
            brackets = False
        elif i >= 2:
            if (ip[i] == ip[i - 2] and ip[i - 1] != ip[i]):
                chunk = ip[i - 2: i + 1]
                reverse = chunk[1] + chunk[0] + chunk[1]
                if brackets:
                    babs.add(chunk)
                    if reverse in abas:
                        return True
                else:
                    abas.add(chunk)
                    if reverse in babs:
                        return True
    return False


def count_tls_ssl(ips: list) -> tuple:
    tls = 0
    ssl = 0
    for ip in ips:
        if supports_tls(ip):
            tls += 1
        if supports_ssl(ip):
            ssl += 1
    return tls, ssl


def run(stream, test=False, draw=False):
    packets = parse(stream)

    result1, result2 = count_tls_ssl(packets)
    return (result1, result2)
