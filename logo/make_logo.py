#!/usr/bin/env python3
"""Generate the 'Autonomous Ledger' fleet mark (Colosseum submission asset)."""
from PIL import Image, ImageDraw

S = 512
NAVY   = (11, 18, 32, 255)
PANEL  = (22, 32, 54, 255)
CYAN   = (0, 194, 184, 255)
GREEN  = (52, 211, 153, 255)
RED    = (248, 113, 113, 255)
WHITE  = (235, 240, 250, 255)
DIM    = (130, 145, 175, 255)

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Rounded-square background
d.rounded_rectangle([16, 16, S-16, S-16], radius=96, fill=NAVY)

# Ledger / terminal window panel
pad = 96
d.rounded_rectangle([pad, int(S*0.30), S-pad, int(S*0.80)], radius=28, fill=PANEL)
# traffic lights
for i, c in enumerate([RED, (245, 158, 11), GREEN]):
    x = pad + 36 + i * 44
    d.ellipse([x, int(S*0.30)+34, x+26, int(S*0.30)+60], fill=c)

# Dollar sign line "value"
d.text((pad+40, int(S*0.55)), "$", font=None)  # fallback; replaced below
# We draw glyphs as shapes for consistency across systems.

# Balance bars (USD mark) — three bars ascending = growth
bx = pad + 48
by = int(S*0.62)
heights = [34, 62, 96, 78]
for i, h in enumerate(heights):
    x0 = bx + i * 40
    y0 = by + 60 - h
    color = CYAN if i < 3 else GREEN   # last bar green (the honest/liquid target)
    d.rounded_rectangle([x0, y0, x0+26, by+60], radius=8, fill=color)

# Exclusion badge: an 'X' over a dimmed sliver = illiquid bag excluded
ex = S - pad - 84
ey = int(S*0.58)
d.rounded_rectangle([ex, ey, ex+52, ey+52], radius=14, fill=(45,55,80,255))  # bag
d.line([ex+40, ey+8, ex+116, ey+84], fill=RED, width=14)
d.line([ex+116, ey+8, ex+40, ey+84], fill=RED, width=14)

# Wordmark below
def rounded_wordmark(cx, y, word, size, color, weight=1.0):
    # Simple geometric approach using default font scaled
    from PIL import ImageFont
    try:
        font = ImageFont.load_default(size)
    except TypeError:
        font = ImageFont.load_default()
    d.text((cx, y), word, font=font, fill=color)

# Use a truetype font if present for the wordmark
import os
cands = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
font48 = font26 = None
for c in cands:
    if os.path.exists(c):
        from PIL import ImageFont
        font48 = ImageFont.truetype(c, 48)
        font26 = ImageFont.truetype(c, 26)
        break

if font48 is not None:
    wlabel = "AUTONOMOUS LEDGER"
    lw = d.textlength(wlabel, font=font48)
    d.text(((S-lw)/2, S-150), wlabel, font=font48, fill=WHITE)
    tag = "one honest USDC number"
    tw = d.textlength(tag, font=font26)
    d.text(((S-tw)/2, S-92), tag, font=font26, fill=DIM)
else:
    d.text((pad, S-160), "AUTONOMOUS LEDGER", fill=WHITE)
    d.text((pad, S-110), "one honest USDC number", fill=DIM)

img.save("/home/sonum/autonomous-ledger/logo/fleet-mark.png")
print("saved fleet-mark.png", img.size)
