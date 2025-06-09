# MIDI-Art-Generator
Generate MIDI art by inputing prompts.

## Description
- 本repo是生成式AI基礎與應用課程的期末project，目的為透過使用者prompt產生圖像後，將圖像轉換為MIDI art。
- 由於課程要求需要有資料集，並且MIDI art在線條愈明顯時愈易於辨識，因此使用幾何圖型的資料集進行訓練。
- 應使用[此LoRA訓練教學](https://techtactician.com/how-to-train-stable-diffusion-lora-models/)，並且由於BLIP需要每一個圖像都有對應的描述文本，因此[此RGB幾何圖形資料集](https://www.kaggle.com/datasets/dineshpiyasamara/geometric-shapes-dataset)與[此黑白幾何圖形資料集](https://www.kaggle.com/datasets/shuvokumarbasak4004/geometric-shapes-new-and-update-dataset)中，每個圖像都應該有一個對應的txt，此txt的描述文字應為```This is a {圖形名稱，使用所在資料夾之名稱}.```。
- 如果時間太趕就先跑黑白的，時間夠就看是要兩個字訓練或是混合訓練。
[動畫截圖資料集](https://www.kaggle.com/datasets/diraizel/anime-images-dataset
)如果自己想跑再玩就好。
- 訓練完成後，應有一個簡易的互動腳本讀取使用者的輸入，先僅限英文，並且訓練完的模型要根據prompt產生圖案，例如***Generate a tentacle-like geometric fractal***（生成一個像觸手的碎形圖）。當然prompt可以是各種圖像，但因為使用的資料集，prompt先以生成幾何圖形藝術為主。
- 生成完畢後，應使用二值化轉換圖像為布林值，若有RGB亦可轉換成RGB值。
最後生成MIDI，使用者應可決定軌道數量、時值，轉換時先以圖像的寬度為最大時間軸長度，再根據預設或輸入的軌道數量及所選樂器（參見[GM音色](https://radio.cvgm.net/demovibes/platform/48/)）產生MIDI檔案。最終呈現使用[MIDIFall](https://github.com/Gawehold/MIDIFall)進行視覺化，demo時應預先渲染輸出好mp4檔案。

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
- Black-and-White geometric shapes: https://www.kaggle.com/datasets/shuvokumarbasak4004/geometric-shapes-new-and-update-dataset
- RGB geometric shapes: https://www.kaggle.com/datasets/dineshpiyasamara/geometric-shapes-dataset
- Anime screenshots: https://www.kaggle.com/datasets/diraizel/anime-images-dataset

## TODO
- Train
- Implementation

## Tools
- MIDI-Visualizer: https://github.com/Gawehold/MIDIFall