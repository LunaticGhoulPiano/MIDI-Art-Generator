import os
import numpy as np
from mido import Message, MetaMessage, MidiFile, MidiTrack
from PIL import Image
from rembg import remove
# import random

GMs = list(range(128)) # list of general midi
midi_offset = 21 # 21 ~ 108: A0 ~ C8

def convert_image(input_path: str, output_path: str, filename: str, threshold: int, rmbg: bool):
    os.makedirs(output_path, exist_ok = True)
    if filename.lower().endswith(".png") or filename.lower().endswith(".jpg"):
        input_file = os.path.join(input_path, filename)
        with Image.open(input_file) as img:
            # (maybe remove background and) grayscale
            if rmbg:
                img = img.convert("RGBA") # add alpha
                no_bg_bytes = remove(img) # remove background
                img = no_bg_bytes.convert("L") # grayscale
            else:
                img = img.convert("L")
            
            # threshold
            arr = np.array(img)
            arr[arr < threshold] = 0
            filtered_img = Image.fromarray(arr.astype(np.uint8))

            # resize
            target_height = 88
            aspect_ratio = filtered_img.width / filtered_img.height
            target_width = int(aspect_ratio * target_height)
            resized_img = filtered_img.resize((target_width, target_height), Image.LANCZOS)

            # save
            resized_img.save(os.path.join(output_path, f"scaled_{filename}"))
            resized_arr = np.array(resized_img)
            np.savetxt(f"{output_path}./{filename[:-4]}_88keys.csv", resized_arr, delimiter = ",", fmt = "%d")
            return True
    else:
        print("No .png or .jpg file")
        return False

def generate_midi(input_path: str, output_path: str, filename: str, rmbg: bool = True, threshold: int = 70,
                  instrument_id: int = 1, tempo: float = 120, pixels_per_beat: int = 1, ticks_per_beat: int = 480):
    # convert image
    if not convert_image(input_path, output_path, filename, threshold, rmbg):
        return
    # read processed image
    with Image.open(os.path.join(output_path, f"scaled_{filename}")) as img:
        arr = np.array(img)
        width = arr.shape[1]
        height = arr.shape[0]
    
    # the original 88keys scaling
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message("program_change", program = instrument_id, time = 0))
    track.append(MetaMessage("set_tempo", tempo = int(60000000 / tempo), time = 0))  # BPM

    time_scale = 1
    prev_x = 0
    for x in range(width):
        delta_time = x - prev_x
        note_on_events = []
        for y in range(height):
            value = arr[height - 1 - y][x]
            if value > 0:
                note = midi_offset + y
                velocity = 80 #int(np.clip(value, 0, 127))
                note_on_events.append((note, velocity))
        for note, velocity in note_on_events:
            track.append(Message("note_on", note = note, velocity = velocity, time = delta_time))
            delta_time = 0
        for note, velocity in note_on_events:
            track.append(Message("note_off", note = note, velocity = velocity, time = time_scale))
        prev_x = x

    midi_out_path_before = os.path.join(output_path, f"{filename[:-4]}_before_scaled.mid")
    mid.save(midi_out_path_before)
    print(f"{midi_out_path_before} saved.")

    # the scaled 88keys
    mid_scaled = MidiFile(ticks_per_beat = ticks_per_beat)
    track_scaled = MidiTrack()
    mid_scaled.tracks.append(track_scaled)
    track_scaled.append(Message("program_change", program = instrument_id, time = 0))
    track_scaled.append(MetaMessage("set_tempo", tempo = int(60000000 / tempo), time = 0))

    ticks_per_pixel = ticks_per_beat // pixels_per_beat  # ex. pixels_per_beat = 4, ticks_per_beat = 480 -> ticks_per_pixel = 120

    for x in range(width):
        delta_time = ticks_per_pixel
        note_on_events = []
        for y in range(height):
            value = arr[height - 1 - y][x]
            if value > 0:
                note = midi_offset + y
                velocity = 80 #int(np.clip(value, 0, 127))
                note_on_events.append((note, velocity))

        # set note events
        for i, (note, velocity) in enumerate(note_on_events):
            track_scaled.append(Message("note_on", note = note, velocity = velocity, time = delta_time if i == 0 else 0))
        for i, (note, velocity) in enumerate(note_on_events):
            track_scaled.append(Message("note_off", note = note, velocity = velocity, time = ticks_per_pixel if i == 0 else 0))

    midi_out_path_after = os.path.join(output_path, f"{filename[:-4]}_after_scaled.mid")
    mid_scaled.save(midi_out_path_after)
    print(f"{midi_out_path_after} saved.")

def convert_all(input_path: str = "./Inputs", output_path: str = "./Outputs"):
    for filename in os.listdir(input_path):
        generate_midi(input_path, output_path, filename)

if __name__ == "__main__":
    #convert_all()
    generate_midi("./Inputs", "./Outputs", "1.png", False)
    generate_midi("./Inputs", "./Outputs", "2.jpg")