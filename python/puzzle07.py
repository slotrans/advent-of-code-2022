
def file_set_from_terminal_log(input_string):
    log_lines = input_string.strip().split("\n")

    files = set()
    current_directory = tuple()
    for line in log_lines:
        if line == "$ cd ..":
            current_directory = current_directory[:-1]
        elif line.startswith("$ cd"):
            new_directory_name = line[5:]
            current_directory = (*current_directory, new_directory_name)
            files.add(current_directory)
        elif line == "$ ls":
            # this is actually a no-op
            continue
        elif line.startswith("dir"):
            subdir_name = line.split(" ")[1]
            files.add((*current_directory, subdir_name))
        elif line[0].isdigit():
            size, name = line.split(" ")
            files.add((*current_directory, f"{name}:{size}"))

    return files


def directory_sizes_from_file_set(file_set):
    sizes = {}
    for file_tuple in list(file_set):
        if ":" in file_tuple[-1]:
            name, size = file_tuple[-1].split(":")
            size = int(size)

            dir_depth = len(file_tuple[:-1])
            for i in range(dir_depth):
                negative_index = -1 * (1+i)
                dir_tuple = file_tuple[:negative_index]
                sizes[dir_tuple] = sizes.get(dir_tuple, 0) + size

    return sizes


if __name__ == "__main__":
    input07 = open("../input/input07").read()

    file_set = file_set_from_terminal_log(input07)
    dir_sizes = directory_sizes_from_file_set(file_set)
    p1_answer = sum([size for size in dir_sizes.values() if size <= 100000])
    print(f"(p1 answer) total size of dirs that are each at most 100000 in size: {p1_answer}") # 


#######################################

SAMPLE_INPUT = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

def test_file_set_from_terminal_log():
    expected = set([
        ("/",),
        ("/", "a"),
        ("/", "a", "e"),
        ("/", "a", "e", "i:584"),
        ("/", "a", "f:29116"),
        ("/", "a", "g:2557"),
        ("/", "a", "h.lst:62596"),
        ("/", "b.txt:14848514"),
        ("/", "c.dat:8504156"),
        ("/", "d"),
        ("/", "d", "j:4060174"),
        ("/", "d", "d.log:8033020"),
        ("/", "d", "d.ext:5626152"),
        ("/", "d", "k:7214296"),
    ])
    actual = file_set_from_terminal_log(SAMPLE_INPUT)
    print(actual)
    assert expected == actual


def test_directory_sizes_from_file_set():
    expected = {
        ("/",): 48381165,
        ("/", "a"): 94853,
        ("/", "a", "e"): 584,
        ("/", "d"): 24933642,        
    }
    actual = directory_sizes_from_file_set(file_set_from_terminal_log(SAMPLE_INPUT))
    print(actual)
    assert expected == actual
