import zipfile
from pathlib import Path
from PIL import Image, ImageDraw
from pytablericons import TablerIcons, OutlineIcon


def generate_icons(images_dir: Path) -> None:
    icons_to_generate = [
        (OutlineIcon.FOLDER,     "icon_folder.png"),
        (OutlineIcon.MOVIE,      "icon_video.png"),
        (OutlineIcon.FILE_MUSIC, "icon_audio.png"),
        (OutlineIcon.FILE,       "icon_file.png"),
    ]
    for icon_enum, filename in icons_to_generate:
        img = TablerIcons.load(icon_enum, color="#FFFFFF")
        img.save(images_dir / filename)


def generate_placeholders(images_dir: Path) -> None:
    from PIL import ImageFont

    app_name = "SimpleMediaServer"
    bg_color = (20, 20, 30)
    text_color = (220, 220, 220)
    fill_ratio = 0.8

    specs = [
        ("channel-poster_sd.png",  248,  140, "PNG"),
        ("channel-poster_hd.png",  336,  210, "PNG"),
        ("channel-poster_fhd.png", 540,  405, "PNG"),
        ("splash-screen_sd.jpg",   720,  480, "JPEG"),
        ("splash-screen_hd.jpg",   1280, 720, "JPEG"),
        ("splash-screen_fhd.jpg",  1920, 1080, "JPEG"),
    ]

    for filename, w, h, fmt in specs:
        # Binary search for the largest font size that fits within fill_ratio of the image
        lo, hi = 1, max(w, h)
        while lo < hi - 1:
            mid = (lo + hi) // 2
            font = ImageFont.load_default(size=mid)
            dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
            bbox = dummy.textbbox((0, 0), app_name, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if tw <= w * fill_ratio and th <= h * fill_ratio:
                lo = mid
            else:
                hi = mid

        font = ImageFont.load_default(size=lo)
        img = Image.new("RGB", (w, h), bg_color)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), app_name, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((w - tw) // 2, (h - th) // 2), app_name, font=font, fill=text_color)
        img.save(images_dir / filename, fmt)


def generate_logo(images_dir: Path) -> None:
    from PIL import ImageFont

    text = "SimpleRokuApp"
    target_height = 40

    lo, hi = 1, target_height * 2
    while lo < hi - 1:
        mid = (lo + hi) // 2
        font = ImageFont.load_default(size=mid)
        dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        bbox = dummy.textbbox((0, 0), text, font=font)
        if bbox[3] - bbox[1] <= target_height:
            lo = mid
        else:
            hi = mid

    font = ImageFont.load_default(size=lo)
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = dummy.textbbox((0, 0), text, font=font)
    w, h = int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((-bbox[0], -bbox[1]), text, font=font, fill=(255, 255, 255, 255))
    img.save(images_dir / "logo.png")


def main():
    script_dir = Path(__file__).parent.resolve()
    out = script_dir / "roku_app.zip"

    generate_icons(script_dir / "images")
    generate_placeholders(script_dir / "images")
    generate_logo(script_dir / "images")

    out.unlink(missing_ok=True)

    skip_names = {".DS_Store", "build.sh", "build.py", "roku_app.zip"}
    skip_dirs = {".git", ".venv", "__pycache__"}

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(script_dir.rglob("*")):
            if path.name in skip_names:
                continue
            if skip_dirs & set(path.parts):
                continue
            if path.suffix == ".pyc":
                continue
            if path.is_file():
                zf.write(path, path.relative_to(script_dir))

    print("Built: roku_app.zip")


if __name__ == "__main__":
    main()
