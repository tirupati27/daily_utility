import sys

def compare_files(file1, file2):
    # Read both files and remove trailing newlines
    with open(file1) as f1:
        lines1 = set(line.split("==")[0].strip() for line in f1)

    with open(file2) as f2:
        lines2 = set(line.split("==")[0].strip() for line in f2)

    # Find common and different lines
    common = lines1.intersection(lines2)
    only_in_file1 = lines1 - lines2
    only_in_file2 = lines2 - lines1

    # Print results
    print("\n✅ Common Lines:")
    for line in common:
        print(line)

    print("\n🚫 Lines only in", file1 + ":")
    print()
    for line in only_in_file1:
        print(line)

    print("\n🚫 Lines only in", file2 + ":")
    print()
    for line in only_in_file2:
        print(line)


# Example usage
if __name__ == "__main__":
    if len(sys.argv) == 3:
        f1, f2 = sys.argv[1], sys.argv[2]
    else:
        f1 = input("Enter first file path: ").strip()
        f2 = input("Enter second file path: ").strip()
    compare_files(f1, f2)
