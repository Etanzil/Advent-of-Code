disk = []

def part1():
    lPtr = 0
    rPtr = len(disk) - 1

    while lPtr < rPtr:
        if disk[lPtr] != ".":
            lPtr += 1
            continue
        if disk[rPtr] == ".":
            rPtr -= 1
            continue

        # Swap file block to fill the gap
        disk[lPtr], disk[rPtr] = disk[rPtr], disk[lPtr]
        lPtr += 1
        rPtr -= 1

    # Calculate the checksum after compaction
    checksum = 0
    for i in range(len(disk)):
        if disk[i] != ".":
            checksum += int(disk[i]) * i
    return checksum


def part2():
    lPtr = 0
    rPtr = len(disk) - 1
    while rPtr > 0:
        # Find the next file block and its length
        if disk[rPtr] == ".":
            rPtr -= 1
            continue
        else:
            seqNum = 1
            number = disk[rPtr]
            while rPtr - seqNum >= 0 and disk[rPtr - seqNum] == number:
                seqNum += 1

        # Find a large enough cluster of free spaces
        placeFound = False
        while not placeFound:
            while lPtr < rPtr and disk[lPtr] != ".":
                lPtr += 1
            seqDot = 1
            while lPtr + seqDot < rPtr and disk[lPtr + seqDot] == ".":
                seqDot += 1
            if seqDot >= seqNum:
                placeFound = True
            else:
                if lPtr + seqDot >= rPtr:
                    break
                else:
                    lPtr += seqDot

        # Swap if a cluster of free spaces was found
        if placeFound:
            disk[lPtr:lPtr + seqNum], disk[rPtr - seqNum + 1:rPtr + 1] = (
                disk[rPtr - seqNum + 1:rPtr + 1],
                disk[lPtr:lPtr + seqNum],
            )
            rPtr -= seqNum
            lPtr = 0
        else:
            rPtr -= 1

    # Calculate the checksum after full compaction
    checksum = 0
    for i in range(len(disk)):
        if disk[i] != ".":
            checksum += int(disk[i]) * i
    return checksum


if __name__ == "__main__":
    with open("day9.txt", "r") as file:
        data = [int(char) for char in file.readline()]

    for i in range(len(data)):
        if i % 2 == 1:
            disk.extend(["."] * int(data[i]))
        else:
            disk.extend([str(i // 2)] * int(data[i]))

    # Solve Part 1
    part1_result = part1()
    print(f"Part 1 Checksum: {part1_result}")

    # Reinitialize the disk for Part 2
    disk = []
    for i in range(len(data)):
        if i % 2 == 1:
            disk.extend(["."] * int(data[i]))
        else:
            disk.extend([str(i // 2)] * int(data[i]))

    # Solve Part 2
    part2_result = part2()
    print(f"Part 2 Checksum: {part2_result}")
