from PIL import Image


def convert_image_to_pixel_art(input_path, output_path, size=32):
    image = Image.open(input_path).convert("RGB")
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    image = image.resize((size * 20, size * 20), Image.Resampling.NEAREST)
    image.save(output_path)


if __name__ == "__main__":
    convert_image_to_pixel_art("examples/input.jpg", "examples/output.png")
