from pathlib import Path
from PIL import Image

# Directory containing your images
IMAGE_DIR = Path("/home/trybien/Documents/GitHub/trybien.github.io/AAO BGs")

# Supported image extensions
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"}

TARGET_WIDTH = 256

print(IMAGE_DIR)
print(IMAGE_DIR.exists())
print(IMAGE_DIR.is_dir())

for image_path in IMAGE_DIR.iterdir():
    if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        continue

    try:
        with Image.open(image_path) as img:
            width, height = img.size

            if width == TARGET_WIDTH:
                print(f"Skipping {image_path.name} (already {TARGET_WIDTH}px wide)")
                continue

            # Calculate proportional height
            new_height = int(height * (TARGET_WIDTH / width))

            resized = img.resize((TARGET_WIDTH, new_height), Image.Resampling.LANCZOS)

            # Save over the original
            resized.save(image_path)

            print(f"Resized {image_path.name}: {width}x{height} -> {TARGET_WIDTH}x{new_height}")

    except Exception as e:
        print(f"Failed to process {image_path.name}: {e}")

print("Done!")
