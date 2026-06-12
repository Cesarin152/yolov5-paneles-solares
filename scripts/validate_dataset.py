import argparse
import json
from collections import Counter
from pathlib import Path


CLASSES = ["cover", "crack", "dust", "normal"]
SPLITS = ["train", "val", "test"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def validate(dataset: Path):
    report = {"dataset": str(dataset), "classes": CLASSES, "splits": {}}
    all_errors = []
    for split in SPLITS:
        image_dir = dataset / "images" / split
        label_dir = dataset / "labels" / split
        images = {
            path.stem: path
            for path in image_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        }
        labels = {path.stem: path for path in label_dir.glob("*.txt")}
        missing_labels = sorted(set(images) - set(labels))
        missing_images = sorted(set(labels) - set(images))
        class_boxes = Counter()
        invalid_lines = []
        total_boxes = 0
        for stem, label_path in labels.items():
            for line_number, line in enumerate(
                label_path.read_text(encoding="utf-8-sig").splitlines(), 1
            ):
                parts = line.split()
                try:
                    if len(parts) != 5:
                        raise ValueError("expected 5 columns")
                    class_id = int(parts[0])
                    coordinates = [float(value) for value in parts[1:]]
                    if class_id not in range(len(CLASSES)):
                        raise ValueError("invalid class")
                    if any(value < 0 or value > 1 for value in coordinates):
                        raise ValueError("coordinate outside [0, 1]")
                    if coordinates[2] <= 0 or coordinates[3] <= 0:
                        raise ValueError("non-positive box dimensions")
                    class_boxes[class_id] += 1
                    total_boxes += 1
                except ValueError as error:
                    invalid_lines.append(
                        {
                            "file": str(label_path),
                            "line": line_number,
                            "content": line,
                            "error": str(error),
                        }
                    )
        split_errors = []
        if missing_labels:
            split_errors.append(f"{len(missing_labels)} images without labels")
        if missing_images:
            split_errors.append(f"{len(missing_images)} labels without images")
        if invalid_lines:
            split_errors.append(f"{len(invalid_lines)} invalid annotation lines")
        all_errors.extend(f"{split}: {error}" for error in split_errors)
        report["splits"][split] = {
            "images": len(images),
            "labels": len(labels),
            "boxes": total_boxes,
            "boxes_by_class": {
                CLASSES[class_id]: class_boxes[class_id]
                for class_id in range(len(CLASSES))
            },
            "missing_labels": missing_labels,
            "missing_images": missing_images,
            "invalid_lines": invalid_lines,
        }
    report["valid"] = not all_errors
    report["errors"] = all_errors
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate(args.dataset)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    raise SystemExit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()
