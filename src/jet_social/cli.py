import argparse
import json
import shutil
import sys
from pathlib import Path

from pydantic import ValidationError

from jet_social.models import Dataset
from jet_social.pipeline import load_dataset, run


def main() -> int:
    parser = argparse.ArgumentParser(description="JET offline pilot tools")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Check local tools; no network or credentials inspected")
    schema = sub.add_parser("schema", help="Export the dataset JSON Schema")
    schema.add_argument("--output", type=Path, required=True)
    validate = sub.add_parser("validate", help="Validate a private or synthetic manifest")
    validate.add_argument("input", type=Path)
    analyze = sub.add_parser("analyze", help="Offline baseline analysis; output may be private")
    analyze.add_argument("input", type=Path)
    analyze.add_argument("--output", type=Path, default=Path("work/runs"))
    demo = sub.add_parser("demo", help="Analyze synthetic data only")
    demo.add_argument("--input", type=Path, default=Path("examples/synthetic/posts.json"))
    demo.add_argument("--output", type=Path, default=Path("work/runs"))
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            print(
                json.dumps(
                    {
                        "python": sys.version.split()[0],
                        "ffmpeg_available": shutil.which("ffmpeg") is not None,
                        "mode": "offline",
                        "live_adapters_implemented": False,
                    },
                    indent=2,
                )
            )
        elif args.command == "schema":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(Dataset.model_json_schema(), indent=2) + "\n")
        else:
            data = load_dataset(args.input)
            if args.command == "validate":
                print(f"Valid: {len(data.posts)} posts; synthetic={data.synthetic}")
            else:
                if args.command == "demo" and not data.synthetic:
                    raise ValueError("Demo accepts synthetic datasets only")
                target = run(data, args.input.read_bytes(), args.output)
                print(f"Completed offline baseline: {target}")
        return 0
    except ValidationError as exc:
        # Pydantic's default messages include input values, which can be sensitive.
        print(
            f"Validation failed ({exc.error_count()} errors); check schema locally.",
            file=sys.stderr,
        )
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except OSError:
        print("File operation failed; check local paths and permissions.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
