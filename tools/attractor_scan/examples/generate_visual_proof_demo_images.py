#!/usr/bin/env python3
"""Generates the two synthetic PNGs used by
`visual_proof_judge_demo.py`. Not part of the shipped package (Pillow
is not a runtime dependency of attractor_scan) -- a dev-time generator
so the two committed images are reproducible and auditable rather than
mystery binaries.

Both images are self-generated for this test, not real specimens --
unlike bifp's text-only rebuttal_judge_demo.py, an image can't be
inlined as a plain string, so the equivalent synthetic pair lives here
as PNGs instead. `singularity_pun_graphic.png` deliberately mirrors
the real mechanism basin_attractors_v1.md §2.8 Case 6 documents (a
genuine mathematical singularity -- y=1/x has a real pole at x=0 --
captioned with the word "Singularity") without reproducing the
paper's actual cited image (a real, copyrighted X post).

    pip install Pillow
    python3 examples/generate_visual_proof_demo_images.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent / "visual_proof_demo_images"


def _font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def make_genuine_benchmark_chart() -> None:
    """A real, legible bar chart -- genuine technical content that
    actually supports the paired claim in visual_proof_judge_demo.py."""
    width, height = 500, 350
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    title_font, label_font = _font(20), _font(16)

    draw.text((20, 15), "Benchmark Accuracy (%)", fill="black", font=title_font)

    bars = [("Baseline B", 42, "gray"), ("Baseline C", 51, "gray"), ("Model X", 87, "steelblue")]
    chart_bottom, chart_left, bar_width, gap, max_height = 300, 80, 90, 50, 220
    x = chart_left
    draw.line([(chart_left - 10, chart_bottom), (chart_left - 10, chart_bottom - max_height - 10)], fill="black")
    draw.line([(chart_left - 10, chart_bottom), (width - 30, chart_bottom)], fill="black")
    for label, value, color in bars:
        bar_h = int(max_height * value / 100)
        draw.rectangle([x, chart_bottom - bar_h, x + bar_width, chart_bottom], fill=color, outline="black")
        draw.text((x, chart_bottom - bar_h - 22), f"{value}%", fill="black", font=label_font)
        draw.text((x, chart_bottom + 8), label, fill="black", font=label_font)
        x += bar_width + gap

    img.save(OUT_DIR / "genuine_benchmark_chart.png")


def make_singularity_pun_graphic() -> None:
    """A real, accurately-drawn mathematical singularity (y=1/x has a
    genuine pole at x=0) captioned "Singularity at x=0" -- the same
    structural move the paper's real cited example makes (genuine
    technical precision in one narrow sense), paired in the demo with
    an unrelated AI-societal-transformation claim it has nothing to do
    with beyond the shared word."""
    width, height = 500, 500
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    title_font, label_font = _font(22), _font(16)

    draw.text((20, 15), "Singularity at x = 0", fill="black", font=title_font)

    cx, cy, scale = width // 2, height // 2 + 20, 40
    draw.line([(30, cy), (width - 30, cy)], fill="black")
    draw.line([(cx, 60), (cx, height - 30)], fill="black")
    draw.text((width - 50, cy + 8), "x", fill="black", font=label_font)
    draw.text((cx + 8, 55), "y", fill="black", font=label_font)

    def plot_branch(x_start: float, x_end: float, step: float) -> None:
        points = []
        x = x_start
        while (step > 0 and x <= x_end) or (step < 0 and x >= x_end):
            y = 1.0 / x
            px, py = cx + x * scale, cy - y * scale
            if 40 <= py <= height - 20:
                points.append((px, py))
            x += step
        if len(points) > 1:
            draw.line(points, fill="crimson", width=3)

    plot_branch(0.15, 5.0, 0.02)
    plot_branch(-0.15, -5.0, -0.02)
    draw.line([(cx, 60), (cx, height - 30)], fill="gray")  # asymptote emphasis

    img.save(OUT_DIR / "singularity_pun_graphic.png")


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    make_genuine_benchmark_chart()
    make_singularity_pun_graphic()
    print(f"wrote {OUT_DIR / 'genuine_benchmark_chart.png'}")
    print(f"wrote {OUT_DIR / 'singularity_pun_graphic.png'}")
