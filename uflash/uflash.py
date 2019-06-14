"""Unzips the keymap file from qmk configurator and begins the flash
process."""

import argparse
import logging
import subprocess
import zipfile

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


def unzip_file_to_directory(input_filename: str, output_dir: str):
    """Unzip a zip file and place the contents in a directory.

    If the directory does not exist, it will be created.
    """
    output_dir_obj = Path(output_dir)
    LOG.info(f"input_filename: {input_filename}")
    LOG.info(f"output_dir_obj: {output_dir_obj}")
    with zipfile.ZipFile(input_filename, "r") as zip_ref:
        zip_ref.extractall(output_dir_obj)

    contents_of_output_directory = [x for x in output_dir_obj.iterdir()]
    LOG.debug(f"list output directory: {contents_of_output_directory}")


def flash_keymap_to_keyboard(keyboard_name: str, keymap_name: str, firmware_type: str):
    command = f"make -C {QMK_ROOT_DIR} {keyboard_name}:{keymap_name}:{firmware_type}"
    LOG.info(f"command: {command}")
    subprocess.run([command], shell=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-filename",
        type=str,
        required=True,
        help="The name of the zip file.",
    )
    parser.add_argument(
        "-o", "--output-dir", type=str, help="The name of the output dir."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO)
    unzip_file_to_directory(args.input_filename, args.output_dir)


if __name__ == "__main__":
    main()
