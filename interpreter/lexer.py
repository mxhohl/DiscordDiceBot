from enum import Enum


class TokenType(Enum):
    """
    Define all the token types
    """
    EOF = 0
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    D = 6
    LPAREN = 7
    RPAREN = 8


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __str__(self):
        string = 'Token({}'.format(self.type)
        if self.value is not None:
            string += ', {})'.format(self.value)
        else:
            string += ')'

        return string

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self):
        self.text = None
        self.pos = -1
        self.current_char = None

        self.ready = False

    def new(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

        self.ready = True

    def error(self, message):
        raise Exception('Lexer error: {}'.format(message))

    def advance(self):
        self.pos += 1
        if self.pos > (len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def read_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.read_number())
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS)
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE)
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY)
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)
            if self.current_char == 'd' or self.current_char == 'D':
                self.advance()
                return Token(TokenType.D)

            self.error("unexpected char '{}'".format(self.current_char))
        return Token(TokenType.EOF)

    def get_all_token(self):
        token_list = [self.get_next_token()]
        while token_list[-1] != Token(TokenType.EOF):
            token_list.append(self.get_next_token())
        return token_list
