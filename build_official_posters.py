import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

base_dir = r"c:\Users\Dell\Desktop\Designing and Email Marketing"
assets_dir = os.path.join(base_dir, "assets")
output_dir = os.path.join(base_dir, "POSTS_AND_REELS_OUTPUT")
os.makedirs(output_dir, exist_ok=True)

# 1. Load the transparent logo from brochure
logo_raw = Image.open(os.path.join(assets_dir, "the_pinkcity_club_logo_transparent.png")).convert("RGBA")
bbox = logo_raw.getbbox()
if bbox:
    logo_raw = logo_raw.crop(bbox)

# 2. Load the exact typography crop from brochure page 1
typo_crop = Image.open(os.path.join(assets_dir, "brochure_typography_crop.png")).convert("RGBA")
typo_np = np.array(typo_crop)
h, w, _ = typo_np.shape

r = typo_np[:, :, 0]
g = typo_np[:, :, 1]
b = typo_np[:, :, 2]

# Magenta letters
is_magenta = (r > 130) & (g < 110) & (b > 50)
clean_typo_data = np.zeros((h, w, 4), dtype=np.uint8)
clean_typo_data[:, :, 0] = r
clean_typo_data[:, :, 1] = g
clean_typo_data[:, :, 2] = b
clean_typo_data[:, :, 3] = np.where(is_magenta, 255, 0)

clean_typo = Image.fromarray(clean_typo_data)
bbox_t = clean_typo.getbbox()
if bbox_t:
    clean_typo = clean_typo.crop(bbox_t)
clean_typo.save(os.path.join(assets_dir, "exact_brochure_typo_transparent.png"))
print("Extracted exact typography cutout successfully:", clean_typo.size)

# Fonts
try:
    font_bold_large = ImageFont.truetype("arialbd.ttf", 52)
    font_bold_med = ImageFont.truetype("arialbd.ttf", 34)
    font_bold_sm = ImageFont.truetype("arialbd.ttf", 26)
except:
    font_bold_large = font_bold_med = font_bold_sm = ImageFont.load_default()

# -------------------------------------------------------------
# POSTER 1: 9:16 Instagram Story Poster (1080 x 1920)
# -------------------------------------------------------------
bg_story = Image.open(os.path.join(assets_dir, "pinkcity_genz_garba_story.jpg")).convert("RGBA")
bg_story = bg_story.resize((1080, 1920), Image.Resampling.LANCZOS)

overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Top Logo Header Pill
draw.rounded_rectangle([(340, 45), (740, 175)], radius=20, fill=(255, 255, 255, 245), outline=(255, 0, 127, 220), width=2)
logo_resized = logo_raw.resize((260, int(260 * logo_raw.height / logo_raw.width)), Image.Resampling.LANCZOS)
logo_x = int((1080 - logo_resized.width) / 2)
logo_y = 52
overlay.paste(logo_resized, (logo_x, logo_y), logo_resized)

# Center Typography Card
card_w, card_h = 960, 470
card_x, card_y = 60, 200
draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=32, fill=(255, 240, 245, 245), outline=(255, 0, 127, 180), width=3)

# Exact Typography from brochure
typo_w = 860
typo_h = int(typo_w * clean_typo.height / clean_typo.width)
typo_resized = clean_typo.resize((typo_w, typo_h), Image.Resampling.LANCZOS)
typo_x = int((1080 - typo_w) / 2)
typo_y = card_y + 25
overlay.paste(typo_resized, (typo_x, typo_y), typo_resized)

# Date Ribbon: 17 - 18 - 19 OCTOBER
date_box_y = typo_y + typo_h + 12
draw.rounded_rectangle([(card_x + 80, date_box_y), (card_x + card_w - 80, date_box_y + 68)], radius=34, fill=(219, 18, 93, 255))
date_text = "17 - 18 - 19 OCTOBER"
date_bbox = draw.textbbox((0, 0), date_text, font=font_bold_large)
tw = date_bbox[2] - date_bbox[0]
draw.text((int((1080 - tw) / 2), date_box_y + 8), date_text, fill=(255, 255, 255), font=font_bold_large)

# Bottom Venue Footer
draw.rounded_rectangle([(40, 1740), (1040, 1880)], radius=24, fill=(15, 8, 30, 240), outline=(255, 209, 102, 190), width=2)
v_text1 = "📍 High Tension Road, Chak Karol, Near HP Petrol Pump, Jaipur - 302017"
v_text2 = "📞 PASSES & INQUIRIES: +91 80585 26618  |  AGE GROUP: 16–50"
bbox1 = draw.textbbox((0, 0), v_text1, font=font_bold_sm)
bbox2 = draw.textbbox((0, 0), v_text2, font=font_bold_med)
draw.text((int((1080 - (bbox1[2] - bbox1[0])) / 2), 1762), v_text1, fill=(255, 255, 255), font=font_bold_sm)
draw.text((int((1080 - (bbox2[2] - bbox2[0])) / 2), 1812), v_text2, fill=(255, 209, 102), font=font_bold_med)

poster1 = Image.alpha_composite(bg_story, overlay)
poster1.convert("RGB").save(os.path.join(output_dir, "01_Official_Story_Poster_9x16.jpg"), quality=95)
print("Saved Poster 1 (Story 9:16)")

# -------------------------------------------------------------
# POSTER 2: 1:1 Instagram Feed Banner (1200 x 1200)
# -------------------------------------------------------------
bg_feed = Image.open(os.path.join(assets_dir, "pinkcity_genz_garba_feed.jpg")).convert("RGBA")
bg_feed = bg_feed.resize((1200, 1200), Image.Resampling.LANCZOS)

overlay2 = Image.new("RGBA", (1200, 1200), (0, 0, 0, 0))
draw2 = ImageDraw.Draw(overlay2)

# Top Logo Header
draw2.rounded_rectangle([(430, 25), (770, 135)], radius=18, fill=(255, 255, 255, 245), outline=(255, 0, 127, 200), width=2)
logo_resized2 = logo_raw.resize((220, int(220 * logo_raw.height / logo_raw.width)), Image.Resampling.LANCZOS)
overlay2.paste(logo_resized2, (int((1200 - logo_resized2.width) / 2), 32), logo_resized2)

# Center Typography Card
c_w, c_h = 1040, 390
c_x, c_y = 80, 155
draw2.rounded_rectangle([(c_x, c_y), (c_x + c_w, c_y + c_h)], radius=28, fill=(255, 240, 245, 245), outline=(255, 0, 127, 180), width=3)

# Exact Typography
typo_w2 = 920
typo_h2 = int(typo_w2 * clean_typo.height / clean_typo.width)
typo_resized2 = clean_typo.resize((typo_w2, typo_h2), Image.Resampling.LANCZOS)
overlay2.paste(typo_resized2, (int((1200 - typo_w2) / 2), c_y + 16), typo_resized2)

# Date Ribbon
d_box_y = c_y + typo_h2 + 8
draw2.rounded_rectangle([(c_x + 160, d_box_y), (c_x + c_w - 160, d_box_y + 64)], radius=32, fill=(219, 18, 93, 255))
d_bbox = draw2.textbbox((0, 0), date_text, font=font_bold_large)
draw2.text((int((1200 - (d_bbox[2] - d_bbox[0])) / 2), d_box_y + 6), date_text, fill=(255, 255, 255), font=font_bold_large)

# Bottom Venue Footer
draw2.rounded_rectangle([(50, 1075), (1150, 1175)], radius=20, fill=(15, 8, 30, 240), outline=(255, 209, 102, 190), width=2)
f_text1 = "📍 High Tension Road, Chak Karol, Near HP Petrol Pump, Jaipur - 302017"
f_text2 = "📞 BOOK PASSES: +91 80585 26618  |  AGE: 16–50  |  SOLO FRIENDLY"
fb1 = draw2.textbbox((0, 0), f_text1, font=font_bold_sm)
fb2 = draw2.textbbox((0, 0), f_text2, font=font_bold_sm)
draw2.text((int((1200 - (fb1[2] - fb1[0])) / 2), 1088), f_text1, fill=(255, 255, 255), font=font_bold_sm)
draw2.text((int((1200 - (fb2[2] - fb2[0])) / 2), 1130), f_text2, fill=(255, 209, 102), font=font_bold_sm)

poster2 = Image.alpha_composite(bg_feed, overlay2)
poster2.convert("RGB").save(os.path.join(output_dir, "02_Official_Feed_Banner_1x1.jpg"), quality=95)
print("Saved Poster 2 (Feed 1:1)")

# -------------------------------------------------------------
# POSTER 3: Best Dressed Award Post (1200 x 1200)
# -------------------------------------------------------------
bg_award = Image.open(os.path.join(assets_dir, "genz_garba_award_post_1789017374593.jpg")).convert("RGBA")
bg_award = bg_award.resize((1200, 1200), Image.Resampling.LANCZOS)

overlay3 = Image.new("RGBA", (1200, 1200), (0, 0, 0, 0))
draw3 = ImageDraw.Draw(overlay3)

# Top Logo Header
draw3.rounded_rectangle([(430, 25), (770, 135)], radius=18, fill=(255, 255, 255, 245), outline=(255, 0, 127, 200), width=2)
overlay3.paste(logo_resized2, (int((1200 - logo_resized2.width) / 2), 32), logo_resized2)

# Date & Best Dressed Banner on Top
draw3.rounded_rectangle([(120, 150), (1080, 240)], radius=24, fill=(219, 18, 93, 245), outline=(255, 209, 102, 200), width=2)
aw_text = "🏆 BEST DRESSED AWARDS • 17 - 18 - 19 OCT"
aw_bbox = draw3.textbbox((0, 0), aw_text, font=font_bold_large)
draw3.text((int((1200 - (aw_bbox[2] - aw_bbox[0])) / 2), 166), aw_text, fill=(255, 255, 255), font=font_bold_large)

# Bottom Venue Footer
draw3.rounded_rectangle([(50, 1075), (1150, 1175)], radius=20, fill=(15, 8, 30, 240), outline=(255, 209, 102, 190), width=2)
draw3.text((int((1200 - (fb1[2] - fb1[0])) / 2), 1088), f_text1, fill=(255, 255, 255), font=font_bold_sm)
draw3.text((int((1200 - (fb2[2] - fb2[0])) / 2), 1130), f_text2, fill=(255, 209, 102), font=font_bold_sm)

poster3 = Image.alpha_composite(bg_award, overlay3)
poster3.convert("RGB").save(os.path.join(output_dir, "03_Official_Best_Dressed_Post_1x1.jpg"), quality=95)
print("Saved Poster 3 (Best Dressed Award 1:1)")

# -------------------------------------------------------------
# POSTER 4: Live Band Reel Cover (1080 x 1920)
# -------------------------------------------------------------
bg_reel = Image.open(os.path.join(assets_dir, "genz_garba_live_band_reel_1789017527452.jpg")).convert("RGBA")
bg_reel = bg_reel.resize((1080, 1920), Image.Resampling.LANCZOS)

overlay4 = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw4 = ImageDraw.Draw(overlay4)

# Top Logo Header
draw4.rounded_rectangle([(340, 45), (740, 175)], radius=20, fill=(255, 255, 255, 245), outline=(255, 0, 127, 220), width=2)
overlay4.paste(logo_resized, (logo_x, logo_y), logo_resized)

# Center Typography Card
draw4.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=32, fill=(255, 240, 245, 245), outline=(255, 0, 127, 180), width=3)
overlay4.paste(typo_resized, (typo_x, typo_y), typo_resized)

# Date Banner
draw4.rounded_rectangle([(card_x + 80, date_box_y), (card_x + card_w - 80, date_box_y + 68)], radius=34, fill=(219, 18, 93, 255))
draw4.text((int((1080 - tw) / 2), date_box_y + 8), date_text, fill=(255, 255, 255), font=font_bold_large)

# Live Band Badge
draw4.rounded_rectangle([(120, 715), (960, 795)], radius=25, fill=(255, 209, 102, 240), outline=(255, 0, 127, 200), width=2)
band_text = "🥁 FEAT. LIVE BAND, BOLLYWOOD DJ & DHOL"
band_bbox = draw4.textbbox((0, 0), band_text, font=font_bold_med)
draw4.text((int((1080 - (band_bbox[2] - band_bbox[0])) / 2), 734), band_text, fill=(15, 8, 30), font=font_bold_med)

# Bottom Venue Footer
draw4.rounded_rectangle([(40, 1740), (1040, 1880)], radius=24, fill=(15, 8, 30, 240), outline=(255, 209, 102, 190), width=2)
draw4.text((int((1080 - (bbox1[2] - bbox1[0])) / 2), 1762), v_text1, fill=(255, 255, 255), font=font_bold_sm)
draw4.text((int((1080 - (bbox2[2] - bbox2[0])) / 2), 1812), v_text2, fill=(255, 209, 102), font=font_bold_med)

poster4 = Image.alpha_composite(bg_reel, overlay4)
poster4.convert("RGB").save(os.path.join(output_dir, "04_Official_Live_Band_Reel_9x16.jpg"), quality=95)
print("Saved Poster 4 (Live Band Reel 9:16)")
