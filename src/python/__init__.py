import os
from pathlib import Path
import re
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError

from PIL import Image


def center_square_crop(im):
    width, height = im.size
    if width > height:
        left = (width - height) / 2
        right = left + height
        top = 0
        bottom = height
    else:
        left = 0
        right = width
        top = (height - width) / 2
        bottom = top + width
    return im.crop((left, top, right, bottom))


def parse_issue_body(body):
    """Parse the body of a GitHub issue into a dict keyed by heading text."""
    parsed = {}
    k = None
    for line in body.split("\n"):
        if line.startswith("###"):
            k = line.removeprefix("###").strip().lower().replace(" ", "_")
            parsed[k] = ""
        elif k is not None:
            parsed[k] += line.strip()
    return parsed


def find_urls(text):
    return list(dict.fromkeys(re.findall(r"(?P<url>https?://[^\s)]+)", text)))


def save_url_image(
    fname,
    profile,
    key,
    image_dir,
    size=(400, 400),
    crop_center=False,
    convert_to_jpg=False,
    jpg_quality=80,
):
    accepted_extensions = {
        "", "jpg", "jpeg", "png", "gif", "svg", "webp", "bmp", "tiff", "ico", "eps", "blp",
    }
    if not profile.get(key):
        return None

    urls = find_urls(profile[key])
    if not urls:
        return None

    for url in urls:
        ext = os.path.splitext(url)[1][1:]
        sep = next((ch for ch in ext if not ch.isalpha()), None)
        if sep is not None:
            ext = ext.partition(sep)[0]

        if ext not in accepted_extensions:
            print(f"Extension {ext} not in accepted extensions: {accepted_extensions}")
            continue

        if ext == "jpeg":
            ext = "jpg"

        image_dir = Path(image_dir)
        file_path = image_dir / (f"{fname}.{ext}" if ext else fname)
        image_dir.mkdir(parents=True, exist_ok=True)

        try:
            urlretrieve(url, str(file_path))
        except (HTTPError, URLError, ValueError) as e:
            print(f"Could not download image from {url}: {e}")
            file_path.unlink(missing_ok=True)
            continue

        if ext in ("svg", "gif"):
            return "/" + str(file_path)

        try:
            im = Image.open(file_path)
            if crop_center:
                im = center_square_crop(im)
            im.thumbnail(size)
        except Exception as e:
            print(f"Could not open {url} as image: {e}")
            file_path.unlink(missing_ok=True)
            continue

        if ext == "jpg":
            im.save(file_path, quality=jpg_quality)
        elif ext == "":
            file_path = file_path.with_suffix(".jpg")
            im.convert("RGB").save(file_path, quality=jpg_quality)
        elif convert_to_jpg:
            file_path = file_path.with_suffix(".jpg")
            im.convert("RGB").save(file_path, quality=jpg_quality)
        else:
            im.save(file_path)

        return "/" + str(file_path)


def write_content_to_file(formatted, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, formatted["filename"]), "w") as f:
        f.write(formatted["content"])


def remove_items_with_values(dictionary, value):
    return {k: v for k, v in dictionary.items() if v != value}


def remove_keys(dictionary, keys_to_remove):
    return {k: v for k, v in dictionary.items() if k not in set(keys_to_remove)}
