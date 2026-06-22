<div align="center">
  <h1>🎬 YT Automation AI Pipeline</h1>
  <p>An end-to-end AI-powered orchestration pipeline that autonomously slices long-form TV episodes into highly engaging, context-aware short-form content for YouTube Shorts, TikTok, and Instagram Reels.</p>
</div>

---

## 🌟 Overview

This project is a fully automated content factory. It doesn't just cut random clips; it actually "watches" and "reads" the episodes to build a highly intelligent, searchable video database. When given a topic, the AI writes a viral script, generates an AI voiceover, searches the database for visually and contextually perfect video clips, and stitches it all together into a polished final video.

## ✨ Key Features

- **🎞️ Intelligent Scene Splitting:** Uses advanced heuristics and `ffmpeg` to automatically slice full-length episodes into hundreds of perfectly timed micro-clips without cutting off mid-scene.
- **📝 Subtitle Context Mapping:** Maps official `.srt` subtitle dialogue directly to specific clips, allowing the AI to understand exactly what is being said in every video file.
- **👁️ Local Vision AI Tagging:** Uses local Vision-Language Models (like Ollama/LLaVA) to physically "watch" the center frame of every clip and automatically tag the characters, actions, and locations.
- **🧠 Lore-Accurate Script Generation:** Feeds deep lore and show context into an LLM (Llama 3.1) to generate engaging, viral-ready scripts on any given topic.
- **🎙️ Flexible TTS Engine:** Supports local GPU-accelerated Text-to-Speech models, Google Colab offloading, and ElevenLabs API integration for premium voice acting.
- **🤖 Autonomous Orchestrator:** The mastermind script that coordinates the LLM, the TTS engine, the intelligent Clip Matcher, and MoviePy to render the final `.mp4`.

## ⚙️ The 3-Step Ingestion Pipeline

Before generating videos, raw episodes must be ingested into the AI's brain (`clip_index.json`). 

### 1. Split the Episode
Chops the raw `.mp4` into hundreds of bite-sized scenes.
```bash
python scripts/scene_splitter_local.py "clips/show_name/episode.mp4" --output "clips/show_name/split_clips" --prefix "s1e1"
```

### 2. Index Subtitles
Embeds the dialogue from an `.srt` file into the clip database.
```bash
python scripts/clip_indexer_subtitles.py --manifest "clips/show_name/split_clips/s1e1_manifest.json" --srt "clips/show_name/subtitles.srt" --show show_name
```

### 3. Vision Auto-Tagging
Wakes up the local Vision AI to visually tag all new clips with characters and actions.
```bash
python scripts/clip_indexer_vision.py --clips-dir "clips/show_name/split_clips"
```

## 🚀 Generating a Video

Once your clip library is indexed, creating a video takes a single command:
```bash
python scripts/orchestrator_noImage_gpuVoice.py --topic "Why Rick Hates Time Travel"
```
The pipeline will automatically generate the script, synthesize the voiceover, retrieve the most relevant clips, and render the final masterpiece to the `output/` folder!

## 🛠️ Tech Stack
- **AI Models:** Ollama (Llama 3.1, LLaVA)
- **Video Processing:** `moviepy` (v2), `ffmpeg`, OpenCV
- **Audio/TTS:** Piper TTS, ElevenLabs, XTTS
- **Environment:** Python 3.10+, PowerShell / Bash
