import os
import cv2
import subprocess
import numpy as np

folder = "Remove Gemini Icon"

# 1. PROCESS POSTER IMAGE
poster_name = "Garba_party_invitation_poster_2K_20260910211149.jpeg"
poster_path = os.path.join(folder, poster_name)

if os.path.exists(poster_path):
    print(f"--- Cleaning Poster Image: {poster_name} ---")
    img = cv2.imread(poster_path)
    h, w = img.shape[:2]
    
    # Inpaint Top-Left corner (Star is at x=59, y=67)
    tl_mask = np.zeros((160, 160), dtype=np.uint8)
    cv2.circle(tl_mask, (59, 67), 40, 255, -1)
    img[0:160, 0:160] = cv2.inpaint(img[0:160, 0:160], tl_mask, 5, cv2.INPAINT_TELEA)
    
    # Also inpaint Bottom-Right corner just in case
    br_mask = np.zeros((160, 160), dtype=np.uint8)
    cv2.circle(br_mask, (80, 80), 45, 255, -1)
    img[h-160:h, w-160:w] = cv2.inpaint(img[h-160:h, w-160:w], br_mask, 5, cv2.INPAINT_TELEA)
    
    cv2.imwrite(poster_path, img, [cv2.IMWRITE_JPEG_QUALITY, 98])
    clean_poster_path = os.path.join(folder, "Garba_party_invitation_poster_2K_20260910211149_clean.jpeg")
    cv2.imwrite(clean_poster_path, img, [cv2.IMWRITE_JPEG_QUALITY, 98])
    print("[SUCCESS] Poster top-left and bottom-right watermarks removed!")

# 2. PROCESS ALL 4 VIDEOS
videos = [
    "Gen_Z_Garba_Party_Promo_20260910210708.mp4",
    "Gen_Z_Garba_Party_Promo_20260910210928.mp4",
    "Gen_Z_Garba_Party_finale_20260910210809.mp4",
    "Gen_Z_Garba_Party_promo_20260910211049.mp4"
]

# Mask for 1920x1080 video:
# Top-Left watermark is centered at x=38, y=51
tl_w, tl_h = 100, 110
tl_video_mask = np.zeros((tl_h, tl_w), dtype=np.uint8)
cv2.circle(tl_video_mask, (38, 51), 32, 255, -1)

# Bottom-Right watermark mask just in case
br_w, br_h = 120, 120
br_video_mask = np.zeros((br_h, br_w), dtype=np.uint8)
cv2.circle(br_video_mask, (60, 60), 36, 255, -1)

for v in videos:
    v_path = os.path.join(folder, v)
    if not os.path.exists(v_path):
        continue
        
    print(f"\n--- Cleaning Video: {v} ---")
    cap = cv2.VideoCapture(v_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    temp_video = os.path.join(folder, f"temp_{v}")
    clean_video = os.path.join(folder, f"{os.path.splitext(v)[0]}_clean.mp4")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 1. Inpaint TOP-LEFT watermark (the actual Gemini star icon!)
        tl_patch = frame[0:tl_h, 0:tl_w]
        frame[0:tl_h, 0:tl_w] = cv2.inpaint(tl_patch, tl_video_mask, 5, cv2.INPAINT_TELEA)
        
        # 2. Inpaint BOTTOM-RIGHT watermark
        br_patch = frame[height-br_h:height, width-br_w:width]
        frame[height-br_h:height, width-br_w:width] = cv2.inpaint(br_patch, br_video_mask, 5, cv2.INPAINT_TELEA)
        
        out.write(frame)
        frame_idx += 1
        if frame_idx % 60 == 0:
            print(f"  Progress: {frame_idx}/{total_frames} frames ({(frame_idx/total_frames)*100:.0f}%)")
            
    cap.release()
    out.release()
    
    # Re-encode with original audio
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", v_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0?",
        "-shortest",
        clean_video
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_video):
        os.remove(temp_video)
        
    # Overwrite original video with clean version
    clean_bytes = open(clean_video, "rb").read()
    with open(v_path, "wb") as f_orig:
        f_orig.write(clean_bytes)
        
    print(f"[SUCCESS] Cleaned {v} successfully!")

print("\n[ALL COMPLETE] All Top-Left & Bottom-Right Gemini Watermarks Permanently Removed!")
