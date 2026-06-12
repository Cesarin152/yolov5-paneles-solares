import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(command, cwd=None):
    print(">", subprocess.list2cmdline([str(item) for item in command]))
    subprocess.run([str(item) for item in command], cwd=cwd, check=True)


def copy_balanced_subset(dataset, target, split, per_class):
    selected = []
    selected_stems = set()
    label_dir = dataset / "labels" / split
    image_dir = dataset / "images" / split
    for class_id in range(4):
        matches = []
        for label_path in sorted(label_dir.glob("*.txt")):
            classes = {
                int(line.split()[0])
                for line in label_path.read_text(encoding="utf-8-sig").splitlines()
                if line.strip()
            }
            if class_id in classes and label_path.stem not in selected_stems:
                matches.append(label_path)
            if len(matches) == per_class:
                break
        if len(matches) < per_class:
            raise RuntimeError(
                f"No hay suficientes ejemplos de clase {class_id} en {split}"
            )
        for label_path in matches:
            image_matches = [
                path
                for path in image_dir.glob(label_path.stem + ".*")
                if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
            ]
            if len(image_matches) != 1:
                raise RuntimeError(f"Imagen ambigua para {label_path}")
            image_path = image_matches[0]
            selected_stems.add(label_path.stem)
            selected.append((image_path, label_path))

    image_target = target / "images" / split
    label_target = target / "labels" / split
    image_target.mkdir(parents=True, exist_ok=True)
    label_target.mkdir(parents=True, exist_ok=True)
    for image_path, label_path in selected:
        shutil.copy2(image_path, image_target / image_path.name)
        shutil.copy2(label_path, label_target / label_path.name)
    return selected


def main():
    root = Path(__file__).resolve().parents[1]
    python = root / ".venv" / "Scripts" / "python.exe"
    yolov5 = root / "vendor" / "yolov5"
    dataset = root / "data" / "solar_panels"
    smoke = root / "smoke_test"

    required = [
        python,
        yolov5 / "detect.py",
        dataset / "images" / "test",
        root / "scripts" / "validate_dataset.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Faltan archivos:\n" + "\n".join(missing))

    run(
        [
            python,
            root / "scripts" / "validate_dataset.py",
            "--dataset",
            dataset,
            "--output",
            root / "reports" / "dataset_report.json",
        ]
    )

    if smoke.exists():
        shutil.rmtree(smoke)
    input_dir = smoke / "input"
    input_dir.mkdir(parents=True)
    sample_images = sorted((dataset / "images" / "test").iterdir())[:2]
    for source in sample_images:
        shutil.copy2(source, input_dir / source.name)

    run(
        [
            python,
            yolov5 / "detect.py",
            "--weights",
            "yolov5n.pt",
            "--img",
            "320",
            "--conf",
            "0.25",
            "--source",
            input_dir,
            "--project",
            smoke,
            "--name",
            "inference",
            "--device",
            "cpu",
            "--exist-ok",
        ],
        cwd=yolov5,
    )

    outputs = [
        path
        for path in (smoke / "inference").iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    ]
    if len(outputs) != len(sample_images):
        raise RuntimeError(
            f"Se esperaban {len(sample_images)} salidas y se generaron {len(outputs)}"
        )
    smoke_dataset = smoke / "dataset"
    train_samples = copy_balanced_subset(
        dataset, smoke_dataset, "train", per_class=2
    )
    val_samples = copy_balanced_subset(dataset, smoke_dataset, "val", per_class=1)
    smoke_yaml = smoke / "smoke_dataset.yaml"
    smoke_yaml.write_text(
        f"""path: {smoke_dataset.as_posix()}
train: images/train
val: images/val

nc: 4
names: [cover, crack, dust, normal]
""",
        encoding="utf-8",
    )

    run(
        [
            python,
            yolov5 / "train.py",
            "--weights",
            yolov5 / "yolov5n.pt",
            "--data",
            smoke_yaml,
            "--epochs",
            "1",
            "--batch",
            "4",
            "--img",
            "160",
            "--workers",
            "0",
            "--device",
            "cpu",
            "--project",
            smoke,
            "--name",
            "training",
            "--exist-ok",
        ],
        cwd=yolov5,
    )
    training_results = smoke / "training" / "results.csv"
    if not training_results.exists():
        raise RuntimeError("La prueba de entrenamiento no generó results.csv")

    report = {
        "python": str(python),
        "yolov5": str(yolov5),
        "device": "cpu",
        "input_images": [path.name for path in sample_images],
        "output_images": [path.name for path in outputs],
        "smoke_train_images": len(train_samples),
        "smoke_val_images": len(val_samples),
        "training_results": str(training_results),
        "status": "ok",
    }
    (smoke / "smoke_test_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
