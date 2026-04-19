import json
import os

ROWS = 20
COLS = 20

SAME_COMMUNITY_WEIGHT = 1.0
BRIDGE_WEIGHT = 0.80

SEEDS = {"c_5_5", "c_14_14"}

BRIDGES = {
    "c_5_9": {"c_5_10": BRIDGE_WEIGHT},
    "c_5_10": {"c_5_9": BRIDGE_WEIGHT},

    "c_9_5": {"c_10_5": BRIDGE_WEIGHT},
    "c_10_5": {"c_9_5": BRIDGE_WEIGHT},

    "c_9_14": {"c_10_14": BRIDGE_WEIGHT},
    "c_10_14": {"c_9_14": BRIDGE_WEIGHT},

    "c_14_9": {"c_14_10": BRIDGE_WEIGHT},
    "c_14_10": {"c_14_9": BRIDGE_WEIGHT},
}


def cell_id(r: int, c: int) -> str:
    return f"c_{r}_{c}"


def community_of(r: int, c: int) -> str:
    if r < 10 and c < 10:
        return "A"
    if r < 10 and c >= 10:
        return "B"
    if r >= 10 and c < 10:
        return "C"
    return "D"


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS


def local_neighbors(r: int, c: int):
    candidates = [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1),
    ]
    return [(nr, nc) for nr, nc in candidates if in_bounds(nr, nc)]


def build_weak_bridges_neighborhood(r: int, c: int) -> dict[str, float]:
    neighbors = {}
    my_comm = community_of(r, c)
    cid = cell_id(r, c)

    for nr, nc in local_neighbors(r, c):
        nid = cell_id(nr, nc)
        other_comm = community_of(nr, nc)

        if my_comm == other_comm:
            neighbors[nid] = SAME_COMMUNITY_WEIGHT

    if cid in BRIDGES:
        neighbors.update(BRIDGES[cid])

    return neighbors


def build_config() -> dict:
    config = {
        "cells": {
            "default": {
                "delay": "transport",
                "model": "social",
                "state": {"value": 0},
                "neighborhood": {}
            }
        }
    }

    for r in range(ROWS):
        for c in range(COLS):
            cid = cell_id(r, c)
            state_value = 1 if cid in SEEDS else 0

            config["cells"][cid] = {
                "state": {"value": state_value},
                "neighborhood": build_weak_bridges_neighborhood(r, c)
            }

    return config


def main() -> None:
    os.makedirs("config", exist_ok=True)
    output_path = "config/social_config_weak_bridges.json"

    config = build_config()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()