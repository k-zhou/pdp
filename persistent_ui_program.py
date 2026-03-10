import serial
import time
import os
from pathlib import Path
from dotenv import load_dotenv
from contextlib import contextmanager

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# SETTINGS
PORT = os.getenv('XPRO_PORT')  # Change to 'COM3' etc. on Windows
BAUD = 115200

SERIAL_CONST = None
# IMPORTANT TODO: Check the directions and correct if needed
DIRECTIONS_MAP = {
    "up":"X",
    "down":"X-",
    "left":"Y",
    "right":"Y-"
}

COMMANDS = None
CONFIRM_QUIT = False

# class cnc_class:
#     def __init__(self, serial):
#         self.__serial = serial
#         assert self.__serial is not None

def move(direction, distance_mm=1000, speed=2000):
    direction = DIRECTIONS_MAP.get(direction, 0) or "X"
    SERIAL_CONST.write(f"G1 {direction}{distance_mm} F{speed}\n")

def show_help():
    all_commands = " ".join(COMMANDS.keys())
    print("All available commands:", all_commands)

def quit_program():
    u_in = input('Confirm quitting by entering "yes" or "y"').strip()
    print(u_in)
    if u_in == "yes" or u_in == "y":
        CONFIRM_QUIT = True
        print(f"Should quit, {CONFIRM_QUIT}")

COMMANDS = {
    "help":"show_help",
    "move":"move",
    "quit":"quit_program"
}

def run_persistent():
    while not CONFIRM_QUIT:
        user_input = input("[CNC control]> ")
        stripped = user_input.strip()
        splitted = stripped.split(' ')
        # TODO: Based on the user's input, do stuff, until the input is quit
        if len(splitted) > 0 and COMMANDS.get(splitted[0], 0):
            joined   = None
            eval_str = f"{COMMANDS.get(splitted[0])}()"
            if len(splitted) > 1:
                bracketed = ['"' + item + '"' for item in splitted[1:]]
                joined = ", ".join(bracketed[:])
                eval_str = f"{COMMANDS.get(splitted[0])}({joined})"
            print(f"The result is {eval_str}")
            eval(eval_str)

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
        run_persistent()
        print("Exiting ...")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    with cnc_controller_manager() as controller:
        println("Starting...")

######################
# For testing purposes

def process_input(input_str):
    stripped = input_str.strip()
    splitted = stripped.split(' ')
    return splitted

def test_join_str(input_arr):
    joined = ", ".join(input_arr[:])
    return joined

def test_calling_input(input_str):
    splitted = process_input(input_str)
    joined = None
    if len(splitted) > 1:
        copy_arr = [ '"' + item + '"' for item in splitted[1:] ]
        # print(copy_arr) ### debug print
        joined = ", ".join(copy_arr[:])
    eval_str = f"{splitted[0]}({joined})"
    return eval_str