import random

from .lexer import *


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.result_desc = ""
        self.current_token = None
        self.next_token = None

        self.ready = False

    def new(self):
        self.result_desc = ""
        self.current_token = self.lexer.get_next_token()
        self.next_token = self.lexer.get_next_token()

        self.ready = True

    def error(self, message):
        raise Exception('Parser error: {}'.format(message))

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token
            self.next_token = self.lexer.get_next_token()
        else:
            self.error("Unexpected token '{}'"
                       .format("None" if self.current_token is None else self.current_token.type))

    def number(self):
        """
        :return: An integer value
        """
        token = self.current_token
        self.eat(token.type)
        return token.value

    def dice(self):
        count = self.current_token.value
        self.eat(TokenType.NUMBER)
        self.eat(TokenType.D)
        value = self.current_token.value
        self.eat(TokenType.NUMBER)

        desc = ""
        result = 0
        for i in range(count):
            dice = random.randint(1, value)
            desc += str(dice) + "+"
            result += dice

        self.result_desc += "{}[{}d{} -> {}]".format(result, count, value, desc[:-1])

        return result

    def factor(self):
        current_token = self.current_token
        next_token = self.next_token

        if next_token.type == TokenType.D:
            return self.dice()

        if current_token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            self.result_desc += str(current_token.value)
            return current_token.value
        elif current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            self.result_desc += "("
            result = self.expr()
            self.result_desc += ")"
            self.eat(TokenType.RPAREN)
            return result
        else:
            self.error("Unexpected token {}".format(current_token))

    def term(self):
        result = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                self.result_desc += " * "
                result *= self.factor()
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
                self.result_desc += " / "
                result //= self.term()
            else:
                self.error("Unexpected token {}".format(token))

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                self.result_desc += " + "
                result += self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                self.result_desc += " - "
                result -= self.term()
            else:
                self.error("Unexpected token {}".format(token))

        return result

    def parse(self):
        if self.ready:
            return self.expr()
        else:
            raise None
