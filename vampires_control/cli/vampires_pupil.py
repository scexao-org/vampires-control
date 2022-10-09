#!/usr/bin/env python
from docopt import docopt
import logging
from logging.handlers import SysLogHandler
from pathlib import Path
import sys
import time

from vampires_control.devices.devices import pupil_wheel

formatter = "%(asctime)s|%(levelname)s|%(name)s - %(message)s"
logging.basicConfig(
    level=logging.DEBUG, format=formatter, handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("vampires_pupil")


numbers = [pos["number"] for pos in pupil_wheel.positions["positions"]]
descriptions = [pos["name"] for pos in pupil_wheel.positions["positions"]]

positions = "\n".join(f"  {i} {d}" for i, d in zip(numbers, descriptions))

__doc__ = f"""
Usage:
    vampires_pupil <position> [-h | --help] [-w | --wait] 
    vampires_pupil wheel (status|target|home|goto|nudge|stop|reset) [<angle>] [-h | --help] [-w | --wait]
    vampires_pupil (x|y) (status|home|goto|nudge|stop) [<pos>] [-h | --help] [-w | --wait]

Options:
    -h --help   Show this screen
    -w --wait   Block command until position has been reached, for applicable commands

Positions:
{positions}

Wheel commands:
    status          Return the current position of the pupil wheel, in {pupil_wheel.pupil_wheel.unit}
    target          Return the target position of the pupil wheel, in {pupil_wheel.pupil_wheel.unit}
    home            Home the pupil wheel
    goto  <angle>   Move the pupil wheel to the given angle, in {pupil_wheel.pupil_wheel.unit}
    nudge <angle>   Move the pupil wheel relatively by the given angle, in {pupil_wheel.pupil_wheel.unit}
    stop            Stop the pupil wheel
    reset           Reset the pupil wheel

Stage commands:
    status          Return the current position of the selected pupil wheel stage, in {pupil_wheel.pupil_stage_x.unit}
    home            Home the selected pupil wheel stage
    reset           Reset the selected pupil wheel stage
    goto  <pos>     Move the selected pupil wheel stage to the given position, in {pupil_wheel.pupil_stage_x.unit}
    stop            Stop the selected pupil wheel stage
"""

# setp 4. action
def main():
    args = docopt(__doc__)
    if len(sys.argv) == 1:
        print(args)
    elif args["wheel"]:
        if args["status"]:
            print(pupil_wheel.pupil_wheel.true_position())
        elif args["target"]:
            print(pupil_wheel.pupil_wheel.target_position())
        elif args["home"]:
            pupil_wheel.pupil_wheel.home(wait=args["--wait"])
        elif args["goto"]:
            angle = float(args["<angle>"])
            pupil_wheel.pupil_wheel.move_absolute(angle, wait=args["--wait"])
        elif args["nudge"]:
            rel_angle = float(args["<angle>"])
            pupil_wheel.pupil_wheel.move_relative(rel_angle, wait=args["--wait"])
        elif args["stop"]:
            pupil_wheel.pupil_wheel.stop()
        elif args["reset"]:
            pupil_wheel.pupil_wheel.reset()
        else:
            print(args)
    elif args["x"] or args["y"]:
        stage = pupil_wheel.pupil_stage_x if args["x"] else pupil_wheel.pupil_stage_y
        if args["status"]:
            print(stage.true_position())
        elif args["goto"]:
            pos = int(args["<pos>"])
            stage.move_absolute(pos, wait=args["--wait"])
        elif args["home"]:
            stage.home(wait=args["--wait"])
        elif args["reset"]:
            stage.reset()
        elif args["stop"]:
            stage.stop()
        else:
            print(args)
    else:
        position = int(args["<position>"])
        pupil_wheel.move_position(position, wait=args["--wait"])


if __name__ == "__main__":
    main()