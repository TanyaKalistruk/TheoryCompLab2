import os

key_word_type = 'KeyWordType'
key_word_int = 'KeyWordInt'
key_word_record = 'KeyWordRecord'
key_word_end = 'KeyWordEnd'
sign_equal = 'SignEqual'
sign_colon = 'SignColon'
sign_semicolon = 'SignSemicolon'
id_alpha = 'IdAlpha'
id_alphabet_ab12 = 'IdAlphabetAB12'


class LeksAnaliz:

    def __init__(self, line: int, string: str):
        self.string = string
        self.dict_defines = {key_word_type: 'type',
                             key_word_int: 'int',
                             key_word_record: 'record',
                             key_word_end: 'end',
                             sign_equal: '=',
                             sign_colon: ':',
                             sign_semicolon: ';',
                             id_alpha: 'alpha',
                             id_alphabet_ab12: ['a', 'b', '1', '2']}
        self.line = line
        self.position = -1
        self.start_position = 0

    def get_token(self):
        """Print word/sing/id and define it"""
        self.position += 1
        try:
            symbol = self.string[self.position]
            if symbol == 't':
                self.check_key_word_type()
            elif symbol == 'i':
                self.check_key_word_int()
            elif symbol == 'r':
                self.check_key_word_record()
            elif symbol == 'e':
                self.check_key_word_end()
            elif symbol in ('a', 'b'):
                self.check_ids()
            elif symbol == ';':
                self.write_to_file("<{token}, {type}>".format(token=symbol, type=sign_semicolon))
                self.get_token()
            elif symbol == ':':
                self.write_to_file("<{token}, {type}>".format(token=symbol, type=sign_colon))
                self.get_token()
            elif symbol == '=':
                self.write_to_file("<{token}, {type}>".format(token=symbol, type=sign_equal))
                self.get_token()
            elif symbol == ' ':
                self.get_token()
            else:
                self.error("Unknown symbol {}".format(symbol))
        except:
            pass

    def error(self, error):
        """Write found error"""
        self.write_to_file(
            "Error in line {line}, position {position}, message: {message}".format(line=self.line,
                                                                                   position=self.position,
                                                                                   message=error),
            "", "")

    def check_alpha_id(self, start_position):
        """Checks if it is alpha id"""
        word_to_check = self.dict_defines[id_alpha]
        self.position += 1
        symbol = self.string[self.position]
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                              type=id_alpha))
                self.get_token()
                break
            self.position += 1
            symbol = self.string[self.position]
        else:
            self.error("It is not an id 'alpha'")

    def check_key_word_end(self):
        """Checks if it is a key word end"""
        word_to_check = self.dict_defines[key_word_end]
        start_position = self.position
        self.position += 1
        symbol = self.string[self.position]
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=word_to_check, type=key_word_end))
                self.get_token()
                break
            self.position += 1
            symbol = self.string[self.position]
        else:
            self.error("It is not a key word 'end'")

    def check_key_word_int(self):
        """Checks if it is key word int"""
        word_to_check = self.dict_defines[key_word_int]
        start_position = self.position
        self.position += 1
        symbol = self.string[self.position]
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=word_to_check, type=key_word_int))
                self.get_token()
                break
            self.position += 1
            symbol = self.string[self.position]
        else:
            self.error("It is not a key word 'int'")

    def check_key_word_record(self):
        """Checks if it is a key word record"""
        word_to_check = self.dict_defines[key_word_record]
        start_position = self.position
        self.position += 1
        symbol = self.string[self.position]
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=word_to_check, type=key_word_record))
                self.get_token()
                break
            self.position += 1
            symbol = self.string[self.position]
        else:
            self.error("It is not a key word 'record'")

    def check_ids(self):
        """Check it is id alpha or id in alphabet {a, b, 1, 2}"""
        start_position = self.position
        self.position += 1
        symbol = self.string[self.position]
        if symbol == 'l' and self.string[start_position] == 'a':
            self.check_alpha_id(start_position)
        else:
            while symbol in self.dict_defines[id_alphabet_ab12]:
                self.position += 1
                symbol = self.string[self.position]
            else:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position],
                                                              type=id_alphabet_ab12))
                self.position -= 1
                self.get_token()

    def check_key_word_type(self):
        """Checks if it is type key word"""
        word_to_check = self.dict_defines[key_word_type]
        start_position = self.position
        self.position += 1
        symbol = self.string[self.position]
        while symbol == word_to_check[self.position]:
            if self.position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                              type=key_word_type))
                self.get_token()
                break
            self.position += 1
            symbol = self.string[self.position]
        else:
            self.error("It is not a key word 'type'")

    @staticmethod
    def write_to_file(message, *args):
        """Write messages to a file"""
        with open("output.txt", "a+") as file:
            file.write(message)
            file.write('\n')
            for arg in args:
                file.write(arg)
                file.write('\n')


if __name__ == '__main__':
    line_num = 1
    with open("input.txt", "r") as line_to_read:
        lines = line_to_read.readlines()
    os.remove("output.txt")
    for line in lines:
        line_without_eof = line.split('\n')[0]
        analyzer = LeksAnaliz(line=line_num, string=line_without_eof)
        analyzer.write_to_file("", "Line number %i" % analyzer.line, "The string is:", analyzer.string, "")
        analyzer.get_token()
        line_num += 1
