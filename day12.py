#!/usr/bin/env python3

import sys


def main(ship):
    directions = load_directions("data/day12-navigation.txt")
    ship.follow_directions(directions)
    print(abs(ship.x) + abs(ship.y))


def load_directions(file_name):
    with open(file_name) as direction_file:
        return [parse_direction(line.strip()) for line in direction_file]


def parse_direction(direction):
    return direction[0], int(direction[1:])


RIGHT_TURNS = {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N",
}
LEFT_TURNS = {
    "N": "W",
    "W": "S",
    "S": "E",
    "E": "N",
}


class DirectShip:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.heading = "E"

    def follow_directions(self, ds):
        for d, distance in ds:
            self.follow_direction(d, distance)

    def follow_direction(self, d, distance):
        move = getattr(self, "move_" + d)
        move(distance)

    def move_N(self, distance):
        self.y += distance

    def move_E(self, distance):
        self.x += distance

    def move_S(self, distance):
        self.y -= distance

    def move_W(self, distance):
        self.x -= distance

    def move_R(self, angle):
        for _ in range(angle // 90):
            self.heading = RIGHT_TURNS[self.heading]

    def move_L(self, angle):
        for _ in range(angle // 90):
            self.heading = LEFT_TURNS[self.heading]

    def move_F(self, distance):
        self.follow_direction(self.heading, distance)


class WaypointShip:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.waypoint_x = 10
        self.waypoint_y = -1

    def follow_directions(self, ds):
        for d, distance in ds:
            self.follow_direction(d, distance)

    def follow_direction(self, d, distance):
        move = getattr(self, "move_" + d)
        move(distance)

    def move_N(self, distance):
        self.waypoint_y -= distance

    def move_E(self, distance):
        self.waypoint_x += distance

    def move_S(self, distance):
        self.waypoint_y += distance

    def move_W(self, distance):
        self.waypoint_x -= distance

    def move_R(self, angle):
        for _ in range(angle // 90):
            old_waypoint_x = self.waypoint_x
            old_waypoint_y = self.waypoint_y
            self.waypoint_x = -old_waypoint_y
            self.waypoint_y = old_waypoint_x

    def move_L(self, angle):
        for _ in range(angle // 90):
            old_waypoint_x = self.waypoint_x
            old_waypoint_y = self.waypoint_y
            self.waypoint_x = old_waypoint_y
            self.waypoint_y = -old_waypoint_x

    def move_F(self, distance):
        self.x += self.waypoint_x * distance
        self.y += self.waypoint_y * distance


if __name__ == "__main__":
    Ship = {
        "direct": DirectShip,
        "waypoint": WaypointShip,
    }[sys.argv[1]]
    main(Ship())
