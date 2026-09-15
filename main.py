from collections import Counter
from PIL import Image, ImageDraw

BEAD_PALETTE = [
    ("White", (255, 255, 255)),
    ("Light Gray", (220, 220, 220)),
    ("Gray", (170, 170, 170)),
    ("Dark Gray", (100, 100, 100)),
    ("Black", (40, 40, 40)),
    ("Cream", (239, 226, 196)),
    ("Tan", (216, 197, 179)),
    ("Brown", (117, 88, 70)),
    ("Red", (200, 50, 50)),
    ("Orange", (230, 120, 45)),
    ("Yellow", (240, 210, 70)),
    ("Green", (80, 160, 90)),
    ("Light Blue", (140, 187, 198)),
    ("Blue", (74, 165, 193)),
    ("Teal", (82, 178, 194)),
    ("Purple", (167, 162, 201)),
    ("Dark Purple", (117, 108, 137)),
]


def color_distance(color_a, color_b):
    return sum((a - b) ** 2 for a, b in zip(color_a, color_b))


def simplify_neutral_color(color, neutral_tolerance=12):
    r, g, b = color

    is_neutral = (
        abs(r - g) <= neutral_tolerance
        and abs(g - b) <= neutral_tolerance
        and abs(r - b) <= neutral_tolerance
    )

    if not is_neutral:
        return color

    brightness = (r + g + b) // 3

    if brightness >= 235:
        return (255, 255, 255)
    if brightness >= 200:
        return (220, 220, 220)
    if brightness >= 150:
        return (170, 170, 170)
    if brightness >= 90:
        return (100, 100, 100)

    return (40, 40, 40)


def match_bead_color(color):
    bead_name, bead_color = min(
        BEAD_PALETTE,
        key=lambda bead: color_distance(color, bead[1]),
    )
    return bead_name, bead_color


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

    bead_counter = Counter()

    for y in range(grid_size):
        for x in range(grid_size):
            color = simplify_neutral_color(small_image.getpixel((x, y)))
            bead_name, bead_color = match_bead_color(color)
            bead_counter[(bead_name, bead_color)] += 1

            left = x * bead_size
            top = y * bead_size
            right = left + bead_size
            bottom = top + bead_size

            draw.rectangle([left, top, right, bottom], fill=bead_color)
            draw.rectangle([left, top, right, bottom], outline=(180, 180, 180))

    pattern.save(output_path)

    with open(color_count_path, "w", encoding="utf-8") as file:
        file.write("# Bead Color Count\n\n")
        file.write("| Bead Color | RGB | Count |\n")
        file.write("|---|---|---:|\n")

        for (bead_name, bead_color), count in bead_counter.most_common():
            hex_color = "#{:02x}{:02x}{:02x}".format(*bead_color)
            file.write(f"| {bead_name} ({hex_color}) | {bead_color} | {count} |\n")


if __name__ == "__main__":
    convert_image_to_bead_pattern(
        input_path="examples/input.jpg",
        output_path="examples/pattern.png",
        color_count_path="examples/color-count.md",
        grid_size=32,
        bead_size=20,
        colors=32,
    )
