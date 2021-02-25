#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum

import sys
from typing import NamedTuple, Dict, List, Union

INPUT_FILE = "input.txt"
BOOT_UP_CYCLES = 6


class State(Enum):
    ACTIVE = "#"
    INACTIVE = "."


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int


@dataclass
class PocketDimension:
    cubes: Dict[Coordinate, State]


def read_expressions() -> List[str]:
    expressions = []
    with open(INPUT_FILE, "r") as f_handle:
        for row, line in enumerate(f_handle):
            line = line.rstrip()
            if line:
                expressions.append(line)

    return expressions


INTEGER, PLUS, MINUS, MUL, LPAREN, RPAREN, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "MUL",
    "(",
    ")",
    "EOF",
)


@dataclass
class Token:
    type: str
    value: Union[str, int]


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self) -> None:
        raise Exception("Invalid character")

    def advance(self) -> None:
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            self.error()

        return Token(EOF, None)


class Interpreter:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()

        while self.current_token.type == PLUS:
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.factor()
        return result

    def expr(self):
        """Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        result = self.term()

        while self.current_token.type in (MINUS, MUL):
            token = self.current_token
            """
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            """
            if token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            elif token.type == MUL:
                self.eat(MUL)
                result = result * self.term()

        return result


def main():
    expressions = read_expressions()
    total = 0
    for expression in expressions:
        lexer = Lexer(expression)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        total += result
    print(total)


if __name__ == "__main__":
    sys.exit(main())
