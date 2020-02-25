#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pprint
from collections import Counter
from typing import Tuple

INPUT_FILE = "input.txt"
WIDE = 25
TALL = 6

pp = pprint.PrettyPrinter(indent=4)

IMAGE_FORMAT = {}


def assemble_image_format():
    image_format = {}
    input = read_input()
    index = 0
    layer = 1
    print(len(input))
    while index < len(input):
        data = []
        for _ in range(TALL):
            data.append(input[index : (index + WIDE)])
            index += WIDE
        image_format.update({f"{layer}": data})
        layer += 1

    return image_format


def read_input() -> str:
    with open(INPUT_FILE, "r") as f_handle:
        inputs = f_handle.readline().rstrip()

    return inputs


def find_correct_layer_with_fewest_zeros(image_format):
    minimum = (float("inf"), -1)
    counter: Counter = Counter()
    for layer, data in image_format.items():
        for pixels in data:
            counter.update(pixels)
        if counter["0"] < minimum[0]:
            minimum = (counter["0"], layer)
        counter.clear()

    return minimum


def do_layer_calculation(layer):
    counter: Counter = Counter()
    for pixels in layer:
        counter.update(pixels)
    print(counter["1"] * counter["2"])


def main():
    image_format = assemble_image_format()
    minimum_layer = find_correct_layer_with_fewest_zeros(image_format)
    do_layer_calculation(image_format[minimum_layer[1]])


if __name__ == "__main__":
    sys.exit(main())
