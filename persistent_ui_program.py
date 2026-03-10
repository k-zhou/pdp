import serial
import time
import os
from pathlib import Path
from dotenv import load_dotenv
from contextlib import contextmanager

# class cnc_class:
#     def __init__(self, serial):
#         self.__serial = serial
#         assert self.__serial is not None

SERIAL_CONST = None
COMMANDS = {
    "move":move,
}
# IMPORTANT TODO: Check the directions and correct if needed
DIRECTIONS_MAP = {
    "up":"X",
    "down":"X-",
    "left":"Y",
    "right":"Y-"
}

def move(direction, distance_mm=1000, speed=2000):
    direction = DIRECTIONS_MAP[direction]|"X"
    SERIAL_CONST.write(f"G1 {direction}{distance_mm} F{speed}\n")

def run():
    confirm_quit = False
    while not confirm_quit:
        u_input = input()

@contextmanager
def cnc_controller_manager(*args, **kwargs):
    try:
        # 1. Open Connection
        s = serial.Serial(PORT, BAUD, timeout=1)
        SERIAL_CONST = s
        time.sleep(2) # Wait for xPRO to wake up
        s.flushInput()

        # 2. Setup Machine State
        # G21: Metric units, G91: Relative mode (move 1m from "here")
        s.write(b"G21 G91\n") 

        # 3. Run the main persistent UI
        run()
    except: Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()


if __name__ == "__main__":
    with cnc_controller_manager() as controller:
        println("Starting...")
