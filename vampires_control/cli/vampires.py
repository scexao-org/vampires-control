#!/usr/bin/env python
from docopt import docopt
import socket
import sys
import zmq

from vampires_control.server import DEFAULT_HOST, DEFAULT_PORT

__doc__ = f"""
Usage:
    vampires [-h | --help] [--host <HOST>] [-p <PORT> | --port <PORT>]
    vampires [--host <HOST>] [-p <PORT> | --port <PORT>] <command> [<args> ...]  [-w | --wait] [-u | --update]

Interface with the VAMPIRES instrument control daemon from the command line. 

Options:
    -h --help           Print this message
    --host <HOST>       VAMPIRES daemon host, default is {DEFAULT_HOST}
    -p --port <PORT>    VAMPIRES daemon port, default is {DEFAULT_PORT}
    -w --wait           For commands which move stages, will block until movement is completed
    -u --update         For status commands, will poll device positions to force update the state

Commands:
    status,st                     Print the full state of VAMPIRES
    get,s <keyword>               Query a keyword from the VAMPIRES status
    set,s <keyword> <value>       Set a keyword to the given value in the VAMPIRES status
    beamsplitter,bs [<cmd>...]    Control the beamsplitter wheel.
    diffwheel,diff,df [<cmd>...]  Control the differential filter wheel.
    pupil,p [<cmd>...]            Control the pupil wheel.
    focus,f [<cmd>...]            Control the focus stage.
    qwp,q [<cmd>...]              Control the two QWP rotators.
"""


def send_command(command, host=DEFAULT_HOST, port=DEFAULT_PORT, response=False):
    context = zmq.Context()
    # set up request socket
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")

    socket.send_string(command)
    response = str(socket.recv(), "ascii")
    return response


def main():
    args = docopt(__doc__, help=False, options_first=True)
    if args["<command>"] is None:
        print(__doc__)
        sys.exit(0)
    host = args["--host"] if args["--host"] is not None else DEFAULT_HOST
    port = int(args["--port"]) if args["--port"] is not None else DEFAULT_PORT

    _args = " ".join(args["<args>"])
    if args["--wait"]:
        _args += " --wait"
    cmd = f"{args['<command>']} {_args}"

    response = send_command(cmd, host, port)
    if response is not None:
        print(response)


if __name__ == "__main__":
    main()