# run_game.py
import os
import sys

# Ensure the 'last_floor_standing' package is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "last_floor_standing")))

from main import main_loop

if __name__ == "__main__":
    main_loop()
