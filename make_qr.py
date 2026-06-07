"""Generate QR code for the love page."""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ErrorCorrect = qrcode.constants.ERROR_CORRECT_H
LANCZOS = Image.LANCZOS if hasattr(Image, "LANCZOS") else Image.ANTIALIAS

URL = "https://zastavaa.github.io/Ivona/"
OUT = r"D:\Opencode\love\qr-code.png"
OUT_FRAME = r"D:\Opencode\love\qr-card.png"

# === 1) QR with rounded modules, rose color ===
qr = qrcode.QRCode(
    version=None,
    error_correction=ErrorCorrect,
    box_size=14,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(front_color=(200, 24, 74), back_color=(255, 245, 247)),
)
qr_img = img.get_image().convert("RGBA")
qr_img.save(OUT)
print(f"Saved: {OUT}  size={qr_img.size}")

# === 2) Framed card with title ===
W, H = 900, 1180
card = Image.new("RGBA", (W, H), (10, 6, 18, 255))
draw = ImageDraw.Draw(card)

# background gradient (dark with rose glow)
for y in range(H):
    t = y / H
    r = int(20 + 40 * t)
    g = int(6 + 20 * t)
    b = int(30 + 30 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# soft glow orbs
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-200, -200, 380, 380], fill=(255, 77, 109, 80))
gd.ellipse([W - 360, H - 360, W + 200, H + 200], fill=(244, 201, 93, 70))
gd.ellipse([W // 2 - 240, H // 2 - 240, W // 2 + 240, H // 2 + 240], fill=(201, 24, 74, 35))
glow = glow.filter(ImageFilter.GaussianBlur(110))
card = Image.alpha_composite(card, glow)
draw = ImageDraw.Draw(card)

# find fonts
def find_font(candidates, size):
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

serif_candidates = [
    r"C:\Windows\Fonts\PlayfairDisplay-Bold.ttf",
    r"C:\Windows\Fonts\PlayfairDisplay-Regular.ttf",
    r"C:\Windows\Fonts\Georgia.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
]
script_candidates = [
    r"C:\Windows\Fonts\Brush Script MT.ttf",
    r"C:\Windows\Fonts\mistral.ttf",
    r"C:\Windows\Fonts\Gabriola.ttf",
    r"C:\Windows\Fonts\segoeuii.ttf",
]
sans_candidates = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]

font_script_top = find_font(script_candidates, 76)
font_title = find_font(serif_candidates, 88)
font_small = find_font(sans_candidates, 22)
font_sub = find_font(serif_candidates, 30)
font_heart = find_font([r"C:\Windows\Fonts\seguiemj.ttf", r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"], 64)

# header text
draw.text((W // 2, 110), "Za tebe", font=font_script_top, fill=(244, 201, 93, 255), anchor="mm")
draw.text((W // 2, 230), "♥", font=font_heart, fill=(255, 77, 109, 255), anchor="mm")
draw.text((W // 2, 330), "skeniraj me", font=font_sub, fill=(255, 215, 220, 255), anchor="mm")

# place QR centered
qr_w = 620
qr_resized = qr_img.resize((qr_w, qr_w), LANCZOS)
qx = (W - qr_w) // 2
qy = 400
# subtle frame around QR
draw.rounded_rectangle(
    [qx - 18, qy - 18, qx + qr_w + 18, qy + qr_w + 18],
    radius=22,
    outline=(255, 143, 163, 120),
    width=2,
)
card.paste(qr_resized, (qx, qy), qr_resized)

# footer
draw.text(
    (W // 2, qy + qr_w + 80),
    "Dve godine, jedna ljubav, beskonačno nasmeha.",
    font=find_font(serif_candidates, 26),
    fill=(255, 215, 220, 255),
    anchor="mm",
)
draw.text(
    (W // 2, qy + qr_w + 130),
    "∞",
    font=find_font(serif_candidates, 36),
    fill=(244, 201, 93, 255),
    anchor="mm",
)

card.convert("RGB").save(OUT_FRAME, quality=95)
print(f"Saved: {OUT_FRAME}  size={card.size}")
