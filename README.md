<div align="center">
  <img src="assets/readme_banner.png" alt="Automated YouTube Shorts AI Pipeline" width="100%">

  # 🤖 Automated YouTube Shorts AI Pipeline
  
  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)](#)
  [![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?logo=pytorch&logoColor=white)](#)
  [![FFmpeg](https://img.shields.io/badge/FFmpeg-Hardware_Accelerated-007808.svg?logo=ffmpeg&logoColor=white)](#)
  [![YOLOv8](https://img.shields.io/badge/YOLOv8-Computer_Vision-00FFFF.svg?logo=ultralytics&logoColor=black)](#)
  [![Status](https://img.shields.io/badge/Status-Active-success.svg)](#)

  **A fully automated, AI-driven pipeline that converts long-form video episodes into highly engaging, auto-captioned, and character-tagged YouTube Shorts.**
</div>

---

## 🌟 Overview

This repository houses an advanced video automation pipeline designed to curate and render short-form content at scale. By leveraging computer vision and natural language processing, the system intelligently identifies scenes, extracts dialogue, semantically maps conversations, and spatially tags characters on screen—all before rendering the final hardware-accelerated video.

### 🧠 Core Capabilities
- **Intelligent Scene Splitting:** Uses `PySceneDetect` to losslessly cut full-length episodes into hundreds of perfect, context-aware micro-clips.
- **Dialogue Extraction:** Maps `.srt` subtitle files directly to generated clips to capture exact conversational context.
- **Semantic Vibe-Search:** Uses Hugging Face's `clip-ViT` models to create dense vector embeddings of every scene, allowing you to search your video database by "vibe" or specific topics.
- **Character Recognition:** Employs a custom-trained **YOLOv8** model to automatically tag which characters (e.g., Rick, Morty, Summer) are actively present in any given scene.
- **Hardware-Accelerated Rendering:** Powered by FFmpeg with NVIDIA NVENC support (`h264_nvenc`) to assemble and render 1080p Shorts natively on the GPU in seconds.

---

## 🛠️ Pipeline Architecture

The pipeline processes raw video through a sequence of 4 specialized indexing scripts, followed by a rendering orchestrator.

```mermaid
graph TD;
    classDef raw fill:#1E293B,stroke:#475569,stroke-width:2px,color:#F8FAFC,rx:5px,ry:5px;
    classDef process fill:#0284C7,stroke:#0369A1,stroke-width:2px,color:#F8FAFC,rx:5px,ry:5px;
    classDef nlp fill:#7C3AED,stroke:#6D28D9,stroke-width:2px,color:#F8FAFC,rx:5px,ry:5px;
    classDef vision fill:#059669,stroke:#047857,stroke-width:2px,color:#F8FAFC,rx:5px,ry:5px;
    classDef db fill:#D97706,stroke:#B45309,stroke-width:2px,color:#F8FAFC,rx:15px,ry:15px;
    classDef render fill:#DC2626,stroke:#B91C1C,stroke-width:2px,color:#F8FAFC,rx:5px,ry:5px;
    classDef final fill:#000000,stroke:#EF4444,stroke-width:3px,color:#FFFFFF,rx:5px,ry:5px;

    A[Raw .mkv Episode]:::raw --> B[1. Scene Splitter]:::process
    B -->|Generates 400+ Clips| C[2. Subtitle Indexer]:::process
    C -->|Extracts Text| D[3. Embeddings Indexer]:::nlp
    D -->|Semantic Search Space| E[4. YOLO Vision Tagger]:::vision
    E -->|Updates Database| F[(clip_index.json)]:::db
    
    F --> G[Video Assembler & Orchestrator]:::render
    G -->|NVENC Hardware Rendering| H[🎬 Final YouTube Short]:::final
```

---

## 🚀 Usage Guide

To process a new episode, activate your virtual environment and run the pipeline sequence below:

### Step 1: Chop the Episode into Scenes
Cuts the main video into individual scene clips based on camera cuts.
```powershell
.\venv\Scripts\python scripts/scene_splitter.py "clips/rick_and_morty/Episode/episode.mkv" --output "clips/rick_and_morty/" --prefix "s5e6"
```
*(The script will automatically cluster the output into a tidy `split_clips` folder inside your Episode directory!)*

### Step 2: Auto-Tag Subtitles
Cross-references the generated video clips with the master subtitle file to perfectly extract dialogue into `clip_index.json`.
```powershell
.\venv\Scripts\python scripts/clip_indexer_subtitles.py --manifest "clips/rick_and_morty/Episode/split_clips/manifest.json" --srt "subtitles/episode.srt" --show "rick_and_morty"
```

### Step 3: Generate Semantic Embeddings
Runs the NLP model to vectorize all extracted text, enabling AI-powered semantic search. *(Note: Force PyTorch to CPU if your RTX 5060 hits architecture limits).*
```powershell
$env:CUDA_VISIBLE_DEVICES="-1"
.\venv\Scripts\python scripts/clip_indexer_embed.py
```

### Step 4: YOLO Vision Tagging
Runs the YOLOv8 computer vision model to scan every frame of the clips and tag the characters present.
```powershell
.\venv\Scripts\python scripts/clip_indexer_yolo.py --weights yolo_wt/20epochs.pt
$env:CUDA_VISIBLE_DEVICES=""
```

---

## ⚙️ Hardware Requirements
- **OS:** Windows 11
- **GPU:** NVIDIA RTX 5060 (or better) with up-to-date Game Ready or Studio Drivers.
- **Dependencies:** FFmpeg must be installed and added to the System PATH with `h264_nvenc` support.

---
<div align="center">
<i>Built with ☕ and ❤️ for Automated Content Creation.</i>
</div>
