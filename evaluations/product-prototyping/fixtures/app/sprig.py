#!/usr/bin/env python3
"""Sprig: remembers when houseplants were last watered and says which are due."""

import argparse
import datetime as dt
import json
import pathlib
import sys


def load(path):
    p = pathlib.Path(path)
    return json.loads(p.read_text()) if p.exists() else {}


def save(path, plants):
    pathlib.Path(path).write_text(json.dumps(plants, indent=2, sort_keys=True) + "\n")


def day(text):
    return dt.date.fromisoformat(text)


def key(name):
    return name.strip().lower()


def next_watering(plant):
    return day(plant["last"]) + dt.timedelta(days=plant["every"])


def is_due(plant, today):
    return next_watering(plant) <= today


def parser():
    p = argparse.ArgumentParser(prog="sprig")
    p.add_argument("--data", default="sprig.json", help="path of the data file")
    p.add_argument("--today", type=day, default=None, help="date to act on, YYYY-MM-DD")
    sub = p.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("name")
    add.add_argument("--every", type=int, required=True, help="days between waterings")
    water = sub.add_parser("water")
    water.add_argument("name")
    remove = sub.add_parser("remove")
    remove.add_argument("name")
    sub.add_parser("due")
    sub.add_parser("list")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    today = args.today or dt.date.today()
    plants = load(args.data)

    if args.command == "add":
        name = key(args.name)
        if name in plants:
            print(f"add: {name} already exists", file=sys.stderr)
            return 2
        plants[name] = {"every": args.every, "last": today.isoformat()}
    elif args.command == "water":
        name = key(args.name)
        if name not in plants:
            print(f"water: unknown plant {name}", file=sys.stderr)
            return 3
        plants[name]["last"] = today.isoformat()
    elif args.command == "remove":
        name = key(args.name)
        if name not in plants:
            print(f"remove: unknown plant {name}", file=sys.stderr)
            return 3
        del plants[name]
    elif args.command == "due":
        for name in sorted(plants):
            if is_due(plants[name], today):
                print(name)
        return 0
    elif args.command == "list":
        for name, plant in plants.items():
            print(f"{name}  every {plant['every']} days  next {next_watering(plant)}")
        return 0

    save(args.data, plants)
    return 0


if __name__ == "__main__":
    sys.exit(main())
