import argparse
from functools import partial

from ft.functions import function_list
from ft.internal import add_dynamic_type
from ft.error import panic


def get_function(name, args, enable_currying=True):
    try:
        function = function_list[name]
    except KeyError:
        panic("Command not found: '{}'".format(name))

    if enable_currying:
        # Partially apply the command
        if len(args) > 0:
            args = map(add_dynamic_type, args)
            function = partial(function, *args)

    return function


def new_command(name, enable_currying=True):
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument('function', help='the function to run for each input')
    parser.add_argument('args', help='optional arguments', nargs='*')
    parser.add_argument('--column', '-c', type=int, help='apply function to a specific column')

    args = parser.parse_args()

    command = get_function(args.function, args.args, enable_currying)

    return command, args
