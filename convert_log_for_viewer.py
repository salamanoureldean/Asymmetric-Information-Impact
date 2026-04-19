from pathlib import Path
import sys


def convert_model_name(name: str) -> str:
    if not name.startswith("c_"):
        return name

    parts = name.split("_")
    if len(parts) != 3:
        return name

    try:
        r = int(parts[1])
        c = int(parts[2])
        return f"({r},{c})"
    except ValueError:
        return name


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("log/social_log_base_scenario_log.csv")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("log/social_log_base_scenario_viewer_log.csv")

    with input_path.open("r", encoding="utf-8") as fin, output_path.open("w", encoding="utf-8") as fout:
        for i, line in enumerate(fin):
            line = line.rstrip("\n")

            if i == 0 and line.startswith("sep="):
                fout.write(line + "\n")
                continue

            if i == 1 and line == "time;model_id;model_name;port_name;data":
                fout.write(line + "\n")
                continue

            parts = line.split(";")
            if len(parts) != 5:
                fout.write(line + "\n")
                continue

            parts[2] = convert_model_name(parts[2])
            fout.write(";".join(parts) + "\n")

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()