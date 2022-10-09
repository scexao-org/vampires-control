#!/usr/bin/env python
from docopt import docopt
from pathlib import Path
import sys
import logging
import time
from logging.handlers import SysLogHandler

from vampires_control.devices.devices import differential_filter

formatter = "%(asctime)s|%(levelname)s|%(name)s - %(message)s"
logging.basicConfig(
    level=logging.DEBUG, format=formatter, handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("vampires_diffwheel")


numbers = [pos["number"] for pos in differential_filter.positions["positions"]]
cam1 = [pos["cam1"] for pos in differential_filter.positions["positions"]]
cam2 = [pos["cam2"] for pos in differential_filter.positions["positions"]]
descriptions = [f"{d1} / {d2}" for d1, d2 in zip(cam1, cam2)]

positions = "\n".join(f"  {i} {d}" for i, d in zip(numbers, descriptions))

__doc__ = f"""
Usage:
    vampires_diffwheel <position> [-h | --help] [-w | --wait] 
    vampires_diffwheel wheel (status|target|home|goto|nudge|stop|reset) [<angle>] [-h | --help] [-w | --wait]

Options:
    -h --help   Show this screen
    -w --wait   Block command until position has been reached, for applicable commands

Positions (cam1 / cam2):
{positions}

Wheel commands:
    status          Returns the current position of the differential filter wheel, in {differential_filter.diffwheel.unit}
    target          Returns the target position of the differential filter wheel, in {differential_filter.diffwheel.unit}
    home            Homes the differential filter wheel
    goto  <angle>   Move the differential filter wheel to the given angle, in {differential_filter.diffwheel.unit}
    nudge <angle>   Move the differential filter wheel relatively by the given angle, in {differential_filter.diffwheel.unit}
    stop            Stop the differential filter wheel
    reset           Reset the differential filter wheel
"""

# setp 4. action
def main():
    args = docopt(__doc__)
    if len(sys.argv) == 1:
        print(args)
    elif args["wheel"]:
        if args["status"]:
            print(differential_filter.diffwheel.true_position())
        elif args["target"]:
            print(differential_filter.diffwheel.target_position())
        elif args["home"]:
            differential_filter.diffwheel.home(wait=args["--wait"])
        elif args["goto"]:
            angle = float(args["<angle>"])
            differential_filter.diffwheel.move_absolute(angle, wait=args["--wait"])
        elif args["nudge"]:
            rel_angle = float(args["<angle>"])
            differential_filter.diffwheel.move_relative(rel_angle, wait=args["--wait"])
        elif args["stop"]:
            differential_filter.diffwheel.stop()
        elif args["reset"]:
            differential_filter.diffwheel.reset()
        else:
            print(args)
    else:
        position = int(args["<position>"])
        differential_filter.move_position(position, wait=args["--wait"])


if __name__ == "__main__":
    main()
