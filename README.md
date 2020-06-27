# osuclean

An extremely simple python3 script for cleansing your osu! folder of any shit beatmaps.

---

## Usage

```
$ ./osuclean.py --help

usage: osuclean [-h] [--directory DIRECTORY] [--cleanup] [--approach-rate AR]
                [--circle-size CS] [--hp-drain HP]
```

- Delete all beatmaps with an AR below **9** : 

    ```./osuclean.py -a 9```
- Delete all beatmaps with CS below **9** :

    ```./osuclean.py -c 9```
- Delete all beatmaps with HP drain higher than **9** :

    ```./osuclean.py -d 9```

- If your beatmaps are stored in a non-standard (`%APPDATA\Local\osu!\Songs\`) location, specify the path with the `--directory`/`-D` flag: 

    `./osuclean.py -D "D:\my_osu_beatmaps"`

- To remove all beatmap folders with no associated difficulties in them, use `--cleanup`/`-C` (you should never have to do this in normal circumstances unless you were manually deleting `.osu` files`: 

    `./osuclean.py --cleanup`

---

I have only tested the script using cpython on archlinux but it should work on Windows w/ python3 without any problems.

---


### `fish` shell script

This repo also includes a `fish` shell script whose only purpose is to remove all beatmaps below a certain hardcoded AR. It was a quick and dirty script and I'm not maintaining it anymore, but it works pretty well so I left it in the repo.
