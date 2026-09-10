import os
import cv2
import subprocess
import numpy as np

folder = "Remove Gemini Icon"

# 1. PROCESS POSTER IMAGE
poster_name = "Garba_party_invitation_poster_2K_20260910211149.jpeg"
poster_path = os.path.join(folder, poster_name)

if os.path.exists(poster_path):
    print(f"--- Processing Image: {poster_name} ---")
    img = cv2.imread(poster_path)
    h, w = img.shape[:2]
    
    # Bottom right corner patch (140x140)
    p_x1, p_y1 = w - 140, h - 140
    p_x2, p_y2 = w, h
    patch = img[p_y1:p_y2, p_x1:p_x2]
    
    # Create mask for the star (center ~ (1455, 2671))
    star_x = 1455 - p_x1
    star_y = 2671 - p_y1
    
    patch_mask = np.zeros((140, 140), dtype=np.uint8)
    cv2.circle(patch_mask, (star_x, star_y), 45, 255, -1)
    
    # Inpaint patch
    clean_patch = cv2.inpaint(patch, patch_mask, 5, cv2.INPAINT_TELEA)
    img[p_y1:p_y2, p_x1:p_x2] = clean_patch
    
    # Save clean image
    clean_poster_path = os.path.join(folder, "Garba_party_invitation_poster_2K_20260910211149_clean.jpeg")
    cv2.imwrite(clean_poster_path, img, [cv2.IMWRITE_JPEG_QUALITY, 98])
    # Overwrite the original file
    cv2.imwrite(poster_path, img, [cv2.IMWRITE_JPEG_QUALITY, 98])
    print("[SUCCESS] Poster image cleaned successfully!")

# 2. PROCESS ALL VIDEOS
videos = [f for f in os.listdir(folder) if f.lower().endswith('.mp4') and not f.endswith('_clean.mp4') and not f.startswith('temp_')]

for v in videos:
    v_path = os.path.join(folder, v)
    print(f"\n--- Processing Video: {v} ---")
    
    cap = cv2.VideoCapture(v_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    temp_video = os.path.join(folder, f"temp_{v}")
    clean_video = os.path.join(folder, f"{os.path.splitext(v)[0]}_clean.mp4")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
    
    # Video watermark patch around bottom-right (1850, 1025)
    p_w, p_h = 130, 130
    p_x1, p_y1 = width - p_w, height - p_h
    p_x2, p_y2 = width, height
    
    star_x = 1851 - p_x1
    star_y = 1023 - p_y1
    
    patch_mask = np.zeros((p_h, p_w), dtype=np.uint8)
    cv2.circle(patch_mask, (star_x, star_y), 44, 255, -1)
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Inpaint corner patch
        patch = frame[p_y1:p_y2, p_x1:p_x2]
        clean_patch = cv2.inpaint(patch, patch_mask, 5, cv2.INPAINT_TELEA)
        frame[p_y1:p_y2, p_x1:p_x2] = clean_patch
        out.write(frame)
        frame_idx += 1
        if frame_idx % 60 == 0:
            print(f"  Progress: {frame_idx}/{total_frames} frames ({(frame_idx/total_frames)*100:.0f}%)")
    
    cap.release()
    out.release()
    
    # Re-encode with ffmpeg to preserve original audio & high quality H.264
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
    
    # Also overwrite the original video file with the clean version
    clean_v_bytes = open(clean_video, "rb").read()
    with open(v_path, "wb") as f_orig:
        f_orig.write(clean_v_bytes)
        
    print(f"[SUCCESS] Video {v} cleaned and updated successfully!")

print("\n[ALL COMPLETE] ALL IMAGES AND VIDEOS IN 'Remove Gemini Icon' CLEANED SUCCESSFULLY!")
