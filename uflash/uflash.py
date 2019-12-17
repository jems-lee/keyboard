"""Unzips the keymap file from qmk configurator and begins the flash
process."""

import argparse
import logging
import shutil
import subprocess
from contextlib import contextmanager
import os

from dataclasses import dataclass
from pathlib import Path

LOG = logging.getLogger(__name__)

QMK_ROOT_DIR = Path("/") / "home" / "james" / "git" / "qmk_firmware"
AVRDUDE = "avrdude"
IRIS_KEYBOARD_KEYMAPS_DIR = (
        Path("/home/james")
        / "git"
        / "qmk_firmware"
        / "keyboards"
        / "keebio"
        / "iris"
        / "keymaps"
)
IRIS_KEYBOARD = "keebio/iris/rev2"


@dataclass
class Keyboard:
    zip_filename: str
    qmk_filename: str
    leaf_filename: str
    make_cmd: str


NYQUIST = Keyboard(
    zip_filename="keymap-keebio-nyquist-rev2-jameslee_nyquist.zip",
    qmk_filename="qmk_firmware/keyboards/keebio/nyquist/keymaps/jameslee_nyquist/",
    leaf_filename="jameslee_nyquist/",
    make_cmd="keebio/nyquist/rev2:jameslee_nyquist:avrdude"
)

IRIS = Keyboard(
    zip_filename="asdf",
    qmk_filename="tmp",
    leaf_filename="asdasd",
    make_cmd="asdfasdfasd"
)



@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-kb",
        "--keyboard",
        type=str,
        required=True,
        choices=['nyquist', 'iris'],
        help="The name of the keyboard, either nyquist or iris."
    )
    parser.add_argument(
        "-x",
        "--execute",
        action="store_true",
        help="Execute the code to flash the keyboard."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO)
    kb_name = args.keyboard
    if kb_name == "nyquist":
        kb = NYQUIST
    else:
        kb = IRIS

    with cd("/home/james/Documents/keyboard/"):
        if args.execute:
            print("executing code")
            subprocess.run(["unzip", kb.zip_filename])
            shutil.copy(f"{kb.leaf_filename}/keymap.c", kb.qmk_filename)
            shutil.copy(f"{kb.leaf_filename}/layers.json", kb.qmk_filename)
            shutil.copy(f"{kb.leaf_filename}/readme.md", kb.qmk_filename)
        with cd("qmk_firmware"):
            print(subprocess.run(["ls"]))
            if args.execute:
                print(subprocess.run(["make", f"{kb.make_cmd}"]))


if __name__ == "__main__":
    main()
