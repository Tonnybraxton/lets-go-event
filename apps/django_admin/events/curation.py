from io import BytesIO
from textwrap import wrap

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


ACCENTS = (
    ("#7c3aed", "#fb923c"),
    ("#0f766e", "#facc15"),
    ("#be123c", "#60a5fa"),
    ("#1d4ed8", "#f97316"),
    ("#6d28d9", "#ec4899"),
)


def build_editorial_placeholder(title: str, county: str, date_label: str, rank: int) -> ContentFile:
    """Build neutral local artwork that clearly asks editors for the final cover."""
    width, height = 1600, 900
    primary, secondary = ACCENTS[(rank - 1) % len(ACCENTS)]
    image = Image.new("RGB", (width, height), "#090b13")
    draw = ImageDraw.Draw(image)

    for y in range(height):
        progress = y / height
        shade = round(10 + (28 * progress))
        draw.line((0, y, width, y), fill=(shade, max(8, shade - 8), shade + 12))

    draw.ellipse((1070, -300, 1780, 410), fill=primary)
    draw.ellipse((-330, 610, 360, 1300), fill=secondary)
    draw.rounded_rectangle((88, 82, 1512, 818), radius=42, outline="#d8d5ff", width=3)

    try:
        title_font = ImageFont.load_default(size=76)
        meta_font = ImageFont.load_default(size=34)
        small_font = ImageFont.load_default(size=26)
    except TypeError:
        title_font = meta_font = small_font = ImageFont.load_default()

    title_lines = "\n".join(wrap(title.upper(), width=27)[:3])
    draw.multiline_text((145, 175), title_lines, font=title_font, fill="#ffffff", spacing=12)
    draw.text((150, 550), f"{county.upper()} COUNTY  -  {date_label.upper()}", font=meta_font, fill="#ede9fe")
    draw.text((150, 705), f"CURATED TOP 10  #{rank}  -  COVER AWAITING EDITOR", font=small_font, fill="#ffedd5")

    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return ContentFile(output.getvalue())
