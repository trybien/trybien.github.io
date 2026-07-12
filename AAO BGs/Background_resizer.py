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

            # Skip if image already satisfies both minimum dimensions
            if width >= MIN_WIDTH and height >= MIN_HEIGHT:
                print(
                    f"Skipping {image_path.name} "
                    f"(already {width}x{height})"
                )
                continue

            # Determine the scale needed to satisfy both minimums
            scale = max(
                MIN_WIDTH / width,
                MIN_HEIGHT / height,
                1
            )

            new_width = round(width * scale)
            new_height = round(height * scale)

            resized = img.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            # Save over the original
            resized.save(image_path)

            print(
                f"Resized {image_path.name}: "
                f"{width}x{height} -> {new_width}x{new_height}"
            )

    except Exception as e:
        print(f"Failed to process {image_path.name}: {e}")

print("Done!")
