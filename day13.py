#!/usr/bin/env python3

import sys


def main(problem):
    with open("data/day13-buses.txt") as bus_file:
        start_time, buses = parse_buses(bus_file)
    print(problem(start_time, buses))


def parse_buses(bus_lines):
    raw_start_time, bus_line = list(bus_lines)
    start_time = int(raw_start_time)
    raw_buses = bus_line.split(",")
    # I assume the second problem of the day is gonna use those x values...
    buses = [(None if b == "x" else int(b)) for b in raw_buses]
    return start_time, buses


def get_wait_product(start_time, buses):
    active_buses = [bus for bus in buses if bus]
    bus, wait_time = calculate_wait_time(start_time, active_buses)
    return bus * wait_time


def calculate_wait_time(start_time, buses):
    minutes_since_last_bus = [(start_time % bus, bus) for bus in buses]
    wait_times = [(bus - last, bus) for (last, bus) in minutes_since_last_bus]
    return min(wait_times)


def get_sequence_start_time(_, buses):
    sequence_times = [
        (sequence_time, bus) for (sequence_time, bus) in enumerate(buses) if bus
    ]
    # Let's say a particular bus comes to the station every 19 minutes. If its sequence_time is 6, that means 6 minutes
    # after our result time it'll return to the station, or in other words, (t + 6) % 19 == 0. So at time t:
    #   t % 19 = 19 - 6 = 13
    # The extra % bus at the end of the expression is a little ugly: It's to deal with the case where sequence_time == 0
    # for our first bus. For that bus, (bus - sequence_time) is just bus, but we want to force it to 0.
    offset_period_pairs = [
        ((bus - sequence_time) % bus, bus) for (sequence_time, bus) in sequence_times
    ]
    offset, period = total_offset_period(offset_period_pairs)
    return offset


def total_offset_period(offset_period_pairs):
    # We're going to calculate this progressively, starting with a base case and then adding each factor in until we
    # have an answer. Initially every time is divisible by all our buses because we have no buses. The pattern repeats
    # with period 1 starting at time t.
    total_offset = 0
    total_period = 1

    while offset_period_pairs:
        # Pull one (offset, period) pair off the list and mix it into our calculation
        (this_offset, this_period), offset_period_pairs = (
            offset_period_pairs[0],
            offset_period_pairs[1:],
        )

        # Loop through numbers matching the "total" pattern from past iterations. If our total period is p and our
        # total offset is o, then for all i, p * i + o satisfies our calculated total constraints. We can trivially
        # calculate this for the initial condition where p=1, i=0: That's equivalent to for all i, 1 * i + 0, which is
        # all i.
        #
        # Our goal here is to calculate a new (offset, period) that will satisfy existing constrains as well as the new
        # one:
        #   total_offset % this_period = this_offset
        # or, equivalently:
        #   (t + bus_sequence_time) % bus_number = 0
        #
        # If our existing total constraints give us matching buses at time = period * i + offset for all i, then we can
        # brute-force through i values and find one that also meets our new constraint. In the worst case where
        # total_period and this_period are relatively prime (and that's what we have: in fact, all periods are prime in
        # the problem input) then we'll loop through every possible offset value with this loop. We're just looking for
        # the one that'll satisfy our new constraint.
        for i in range(this_period):
            new_offset = total_period * i + total_offset
            if new_offset % this_period == this_offset:
                break
        total_offset = new_offset

        # At this point we know that t = total_offset satisfies all of our constraints up to this point. After all,
        # previous iterations verified that it met those constraints, and we just finished verifying that it'll meet the
        # new constraint. We also know, though, that total_offset isn't the only one that'll meet those constraints.
        # This will repeat with a period equal to the least common multiple of all constraint periods, basically because
        # modulo math. All our periods are prime (and in fact, as mentioned above, plain ol prime), so in this case we
        # can just multiply in our current period to get the total one.
        total_period *= this_period

        # And now that we satisfy our constraints, we can continue the loop and add the next one.

    return total_offset, total_period


if __name__ == "__main__":
    problem = {
        "wait": get_wait_product,
        "sequence": get_sequence_start_time,
    }[sys.argv[1]]
    main(problem)
