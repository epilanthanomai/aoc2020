#!/usr/bin/env python3


def main():
    with open("data/day13-buses.txt") as bus_file:
        start_time, buses = parse_buses(bus_file)
    active_buses = [bus for bus in buses if bus]
    bus, wait_time = calculate_wait_time(start_time, active_buses)
    print(bus * wait_time)


def parse_buses(bus_lines):
    raw_start_time, bus_line = list(bus_lines)
    start_time = int(raw_start_time)
    raw_buses = bus_line.split(",")
    # I assume the second problem of the day is gonna use those x values...
    buses = [(None if b == "x" else int(b)) for b in raw_buses]
    return start_time, buses


def calculate_wait_time(start_time, buses):
    minutes_since_last_bus = [(start_time % bus, bus) for bus in buses]
    wait_times = [(bus - last, bus) for (last, bus) in minutes_since_last_bus]
    return min(wait_times)


if __name__ == "__main__":
    main()
