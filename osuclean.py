#!/usr/bin/python3

# a python3 version of my osuclean shellscript created for portability - I aim to make it work on windows as well
# but so far I've only tested it on cpython3 on archlinux

import argparse
import re
import os
from pathlib import Path
from shutil import rmtree # pathlib.Path.rmdir cannot delete non-empty directories, thus rely on the shell

def cleanup(beatmap_root):
    """Check if there are any beatmap folders with no .osu files in them, and remove them"""
    print(f"Cleaning up empty beatmap folders from \033[33m{beatmap_root}\033[0m...")
    for empty_beatmap_path in [path for path in beatmap_root.iterdir() if path.is_dir() and not [child for child in path.glob("*.osu")]]:
        print(f"  Cleaning up \033[32m{empty_beatmap_path.name}\033[0m...")
        rmtree(empty_beatmap_path, True)

def main():
    args = argparse.ArgumentParser(prog="osuclean",
                                   description="python3 script for cleansing your !osu beatmaps folder of any shit beatmaps"
                                   )
    args.add_argument("--directory",     "-D", help="""Use this as the base directory of your !osu beatmaps, instead of the default:
                                                    %appdata%\Local\osu!\Songs""")
    args.add_argument("--cleanup",       "-C", action="store_true", help="Remove any leftover beatmap folders with no .osu files in them")
    args.add_argument("--approach-rate", "-a", type=float,          help="Remove all beatmaps with an ApproachRate value lower than specified", dest="ar")
    args.add_argument("--circle-size",   "-c", type=float,          help="Remove all beatmaps with a CircleSize value lower than specified", dest="cs")
    args.add_argument("--hp-drain",      "-d", type=float,          help="Remove all beatmaps with a HPDrainRate higher than specified", dest="hp")

    args_parsed = args.parse_args()

    if(args_parsed.directory):
        # user has provided their own path
        BEATMAP_PATH = Path(args_parsed.directory)
    else:
        BEATMAP_PATH = Path(Path.home() , 'AppData' , 'Local' , 'osu!' , 'Songs') # used by default in the case the user doesn't provide their own path

    if not BEATMAP_PATH.exists():
        print(f"Invalid beatmap path: {BEATMAP_PATH}")
        exit(1)

    if args_parsed.cleanup:
        cleanup(BEATMAP_PATH)
        exit(0)

    # compile regexes (only compile the needed ones)
    if args_parsed.ar:
        regex_AR = re.compile("(?<=ApproachRate:)(\d)+(\.)*\d*")
    if args_parsed.cs:
        regex_CS = re.compile("(?<=CircleSize:)(\d)+(\.)*\d*")
    if args_parsed.hp:
        regex_HP = re.compile("(?<=HPDrainRate:)(\d)+(\.)*\d*")

    for beatmap_path in BEATMAP_PATH.glob("**/*.osu"):
        remove = False
        with beatmap_path.open('r') as f:
            # read the first 60 lines of the file into a local buffer FIXME: there's probably a more pythonic way to do this
            buf = ""
            for i in range(1, 60):
                buf += f.readline()

            current_AR = current_CS = current_HP = 0

            if args_parsed.ar:
                res = regex_AR.search(buf)
                if res:
                    current_AR = float(res.__getitem__(0))
                    if current_AR < args_parsed.ar:
                        remove = True
            if args_parsed.cs:
                res = regex_CS.search(buf)
                if res:
                    current_CS = float(res.__getitem__(0))
                    if current_CS < args_parsed.cs:
                        remove = True
            if args_parsed.hp:
                res = regex_HP.search(buf)
                if res:
                    current_HP = float(res.__getitem__(0))
                    if current_HP > args_parsed.hp:
                        remove = True
        
        if remove:
            # map met at least one of the remove criteria, delete the .osu file

            print(f"Removing beatmap: \033[33m{beatmap_path.stem}\033[0m (AR: \033[34m{current_AR}\033[0m, CS: \033[34m{current_CS}\033[0m, HP: \033[34m{current_HP}\033[0m)")
            beatmap_path.unlink(True)

            if any(beatmap_path.parent.glob("/*.osu")):
                rmtree(beatmap_path.parent, True)

if __name__ == "__main__":
    main()
