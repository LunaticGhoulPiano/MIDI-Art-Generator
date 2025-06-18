# MIDI-Art-Generator
Generate MIDI art by inputing prompts.

## Description
- 本repo是生成式AI基礎與應用課程的期末project，目的為透過使用者prompt產生圖像後，將圖像轉換為MIDI art。

## Work Flow
```
--------------                     -------------------  -----------------  -------------------
| Initialize |-User-given prompt->| Image generation |->| RGB/Grayscale |->| MIDI-generation |
--------------                     -------------------  -----------------  -------------------
```

## References
- Train own diffusion model: https://techtactician.com/how-to-train-stable-diffusion-lora-models/
- Text-to-Image: https://github.com/paarthneekhara/text-to-image
- Image-to-ASCII: https://github.com/vietnh1009/ASCII-generator

## Datasets
- Self-labeled dataset: [MIDI_Art](https://huggingface.co/datasets/LunaticGhoulPiano/MIDI_Art)

## TODO
- Train
- Implementation

## Tools
- MIDI-Visualizer: https://github.com/Gawehold/MIDIFall