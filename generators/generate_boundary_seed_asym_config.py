import json
import os

ROWS = 20
COLS = 20

SAME_COMMUNITY_WEIGHT = 1.0
CROSS_COMMUNITY_WEIGHT = 0.30

SEEDS = {
    "c_5_9",
    "c_9_5",
    "c_10_14",
    "c_14_10",
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


def wrapped_neighbor(r: int, c: int, dr: int, dc: int) -> tuple[int, int]:
    return ((r + dr) % ROWS, (c + dc) % COLS)


def build_neighborhood(r: int, c: int) -> dict[str, float]:
    neighbors = {}
    my_comm = community_of(r, c)

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = wrapped_neighbor(r, c, dr, dc)
        neighbor_comm = community_of(nr, nc)
        weight = SAME_COMMUNITY_WEIGHT if my_comm == neighbor_comm else CROSS_COMMUNITY_WEIGHT
        neighbors[cell_id(nr, nc)] = weight

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
                "neighborhood": build_neighborhood(r, c)
            }

    return config


def main() -> None:
    os.makedirs("config", exist_ok=True)
    output_path = os.path.join("config", "social_config_boundary_seed.json")

    config = build_config()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
    