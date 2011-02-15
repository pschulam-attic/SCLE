from sys import argv

def clean(filename):
    out_file = filename[:-6] + "clean"
    input = open(filename, 'r')
    output = open(out_file, 'w')
    for line in input:
        if line.startswith("(TOP~"):
            output.write(line)
    input.close()
    output.close()
    return out_file

def main():
    if len(argv) != 2:
        print "Must pass .model* file to clean"
    else:
        clean(argv[1])

if __name__ == "__main__":
    main()
