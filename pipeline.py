#!/usr/bin/env python
"""
Microstock Automation Pipeline (Python 2.7 compatible)
Analyze images -> Generate metadata -> Validate keywords -> Export CSV/JSON
"""

from __future__ import print_function
import os
import sys

from config import IMAGES_DIR, OUTPUT_DIR, IMAGE_EXTENSIONS
from analyzers.vision import ImageAnalyzer
from generators.metadata import MetadataGenerator
from validators.keywords import KeywordValidator
from exporters.csv_exporter import CSVExporter


def find_images(directory):
    images = []
    try:
        entries = os.listdir(directory)
    except OSError:
        return images

    for name in entries:
        ext = os.path.splitext(name)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            images.append(os.path.join(directory, name))
    return sorted(images)


def run_pipeline(skip_vision=False):
    images = find_images(IMAGES_DIR)

    if not images:
        print("No images found in {dir}".format(dir=IMAGES_DIR))
        print("Supported formats: " + ", ".join(IMAGE_EXTENSIONS))
        return

    print("Found {count} image(s)\n".format(count=len(images)))

    analyzer = ImageAnalyzer()
    generator = MetadataGenerator()
    validator = KeywordValidator()
    exporter = CSVExporter()

    all_metadata = []

    for img_path in images:
        img_name = os.path.basename(img_path)
        print("[{name}] Analyzing...".format(name=img_name))

        if skip_vision:
            analysis = {"filename": img_name, "analysis": "{}"}
        else:
            analysis = analyzer.analyze(img_path)
            print("  Vision analysis complete")

        print("  Generating metadata...")
        metadata = generator.generate(analysis)

        metadata["filename"] = img_name
        metadata["keywords"] = validator.clean(metadata.get("keywords", []))

        validation = validator.validate(metadata["keywords"])
        if not validation["valid"]:
            print("  Warnings: {issues}".format(issues=validation["issues"]))

        title_preview = metadata.get("title", "N/A")[:60]
        print("  Title: {title}...".format(title=title_preview))
        print("  Keywords: {count}".format(count=validation["count"]))
        print()

        all_metadata.append(metadata)

    csv_path = os.path.join(OUTPUT_DIR, "metadata.csv")
    json_path = os.path.join(OUTPUT_DIR, "metadata.json")

    exporter.export(all_metadata, csv_path)
    exporter.export_json(all_metadata, json_path)

    print("Pipeline complete!")
    print("  CSV:  {path}".format(path=csv_path))
    print("  JSON: {path}".format(path=json_path))


if __name__ == "__main__":
    skip = "--skip-vision" in sys.argv
    run_pipeline(skip_vision=skip)
