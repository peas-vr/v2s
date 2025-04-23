import os
import cv2
import shutil
from PIL import Image

input_exts = ('.gif', '.mp4', '.avi', '.mov', '.mkv')
output_dir = 'spritesheets'
originals_dir = 'originals'

def process_input(input_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.gif':
        return extract_gif_frames(input_path)
    elif ext in input_exts:
        return extract_video_frames(input_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def transparent_frame(size):
    return Image.new('RGBA', size, (0, 0, 0, 0))

def extract_gif_frames(input_path):
    with Image.open(input_path) as im:
        frames = []
        durations = []
        try:
            while True:
                frames.append(im.copy().convert('RGBA'))
                duration = max(1, im.info.get('duration', 100))
                durations.append(duration)
                im.seek(len(frames))
        except EOFError:
            pass
        return frames, durations

def extract_video_frames(input_path):
    cap = cv2.VideoCapture(input_path)
    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_duration = 1000 / fps  # Duration in ms per frame
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(rgb_frame).convert('RGBA')
        frames.append(pil_frame)
    
    cap.release()
    durations = [frame_duration] * len(frames)
    return frames, durations

def downsample_frames_and_durations(frames, durations):
    while len(frames) > 64:
        new_frames = frames[::2]
        new_durations = []
        
        for i in range(0, len(durations), 2):
            if i+1 < len(durations):
                new_durations.append(durations[i] + durations[i+1])
            else:
                new_durations.append(durations[i])
        
        frames, durations = new_frames, new_durations
    
    return frames[:64], durations[:64]

def calculate_fps(durations):
    total_duration = sum(durations)
    if total_duration == 0:
        return 24
    
    avg_duration = total_duration / len(durations)
    fps = 1000 / avg_duration
    return max(1, min(round(fps), 64))

def generate_spritesheet(frames, output_path, fps):
    # Create VRChat-compatible sprite sheet
    actual_frames = len(frames)
    grid_size = 8
    frame_size = 128

    sprite_sheet = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    
    for i in range(64):
        x = (i % grid_size) * frame_size
        y = (i // grid_size) * frame_size
        
        if i < actual_frames:
            frame = frames[i].resize((frame_size, frame_size), Image.Resampling.LANCZOS)
        else:
            frame = transparent_frame((frame_size, frame_size))
        
        sprite_sheet.paste(frame, (x, y))

    sprite_sheet.save(output_path, 'PNG')

def unique_filename(path):
    counter = 1
    base, ext = os.path.splitext(path)
    while os.path.exists(path):
        path = f"{base}({counter}){ext}"
        counter += 1
    return path

def process_all_files():
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(originals_dir, exist_ok=True)
    
    files = [f for f in os.listdir() if os.path.splitext(f)[1].lower() in input_exts]
    
    if not files:
        print("No supported files found in current directory")
        return
    
    processed = 0
    for filename in files:
        try:
            frames, durations = process_input(filename)
            processed_frames, processed_durations = downsample_frames_and_durations(frames, durations)
            fps = calculate_fps(processed_durations)
            
            base_name = os.path.splitext(filename)[0]
            output_filename = f"{base_name}_{len(processed_frames)}frames_{fps}fps.png"
            output_path = os.path.join(output_dir, output_filename)
            
            generate_spritesheet(processed_frames, output_path, fps)
            
            original_path = unique_filename(os.path.join(originals_dir, filename))
            shutil.move(filename, original_path)
            
            print(f"Successfully processed: {filename}")
            processed += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    print(f"\nSuccessfully processed {processed}/{len(files)} files")

if __name__ == "__main__":
    process_all_files()