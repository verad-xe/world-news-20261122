"""Caption the generated artwork into the finished entry image.

Takes one raw Stable Diffusion XL candidate (1024x1024, no text — image
models garble lettering) and draws the day's headlines onto it as a
newspaper-style front page: a masthead band on top and a headline stack
at the bottom.  The headlines are the stories the world's wires led with
on Sunday 22 November 2026:

  * Russian missiles land in Poland; NATO's chief vows to defend Poland
  * Iran strikes tankers in the Strait of Hormuz; Houthis strike Riyadh;
    Bahrain reports an Iranian strike on an industrial site
  * Mexican forces capture cartel kingpin "El Chapo Isidro" in Sinaloa
  * G20 summit opens in Johannesburg, the first on African soil
  * Magnitude 6.7 earthquake hits Peru's Andes; no deaths reported

Usage: python3 caption.py cand_42.png entry.png
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RED = (200, 32, 40)
WHITE = (245, 245, 240)
DIM = (210, 210, 205)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD, size)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int,
             start: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 10 and draw.textlength(text, font=font(size)) > max_width:
        size -= 2
    return font(size)


def main() -> None:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    img = Image.open(src).convert("RGB")
    w, h = img.size
    assert (w, h) == (1024, 1024), f"unexpected size {img.size}"
    draw = ImageDraw.Draw(img, "RGBA")
    margin = 36
    maxw = w - 2 * margin

    # --- masthead band -------------------------------------------------
    top_h = 168
    draw.rectangle([0, 0, w, top_h], fill=(8, 10, 18, 235))
    draw.rectangle([0, top_h, w, top_h + 6], fill=RED + (255,))
    f_title = fit_font(draw, "THE WORLD ON EDGE", maxw, 84)
    draw.text((margin, 18), "THE WORLD ON EDGE", font=f_title, fill=WHITE)
    date = "SUNDAY 22 NOVEMBER 2026"
    f_date = font(31)
    draw.text((margin, 114), date, font=f_date, fill=RED)
    date_end = margin + draw.textlength(date, font=f_date)
    tag = "· THE DAY IN ONE PICTURE"
    f_tag = fit_font(draw, tag, w - margin - (date_end + 26), 28)
    draw.text((date_end + 26, 117), tag, font=f_tag, fill=DIM)

    # --- headline stack ------------------------------------------------
    lines = [
        "RUSSIAN MISSILES LAND IN POLAND — NATO VOWS TO DEFEND IT",
        "IRAN STRIKES TANKERS IN HORMUZ · HOUTHIS HIT RIYADH",
        "MEXICO CAPTURES CARTEL KINGPIN 'EL CHAPO ISIDRO'",
        "G20 OPENS IN JOHANNESBURG · 6.7 QUAKE ROCKS PERU",
    ]
    line_h = 52
    bot_h = 26 + line_h * len(lines) + 14
    y0 = h - bot_h
    draw.rectangle([0, y0, w, h], fill=(8, 10, 18, 228))
    draw.rectangle([0, y0 - 6, w, y0], fill=RED + (255,))
    y = y0 + 24
    for line in lines:
        f = fit_font(draw, line, maxw, 37)
        draw.text((margin, y), line, font=f, fill=WHITE)
        y += line_h

    img.save(dst, format="PNG", optimize=True)
    size = dst.stat().st_size
    print(f"wrote {dst} ({size} bytes)")
    if size > 1_048_576:
        # Palette-quantize: flat illustration survives 256 colours well.
        img.convert("RGB").quantize(colors=256, method=Image.Quantize.FASTOCTREE).save(
            dst, format="PNG", optimize=True)
        size = dst.stat().st_size
        print(f"quantized -> {size} bytes")
    assert size <= 1_048_576, "still over the 1 MiB cap"


if __name__ == "__main__":
    main()
