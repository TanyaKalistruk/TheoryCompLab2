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
        self.is_position_after_record = False

    def get_token(self):
        """Returns first unread symbol, change position number to +1"""
        self.position += 1
        try:
            symbol = self.string[self.position]
        except:
            symbol = None
        return symbol

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
        symbol = self.get_token()
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                              type=id_alpha))
                break
            symbol = self.get_token()
        else:
            self.error("It is not an id 'alpha'")

    def check_key_word_end(self):
        """Checks if it is a key word end"""
        word_to_check = self.dict_defines[key_word_end]
        start_position = self.position
        symbol = self.get_token()
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                              type=key_word_end))
                self.is_position_after_record = False
                self.check_semicolon()
                break
            symbol = self.get_token()
        else:
            self.error("It is not a key word 'end'")

    def check_semicolon(self):
        """Checks is it ; or the end of line"""
        if self.position == len(self.string) - 1:
            if self.is_position_after_record:
                self.error("There should be a key word 'end'")
            else:
                self.write_to_file("", "")
        else:
            symbol = self.get_token()
            if symbol == ' ':
                self.check_semicolon()
            else:
                if symbol == ';':
                    self.write_to_file("<{token}, {type}>".format(token=self.string[self.position:self.position + 1],
                                                                  type=sign_semicolon))
                    self.check_iden()
                elif self.is_position_after_record:
                    self.check_key_word_end()
                else:
                    self.error("There should be a sing ';' or it should the end of line")

    def check_key_word_int(self):
        """Checks if it is key word int"""
        word_to_check = self.dict_defines[key_word_int]
        start_position = self.position
        symbol = self.get_token()
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                              type=key_word_int))
                self.check_semicolon()
                break
            symbol = self.get_token()
        else:
            self.error("It is not a key word 'int'")

    def check_key_word_record(self):
        """Checks if it is a key word record"""
        word_to_check = self.dict_defines[key_word_record]
        start_position = self.position
        symbol = self.get_token()
        while symbol == word_to_check[self.position - start_position]:
            if self.position - start_position == len(word_to_check) - 1:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                              type=key_word_record))
                self.check_iden()
                break
            symbol = self.get_token()
        else:
            self.error("It is not a key word 'record'")

    def check_vyr(self):
        """Checks VYR rules"""
        symbol = self.get_token()
        if symbol == ' ':
            self.check_vyr()
        elif symbol == 'i':
            self.check_key_word_int()
        elif symbol == 'r':
            self.is_position_after_record = True
            self.check_key_word_record()

    def check_sing(self, symbol, sign, type_sign):
        """Check if symbol is as passed sing"""
        if symbol == sign:
            self.write_to_file("<{token}, {type}>".format(token=self.string[self.position:self.position + 1],
                                                          type=type_sign))
            self.check_vyr()
        else:
            self.error("There should be an '{sign}' sing".format(sign=sign))

    def check_sign_equal_or_colon(self):
        """Check if it is sign an = or :"""
        symbol = self.get_token()
        if symbol == ' ':
            self.check_sign_equal_or_colon()
        else:
            if not self.is_position_after_record:
                self.check_sing(symbol=symbol, sign='=', type_sign=sign_equal)
            else:
                self.check_sing(symbol=symbol, sign=':', type_sign=sign_colon)

    def check_ids(self):
        """Check it is id alpha or id in alphabet {a, b, 1, 2}"""
        start_position = self.position
        symbol = self.get_token()
        if symbol == 'l' and self.string[start_position] == 'a':
            self.check_alpha_id(start_position)
        else:
            while symbol in self.dict_defines[id_alphabet_ab12]:
                symbol = self.get_token()
            else:
                self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                              type=id_alphabet_ab12))
        self.check_sign_equal_or_colon()

    def check_iden(self):
        """Checks if it is an id"""
        symbol = self.get_token()
        if symbol == ' ':
            self.check_iden()
        else:
            if symbol in ('a', 'b'):
                self.check_ids()
            else:
                self.error("Unknown symbols")

    def check_key_word_type(self):
        """Checks if it is type key word"""
        word_to_check = self.dict_defines[key_word_type]
        start_position = self.position
        symbol = self.get_token()
        while symbol == word_to_check[self.position]:
            if self.position == len(word_to_check) - 1:
                if start_position == 0:
                    self.write_to_file("<{token}, {type}>".format(token=self.string[start_position:self.position + 1],
                                                                  type=key_word_type))
                    self.check_iden()
                else:
                    self.error("The key word 'type' should be on the beginning of string")
                break
            symbol = self.get_token()
        else:
            self.error("It is not a key word 'type'")

    def analyze_string(self):
        """Analyze beginning of string"""
        self.write_to_file("Line number %i" % self.line, "The string is:", self.string, "")
        symbol = self.get_token()
        if symbol == 't':
            self.check_key_word_type()
        else:
            self.error("The key word 'type' should be on the beginning of string")

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
        analyzer.analyze_string()
        line_num += 1
