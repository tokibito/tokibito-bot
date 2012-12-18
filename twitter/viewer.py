#!/usr/bin/env python
# coding: utf-8
import os
import sys
import time
from subprocess import Popen, PIPE


def exec_command(command):
    p = Popen(command, stdout=PIPE)
    buf = ""
    while True:
        bits = p.stdout.read()
        buf += bits
        if buf.strip().endswith("OK."):
            break
    return buf


def main():
    if len(sys.argv) > 1:
        commands = sys.argv[1:]
    else:
        commands = ["home"]
    while True:
        try:
            result = exec_command(["./run"] + commands)
            os.system("clear")
            print(result)
            time.sleep(30)
        except KeyboardInterrupt:
            print(" exit.")
            sys.exit(0)


if __name__ == '__main__':
    main()
