#!/usr/bin/env python3
"""
Microstock Automation Pipeline
Analyze images → Generate metadata → Validate keywords → Export CSV/JSON
"""

import json
import sys
from pathlib import Path

from config import IMAGES_DIR, OUTPUT_DIR, IMAGE_EXTENSIONS
from analyzers.vision import ImageAnalyzer
from generators.metadata import MetadataGenerator
from validators.keywords import KeywordValidator
from exporters.csv_exporter import CSVExporter


def find_images(directory: str) -> list[Path]:
    images = []
    for ext in IMAGE_EXTENSIONS:
        images.extend(Path(directory).glob(f"*{ext}"))
        images.extend(Path(directory).glob(f"*{ext.upper()}"))
    return sorted(images)


def run_pipeline(skip_vision: bool = False):
    images = find_images(IMAGES_DIR)

    if not images:
        print(f"No images found in {IMAGES_DIR}")
        print("Supported formats: " + ", ".join(IMAGE_EXTENSIONS))
        return

    print(f"Found {len(images)} image(s)\n")

    analyzer = ImageAnalyzer()
    generator = MetadataGenerator()
    validator = KeywordValidator()
    exporter = CSVExporter()

    all_metadata = []

    for img_path in images:
        print(f"[{img_path.name}] Analyzing...")

        if skip_vision:
            analysis = {"filename": img_path.name, "analysis": "{}"}
        else:
            analysis = analyzer.analyze(str(img_path))
            print(f"  Vision analysis complete")

        print(f"  Generating metadata...")
        metadata = generator.generate(analysis)

        metadata["filename"] = img_path.name
        metadata["keywords"] = validator.clean(
            metadata.get("keywords", []),
        )

        validation = validator.validate(metadata["keywords"])
        if not validation["valid"]:
            print(f"  Warnings: {validation['issues']}")

        print(f"  Title: {metadata.get('title', 'N/A')[:60]}...")
        print(f"  Keywords: {validation['count']}")
        print()

        all_metadata.append(metadata)

    csv_path = Path(OUTPUT_DIR) / "metadata.csv"
    json_path = Path(OUTPUT_DIR) / "metadata.json"

    exporter.export(all_metadata, str(csv_path))
    exporter.export_json(all_metadata, str(json_path))

    print("Pipeline complete!")
    print(f"  CSV:  {csv_path}")
    print(f"  JSON: {json_path}")


if __name__ == "__main__":
    skip = "--skip-vision" in sys.argv
    run_pipeline(skip_vision=skip)
