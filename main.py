from collections import Counter
from PIL import Image, ImageDraw

def simplify_near_white(color, threshold=235):
    r, g, b = color

    if r >= threshold and g >= threshold and b >= threshold:
        return (255, 255, 255)

    return color

def convert_image_to_bead_pattern(
    input_path,
    output_path,
    color_count_path,
    grid_size=32,
    bead_size=20,
    colors=32,
):
    image = Image.open(input_path).convert("RGB")

    small_image = image.resize((grid_size, grid_size), Image.Resampling.LANCZOS)
    small_image = small_image.quantize(colors=colors).convert("RGB")

    pattern_size = grid_size * bead_size
    pattern = Image.new("RGB", (pattern_size, pattern_size), "white")
    draw = ImageDraw.Draw(pattern)

    color_counter = Counter()

    for y in range(grid_size):
        for x in range(grid_size):
            color = simplify_near_white(small_image.getpixel((x, y)))
            color_counter[color] += 1

            left = x * bead_size
            top = y * bead_size
            right = left + bead_size
            bottom = top + bead_size

            draw.rectangle([left, top, right, bottom], fill=color)
            draw.rectangle([left, top, right, bottom], outline=(180, 180, 180))

    pattern.save(output_path)

    with open(color_count_path, "w", encoding="utf-8") as file:
        file.write("# Bead Color Count\n\n")
        file.write("| Color | RGB | Count |\n")
        file.write("|---|---|---:|\n")

        for color, count in color_counter.most_common():
            hex_color = "#{:02x}{:02x}{:02x}".format(*color)
            file.write(f"| {hex_color} | {color} | {count} |\n")


if __name__ == "__main__":
    convert_image_to_bead_pattern(
        input_path="examples/input.jpg",
        output_path="examples/pattern.png",
        color_count_path="examples/color-count.md",
        grid_size=32,
        bead_size=20,
        colors=32,
    )
