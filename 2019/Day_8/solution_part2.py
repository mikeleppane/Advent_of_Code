#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import sys
from typing import Dict, List

INPUT_FILE = "input.txt"
WIDE = 25
TALL = 6

pp = pprint.PrettyPrinter(indent=4)
IMAGE_FORMAT_TYPE = Dict[str, List[str]]

IMAGE_FORMAT: IMAGE_FORMAT_TYPE = {}
BLACK, WHITE, TRANSPARENT = (0, 1, 2)


def assemble_image_format() -> IMAGE_FORMAT_TYPE:
    image_format = {}
    _input = read_input()
    index = 0
    layer = 1
    while index < len(_input):
        data = []
        for _ in range(TALL):
            data.append(_input[index : (index + WIDE)])
            index += WIDE
        image_format.update({f"{layer}": data})
        layer += 1

    return image_format


def read_input() -> str:
    with open(INPUT_FILE, "r") as f_handle:
        inputs = f_handle.readline().rstrip()

    return inputs


def get_decoded_image(image_format: IMAGE_FORMAT_TYPE) -> List[int]:
    decoded_image = []
    for index in range(WIDE * TALL):
        layer_number = index + 1
        if layer_number > len(image_format):
            layer_number = len(image_format)
        pixel_at_position = define_visible_pixel_in_layer(
            image_format, index, str(layer_number)
        )
        decoded_image.append(pixel_at_position)

    return decoded_image


def define_visible_pixel_in_layer(
    image_format: IMAGE_FORMAT_TYPE, position: int, layer_number: str
) -> int:
    pixel_at_position = int("".join(image_format[layer_number])[position])
    for layer, data in image_format.items():
        is_ok_to_exit = layer == layer_number and pixel_at_position != TRANSPARENT
        if is_ok_to_exit:
            break
        pixel = int("".join(data)[position])
        if pixel != TRANSPARENT:
            pixel_at_position = pixel
            break
    return pixel_at_position


def show_decoded_image(decoded_image: List[int]) -> None:
    print(int("".join(str(x) for x in decoded_image)))
    index = 0
    for _ in range(TALL):
        for number in decoded_image[index : (index + WIDE)]:
            if number == 0:
                sys.stdout.write("  ")
            else:
                sys.stdout.write("\u2591\u2591")
        sys.stdout.write("\n")
        index += WIDE


def main():
    image_format = assemble_image_format()
    decoded_image = get_decoded_image(image_format)
    show_decoded_image(decoded_image)


if __name__ == "__main__":
    sys.exit(main())
