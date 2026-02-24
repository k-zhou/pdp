# This attempts to determine the number of slots a given core box has, 
# based on a cross-direction scan of the contour.

import math
import random

#####################################################################################
# Generates a synthetic dataset with
# random amounts of cores, random wall width, and random core diams

def generate_synthetic_data(wall_max_height=70):
    RNG = random
    WALL_HEIGHT = math.ceil(wall_max_height * ( RNG.random() * 0.3 + 0.7))
    WALL_WIDTH = math.ceil( 5 * ( RNG.random() * 0.6 + 0.4 ))
    SLOT_WIDTH = math.ceil(10 * ( RNG.random() * 0.8 + 0.2 ))
    CORE_WIDTH = math.ceil(SLOT_WIDTH * ( RNG.random() * 0.1 + 0.9 ))
    SCALE = math.pi / CORE_WIDTH
    LOOSE_SPACE = SLOT_WIDTH - CORE_WIDTH
    SLOT_COUNT = 3 + math.ceil(4 * RNG.random()) # 4 to 7

    TOTAL_LEN = SLOT_COUNT * SLOT_WIDTH + ( SLOT_COUNT + 1 ) * WALL_WIDTH
    SYNTH_DATA = [0 for i in range(TOTAL_LEN)]

    x = 0
    # Wall
    for i in range(WALL_WIDTH):
        SYNTH_DATA[x] = WALL_HEIGHT
        x += 1
    for i in range(SLOT_COUNT):
        # Slot and core
        start = math.floor(LOOSE_SPACE * RNG.random())
        x += start
        for j in range(CORE_WIDTH):
            SYNTH_DATA[x] = math.ceil(math.sin(SCALE * j)) + CORE_WIDTH // 2
            x += 1
        # Wall
        for j in range(WALL_WIDTH):
            SYNTH_DATA[x] = WALL_HEIGHT
            x += 1
    # TODO

    # Add noise
    NOISY_DATA = SYNTH_DATA.copy()

    return NOISY_DATA, SYNTH_DATA


#####################################################################################
# Detection routine
# The assumption being box walls are much thinner than cores, hence any core that is 
# close to the sensor and has the same height as walls will have very wide footprints
# relatively speaking.
# 
# My current plan for this is:
# 1. Scan the contour the same way like the lengthwise core contour scanning
# 2. Naívely get all instances that cross the threshold of "high" by logging their
#    start and end coords.
# 3. Filter out all those instances that have an excessive difference between their
#    start and end coords.

def detect_rows():
    # TODO
    return 0