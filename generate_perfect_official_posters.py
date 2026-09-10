import fitz
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

base_dir = r"c:\Users\Dell\Desktop\Designing and Email Marketing"
assets_dir = os.path.join(base_dir, "assets")
output_dir = os.path.join(base_dir, "POSTS_AND_REELS_OUTPUT")
os.makedirs(output_dir, exist_ok=True)

# 1. Open brochure.pdf and create updated cover page
doc = fitz.open(os.path.join(base_dir, "brochure.pdf"))
page1 = doc[0]

# Sample background color at date position (y=430, x=300)
# Page 1 background in that area is soft pink/cream: approx #fdedeb or #fbeae8
# Let's inspect exact pixel color from rendered pixmap
pix = page1.get_pixmap(dpi=150)
# Convert to PIL Image to get exact background color around (300, 434)
img_p1_sample = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
scale_x = pix.width / page1.rect.width
scale_y = pix.height / page1.rect.height

bg_color_rgb = img_p1_sample.getpixel((int(290 * scale_x), int(410 * scale_y)))
print(f"Sampled background color: {bg_color_rgb}")
bg_color_norm = (bg_color_rgb[0] / 255.0, bg_color_rgb[1] / 255.0, bg_color_rgb[2] / 255.0)

# Redact old date text '1 7 t o 1 9 O c t ob e r'
rect_date = fitz.Rect(140, 415, 455, 455)
page1.add_redact_annot(rect_date, fill=bg_color_norm)
page1.apply_redactions()

# Insert new text '1 7 - 1 8 - 1 9   O c t o b e r'
# Color of text: deep charcoal / warm brown: rgb(60, 40, 45) -> (0.24, 0.16, 0.18)
new_date_text = "1 7 - 1 8 - 1 9   O c t o b e r"
page1.insert_text(
    fitz.Point(170, 440),
    new_date_text,
    fontsize=20,
    fontname="helv", # Will render clean and sharp
    color=(0.22, 0.15, 0.18)
)

# Insert THE PINKCITY CLUB logo at top (above PRESENTS)
# PRESENTS is at y=145
# Insert logo at rect (x0=210, y0=40, x1=385, y1=130)
logo_img_path = os.path.join(assets_dir, "the_pinkcity_club_logo_transparent.png")
if os.path.exists(logo_img_path):
    logo_rect = fitz.Rect(210, 45, 385, 135)
    page1.insert_image(logo_rect, filename=logo_img_path)

# Render updated Page 1 at 300 DPI (approx 2480 x 3508)
mat = fitz.Matrix(4.0, 4.0) # 4x scale
pix_updated = page1.get_pixmap(matrix=mat, alpha=False)
updated_cover_pil = Image.frombytes("RGB", [pix_updated.width, pix_updated.height], pix_updated.samples)
updated_cover_path = os.path.join(assets_dir, "updated_authentic_cover_hd.png")
updated_cover_pil.save(updated_cover_path, quality=100)
print(f"Saved updated authentic cover: {pix_updated.width}x{pix_updated.height}")

# -------------------------------------------------------------------------
# CREATE 4 CLEAN, BEAUTIFUL, AUTHENTIC SOCIAL MEDIA ASSETS
# -------------------------------------------------------------------------

# 1. Official Story Poster (9:16 - 1080 x 1920)
# Take the authentic cover and frame it in 1080x1920 with venue footer
story_bg = Image.new("RGB", (1080, 1920), bg_color_rgb)
# Resize cover to fit nicely in center
# Cover aspect ratio is 595.28 / 841.89 = 0.707. Story aspect ratio is 1080 / 1920 = 0.5625
cover_h = 1720
cover_w = int(cover_h * (pix_updated.width / pix_updated.height))
cover_resized = updated_cover_pil.resize((cover_w, cover_h), Image.Resampling.LANCZOS)

# Center cover horizontally
cx = int((1080 - cover_w) / 2)
story_bg.paste(cover_resized, (cx, 20))

# Bottom Venue Footer
draw_story = ImageDraw.Draw(story_bg)
try:
    font_venue = ImageFont.truetype("arialbd.ttf", 22)
    font_contact = ImageFont.truetype("arialbd.ttf", 26)
except:
    font_venue = font_contact = ImageFont.load_default()

# Venue bar at bottom
draw_story.rectangle([(0, 1780), (1080, 1920)], fill=(219, 18, 93))
v1 = "📍 High Tension Road, Chak Karol, Near HP Petrol Pump, Jaipur - 302017"
v2 = "🎟️ PASSES & INQUIRIES: +91 80585 26618  |  AGE GROUP: 16–50"

tb1 = draw_story.textbbox((0, 0), v1, font=font_venue)
tb2 = draw_story.textbbox((0, 0), v2, font=font_contact)
draw_story.text((int((1080 - (tb1[2] - tb1[0])) / 2), 1805), v1, fill=(255, 255, 255), font=font_venue)
draw_story.text((int((1080 - (tb2[2] - tb2[0])) / 2), 1850), v2, fill=(255, 220, 235), font=font_contact)

out_story = os.path.join(output_dir, "01_Official_Story_Poster_9x16.jpg")
story_bg.save(out_story, quality=98)
print("Saved 01_Official_Story_Poster_9x16.jpg")


# 2. Official Feed Banner (1:1 - 1200 x 1200)
# Crop & compose the authentic cover centered with the exact typography, dancers, logo & 17-18-19 Oct
feed_bg = Image.new("RGB", (1200, 1200), bg_color_rgb)
cover_feed_w = 1200
cover_feed_h = int(cover_feed_w * (pix_updated.height / pix_updated.width))
cover_feed_resized = updated_cover_pil.resize((cover_feed_w, cover_feed_h), Image.Resampling.LANCZOS)

# Center crop to 1200x1200 focusing on top logo + typography + dancers
feed_bg.paste(cover_feed_resized, (0, 0))

# Bottom venue overlay bar
draw_feed = ImageDraw.Draw(feed_bg)
draw_feed.rectangle([(0, 1100), (1200, 1200)], fill=(219, 18, 93))
f_v1 = "📍 High Tension Road, Chak Karol, Near HP Petrol Pump, Jaipur - 302017"
f_v2 = "🎟️ BOOK EARLY BIRD PASSES: +91 80585 26618  |  THE PINKCITY CLUB"
ftb1 = draw_feed.textbbox((0, 0), f_v1, font=font_venue)
ftb2 = draw_feed.textbbox((0, 0), f_v2, font=font_contact)
draw_feed.text((int((1200 - (ftb1[2] - ftb1[0])) / 2), 1118), f_v1, fill=(255, 255, 255), font=font_venue)
draw_feed.text((int((1200 - (ftb2[2] - ftb2[0])) / 2), 1155), f_v2, fill=(255, 220, 235), font=font_contact)

out_feed = os.path.join(output_dir, "02_Official_Feed_Banner_1x1.jpg")
feed_bg.save(out_feed, quality=98)
print("Saved 02_Official_Feed_Banner_1x1.jpg")


# 3. Export all 8 Authentic Brochure Pages as High-Res Carousel Images (1200 x 1700)
carousel_dir = os.path.join(output_dir, "Carousel_Slides")
os.makedirs(carousel_dir, exist_ok=True)

# Save page 1 updated
updated_cover_pil.save(os.path.join(carousel_dir, "Slide_01_Cover.jpg"), quality=95)

# Render pages 2 to 8
for p_idx in range(1, len(doc)):
    p = doc[p_idx]
    pix_p = p.get_pixmap(matrix=mat, alpha=False)
    p_img = Image.frombytes("RGB", [pix_p.width, pix_p.height], pix_p.samples)
    slide_name = f"Slide_{p_idx+1:02d}_{['Welcome', 'Vision', 'Whats_Happening', 'Sponsorship_Benefits', 'Sponsorship_Tiers', 'Audience', 'Venue_Contact'][p_idx-1]}.jpg"
    p_img.save(os.path.join(carousel_dir, slide_name), quality=95)
    print(f"Saved Carousel {slide_name}")

print("All official graphics generated with 100% authenticity!")
