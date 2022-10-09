#!/usr/bin/env python
from docopt import docopt
from pathlib import Path
import sys
import logging
import time
from logging.handlers import SysLogHandler

from vampires_control.devices.devices import beamsplitter

formatter = "%(asctime)s|%(levelname)s|%(name)s - %(message)s"
logging.basicConfig(
    level=logging.DEBUG, format=formatter, handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("vampires_beamsplitter")


numbers = [pos["number"] for pos in beamsplitter.positions["positions"]]
descriptions = [pos["name"] for pos in beamsplitter.positions["positions"]]

positions = "\n".join(f"  {i} {d}" for i, d in zip(numbers, descriptions))

__doc__ = f"""
Usage:
    vampires_beamsplitter <position> [-h | --help] [-w | --wait] 
    vampires_beamsplitter wheel (status|target|home|goto|nudge|stop|reset) [<angle>] [-h | --help] [-w | --wait]

Options:
    -h --help   Show this screen
    -w --wait   Block command until position has been reached, for applicable commands

Positions:
{positions}

Wheel commands:
    status          Returns the current position of the beamsplitter wheel, in {beamsplitter.beamsplitter_wheel.unit}
    target          Returns the target position of the beamsplitter wheel, in {beamsplitter.beamsplitter_wheel.unit}
    home            Homes the beamsplitter wheel
    goto  <angle>   Move the beamsplitter wheel to the given angle, in {beamsplitter.beamsplitter_wheel.unit}
    nudge <angle>   Move the beamsplitter wheel relatively by the given angle, in {beamsplitter.beamsplitter_wheel.unit}
    stop            Stop the beamsplitter wheel
    reset           Reset the beamsplitter wheel
"""

# setp 4. action
def main():
    args = docopt(__doc__)
    if len(sys.argv) == 1:
        print(args)
    elif args["wheel"]:
        if args["status"]:
            print(beamsplitter.beamsplitter_wheel.true_position())
        elif args["target"]:
            print(beamsplitter.beamsplitter_wheel.target_position())
        elif args["home"]:
            beamsplitter.beamsplitter_wheel.home(wait=args["--wait"])
        elif args["goto"]:
            angle = float(args["<angle>"])
            beamsplitter.beamsplitter_wheel.move_absolute(angle, wait=args["--wait"])
        elif args["nudge"]:
            rel_angle = float(args["<angle>"])
            beamsplitter.beamsplitter_wheel.move_relative(
                rel_angle, wait=args["--wait"]
            )
        elif args["stop"]:
            beamsplitter.beamsplitter_wheel.stop()
        elif args["reset"]:
            beamsplitter.beamsplitter_wheel.reset()
        else:
            print(args)
    else:
        position = int(args["<position>"])
        beamsplitter.move_position(position, wait=args["--wait"])


if __name__ == "__main__":
    main()
