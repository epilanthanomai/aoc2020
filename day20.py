#!/usr/bin/env python3

import operator
import re
from collections import defaultdict
from functools import reduce


DIMENSION = 12


def main():
    tiles = load_tiles("data/day20-tiles.txt")
    layout = lay_out_tiles(tiles)
    print(product(get_corner_ids(layout)))


def load_tiles(file_name):
    with open(file_name) as tile_file:
        tile_data = tile_file.read()
    tile_strings = tile_data.strip().split("\n\n")
    return dict(parse_tile(tile_string) for tile_string in tile_strings)


def get_corner_ids(layout):
    return (
        layout[0][0][0],
        layout[0][-1][0],
        layout[-1][0][0],
        layout[-1][-1][0],
    )


def product(values):
    return reduce(operator.mul, values, 1)


TILE_TITLE_RE = re.compile("Tile (\d+):")


def parse_tile(tile_string):
    lines = tile_string.splitlines()
    title_line, tile_lines = lines[0], lines[1:]
    title_match = TILE_TITLE_RE.match(title_line)
    tile_number = int(title_match.group(1))
    return tile_number, tile_lines


def lay_out_tiles(tiles):
    tile_sides = {
        tile_id: collect_tile_sides(lines) for (tile_id, lines) in tiles.items()
    }
    index = index_sides(tile_sides)
    tile_ids = set(tiles.keys())
    start_tile = tile_ids.pop()
    start_row_matches = extend_row_from_tile(start_tile, tile_ids, tile_sides, index)
    assert len(start_row_matches) == 1
    start_row, tile_ids = list(start_row_matches)[0]
    result_matches = extend_layout_from_row(start_row, tile_ids, tile_sides, index)
    assert len(start_row_matches) == 1
    result = list(result_matches)[0]
    return result


def collect_tile_sides(tile):
    # clockwise
    top = tile[0]
    right = "".join(row[-1] for row in tile)
    bottom = "".join(reversed(tile[-1]))
    left = "".join(row[0] for row in reversed(tile))

    return (top, right, bottom, left)


def reverse_side(side):
    return "".join(reversed(side))


def opposite_direction(direction):
    return (direction + 2) % 4


def index_sides(sides):
    index = defaultdict(set)
    for tile_id, tile_sides in sides.items():
        for side_number, side in enumerate(tile_sides):
            reversed_side = reverse_side(side)
            index[side].add((tile_id, False, side_number))
            index[reversed_side].add((tile_id, True, -side_number))
    return index


def extend_row_from_tile(start_tile_id, remaining_tile_ids, tile_sides, index):
    partial_matches = [([(start_tile_id, False, 0)], remaining_tile_ids)]
    result = []
    while partial_matches:
        (current_match, available_tile_ids), partial_matches = (
            partial_matches[0],
            partial_matches[1:],
        )

        # options to the right
        right_id, right_flipped, right_orientation = current_match[-1]
        for candidate in tile_extensions_in_direction(
            right_id,
            right_flipped,
            right_orientation,
            1,  # right
            tile_sides,
            index,
            available_tile_ids,
        ):
            candidate_id, _, _ = candidate
            next_partial_match = current_match + [candidate]
            next_tile_ids = available_tile_ids.difference([candidate_id])
            if len(next_partial_match) == DIMENSION:
                result.append((tuple(next_partial_match), frozenset(next_tile_ids)))
            else:
                partial_matches.append((next_partial_match, next_tile_ids))

        # options to the left
        left_id, left_flipped, left_orientation = current_match[0]
        for candidate in tile_extensions_in_direction(
            left_id,
            left_flipped,
            left_orientation,
            3,  # left
            tile_sides,
            index,
            available_tile_ids,
        ):
            candidate_id, _, _ = candidate
            next_partial_match = [candidate] + current_match
            next_tile_ids = available_tile_ids.difference([candidate_id])
            if len(next_partial_match) == DIMENSION:
                result.append((tuple(next_partial_match), frozenset(next_tile_ids)))
            else:
                partial_matches.append((next_partial_match, next_tile_ids))

    return set(result)


def extend_layout_from_row(start_row, tile_ids, tile_sides, index):
    partial_matches = [([start_row], tile_ids)]
    result = []
    while partial_matches:
        (current_match, available_tile_ids), partial_matches = (
            partial_matches[0],
            partial_matches[1:],
        )

        # options above
        for candidate in row_extensions_in_direction(
            current_match[0],
            0,  # up
            tile_sides,
            index,
            available_tile_ids,
        ):
            row_tile_ids = [tile_id for (tile_id, flip, orientation) in candidate]
            next_partial_match = [candidate] + current_match
            next_tile_ids = available_tile_ids.difference(row_tile_ids)
            if len(next_partial_match) == DIMENSION:
                result.append(tuple(next_partial_match))
            else:
                partial_matches.append((next_partial_match, next_tile_ids))

        # options beloww
        for candidate in row_extensions_in_direction(
            current_match[-1],
            2,  # down
            tile_sides,
            index,
            available_tile_ids,
        ):
            row_tile_ids = [tile_id for (tile_id, flip, orientation) in candidate]
            next_partial_match = current_match + [candidate]
            next_tile_ids = available_tile_ids.difference(row_tile_ids)
            if len(next_partial_match) == DIMENSION:
                result.append(tuple(next_partial_match))
            else:
                partial_matches.append((next_partial_match, next_tile_ids))

    return set(result)


def tile_extensions_in_direction(
    tile_id, flipped, orientation, direction, sides, index, available_ids
):
    side = get_tile_side(sides[tile_id], flipped, orientation, direction)
    candidates = find_tiles_with_constraint(
        reverse_side(side), opposite_direction(direction), index
    )
    return [
        (candidate_id, candidate_flipped, candidate_orientation)
        for (candidate_id, candidate_flipped, candidate_orientation) in candidates
        if candidate_id in available_ids
    ]


def row_extensions_in_direction(row, direction, sides, index, available_ids):
    start_id, start_flipped, start_orientation = row[0]
    start_side = get_tile_side(
        sides[start_id], start_flipped, start_orientation, direction
    )
    start_tile_candidates = find_tiles_with_constraint(
        reverse_side(start_side), opposite_direction(direction), index
    )
    partial_matches = [
        (
            [(candidate_id, candidate_flipped, candidate_orientation)],
            available_ids.difference([candidate_id]),
        )
        for (
            candidate_id,
            candidate_flipped,
            candidate_orientation,
        ) in start_tile_candidates
        if candidate_id in available_ids
    ]

    result = []
    while partial_matches:
        (match, match_available_ids), partial_matches = (
            partial_matches[0],
            partial_matches[1:],
        )
        right_id, right_flipped, right_orientation = match[-1]
        right_side = get_tile_side(sides[right_id], right_flipped, right_orientation, 1)

        parallel_id, parallel_flipped, parallel_orientation = row[len(match)]
        parallel_side = get_tile_side(
            sides[parallel_id], parallel_flipped, parallel_orientation, direction
        )

        for candidate in find_tiles_with_constraints(
            [
                (reverse_side(right_side), 3, index),
                (reverse_side(parallel_side), opposite_direction(direction), index),
            ]
        ):
            candidate_id, _, _ = candidate
            next_available_ids = match_available_ids.difference([candidate_id])
            next_match = match + [candidate]
            if len(next_match) == DIMENSION:
                result.append(tuple(next_match))
            else:
                partial_matches.append((next_match, next_available_ids))

    return result


def get_tile_side(tile_sides, flipped, orientation, direction):
    side_number = orientation + direction
    if flipped:
        side_number = -side_number
    side_number = side_number % 4
    side = tile_sides[side_number]
    return reverse_side(side) if flipped else side


def find_tiles_with_constraints(constraints):
    matches = [
        set(find_tiles_with_constraint(*constraint)) for constraint in constraints
    ]
    return set.intersection(*matches) if matches else set()


def find_tiles_with_constraint(side, direction, index):
    matches = index[side]
    return [
        (tile_id, flipped, ((side - direction) if flipped else (side - direction)) % 4)
        for (tile_id, flipped, side) in matches
    ]


if __name__ == "__main__":
    main()
