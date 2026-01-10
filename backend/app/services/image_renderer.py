# from PIL import Image, ImageDraw, ImageFont
# from pathlib import Path

# def render_card(template_path: str, placeholders: list, values: dict):
#     img = Image.open(template_path).convert("RGBA")
#     draw = ImageDraw.Draw(img)

#     for p in placeholders:
#         text = values.get(p["key"], "")

#         if not text:
#             continue

#         font_size = p.get("fontSize", 20)
#         font_family = p.get("fontFamily", "Arial")

#         # Fallback-safe font
#         try:
#             font = ImageFont.truetype(
#                 f"app/assets/fonts/{font_family}.ttf",
#                 font_size
#             )
#         except:
#             font = ImageFont.load_default()

#         draw.text(
#             (p["x"], p["y"]),
#             text,
#             fill=p.get("color", "#000000"),
#             font=font
#         )

#     return img
















from PIL import Image, ImageDraw, ImageFont
from pathlib import Path



def render_card(img: Image.Image, placeholders: list, values: dict):
    draw = ImageDraw.Draw(img)

    for p in placeholders:
        text = values.get(p["key"], "")
        if not text:
            continue

        font_size = p.get("fontSize", 20)
        font_family = p.get("fontFamily", "Arial")

        try:
            font = ImageFont.truetype(
                f"app/assets/fonts/{font_family}.ttf",
                font_size
            )
        except:
            font = ImageFont.load_default()

        draw.text(
            (p["x"], p["y"]),
            text,
            fill=p.get("color", "#000000"),
            font=font
        )

    return img
