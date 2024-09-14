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


def count_tls(ips: list) -> int:
    count = 0
    for ip in ips:
        if supports_tls(ip):
            count += 1
    return count


def run(stream, test=False, draw=False):
    packets = parse(stream)

    result1 = count_tls(packets)
    result2 = 0

    return (result1, result2)
