import os

meaning = ("KeyWordCancel", "KeyWordCall", "FourSingNumber123")

matrix = (
     (1, 4, 0, 0, 0, 0, -4),
     (2, 4, 0, 0, 0, 0, -4),
     (3, 4, 0, 0, 0, 0, -4),
     (-1, 4, 0, 0, 0, 0, -4),
     (1, 4, 5, 0, 0, 0, -4),
     (1, 4, 0, 6, 7, 0, -4),
     (1, 4, 0, -2, 0, 0, -4),
     (1, 8, 0, 0, 0, 0, -4),
     (1, 4, 5, 0, 0, 9, -4),
     (1, 4, 0, -3, 0, 0, -4)
)


def classify_symbol(symbol: str) -> int:
    """Return the class of passed symbol"""
    if symbol in ('1', '2', '3'):
        return 0
    elif symbol == 'c':
        return 1
    elif symbol == 'a':
        return 2
    elif symbol == 'l':
        return 3
    elif symbol == 'n':
        return 4
    elif symbol == 'e':
        return 5
    else:
        return 6


def write_to_file(message, *args):
    """Write messages to a file"""
    with open("output.txt", "a+") as file:
        file.write(message)
        file.write('\n')
        for arg in args:
            file.write(arg)
            file.write('\n')


def analyze(string: str):
    """Analyze string from file"""
    st = 0
    i = 0
    begin = i
    while i < len(string):
        symbol = string[i]
        cl = classify_symbol(symbol)
        st = matrix[st][cl]
        if st == 1 or st == 4 or st == 0:
            begin = i
        if st == 5:
            begin = i - 1
        i += 1
        if st == -1 or st == -2 or st == -3:
            to_write = string[begin:i]
            write_to_file("<{token}, {type}>".format(token=meaning[st], type=to_write))
            st = 0
            begin = i
        elif st == -4:
            st = 0
            begin = i


if __name__ == '__main__':
    line_num = 1
    with open("input.txt", "r") as line_to_read:
        lines = line_to_read.readlines()
    os.remove("output.txt")
    for line in lines:
        line_without_eof = line.split('\n')[0]
        write_to_file("", "Line number %i" % line_num, "The string is:", line_without_eof)
        analyze(line_without_eof)
        line_num += 1
