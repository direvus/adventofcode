def run(stream, test=False):
    result1 = 0
    result2 = 0
    for line in stream:
        width, height, length = [int(x) for x in line.strip().split('x')]
        volume = width * height * length
        areas = (width * height, width * length, height * length)
        perimeters = (
                2 * width + 2 * height,
                2 * width + 2 * length,
                2 * height + 2 * length)
        min_area = min(areas)
        result1 += sum([2 * area for area in areas]) + min_area
        result2 += min(perimeters) + volume
    return (result1, result2)
