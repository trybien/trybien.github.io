from pathlib import Path
from PIL import Image

# Directory containing your images
IMAGE_DIR = Path("/home/trybien/Documents/GitHub/trybien.github.io/AAO BGs")

# Supported image extensions
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"}

MIN_WIDTH = 256
MIN_HEIGHT = 192

print(IMAGE_DIR)
print(IMAGE_DIR.exists())
print(IMAGE_DIR.is_dir())

for image_path in IMAGE_DIR.iterdir():
    if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        continue

    try:
        with Image.open(image_path) as img:
            width, height = img.size

            TARGET_WIDTH = 256
            TARGET_HEIGHT = 192

            # Scale to each target
            height_scale = TARGET_HEIGHT / height
            width_scale = TARGET_WIDTH / width

            # Pick the scale closest to 1
            if abs(height_scale - 1) <= abs(width_scale - 1):
                scale = height_scale
                target = f"height {TARGET_HEIGHT}"
            else:
                scale = width_scale
                target = f"width {TARGET_WIDTH}"

            new_width = round(width * scale)
            new_height = round(height * scale)

            # Skip if no change
            if new_width == width and new_height == height:
                print(f"Skipping {image_path.name} (already {width}x{height})")
                continue

            resized = img.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            resized.save(image_path)

            print(
                f"Resized {image_path.name}: "
                f"{width}x{height} -> {new_width}x{new_height} "
                f"(matched {target})"
            )

    except Exception as e:
        print(f"Failed to process {image_path.name}: {e}")

print("Done!")
