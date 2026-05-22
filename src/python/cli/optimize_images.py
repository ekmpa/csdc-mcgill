"""
Resize and convert bio/avatar images to 300×300 WebP.

    python -m src.python.cli.optimize_images --source_dir assets/images/bio/
"""
import argparse
from pathlib import Path

from tqdm import tqdm
from PIL import Image

from .. import center_square_crop


def main(source_dir: str) -> None:
    source_dir = Path(source_dir)
    if not source_dir.exists():
        print(f"Directory {source_dir} does not exist.")
        return

    all_images = [p for ext in ("jpg", "jpeg", "png") for p in source_dir.glob(f"*.{ext}")]

    for image_path in tqdm(all_images):
        im = Image.open(image_path)
        if image_path.suffix.lower() == ".png":
            im = im.convert("RGB")
        if im.width != im.height:
            im = center_square_crop(im)
        im.thumbnail((300, 300))
        out = image_path.with_suffix(".avatar.webp")
        im.save(out, "WEBP", quality=80)
        print(f"Optimized {image_path} → {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize and convert bio images to WebP avatars.")
    parser.add_argument("--source_dir", type=str, required=True)
    args = parser.parse_args()
    main(args.source_dir)
