"""
clip_indexer_allphasesUpdated.py - Master orchestration script.

Executes the entire 5-phase clip indexing pipeline on single or batch episodes:
  Phase 1: scene_splitter.py
  Phase 2: clip_indexer_subtitles.py
  Phase 3: clip_indexer_embed.py
  Phase 4: clip_indexer_yolo.py
  Phase 5: episode_indexer.py
"""

import argparse
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("allphases_updated")

def run_cmd(cmd_list, description):
    log.info("=" * 60)
    log.info(f"PHASE: {description}")
    log.info("=" * 60)
    log.info(f"Running: {' '.join(cmd_list)}")
    
    try:
        result = subprocess.run(cmd_list, check=True)
        log.info(f"✓ {description} complete.")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"❌ {description} failed with exit code {e.returncode}.")
        return False

def run_single_episode(episode_path: Path, show_slug: str, yolo_weights: str, threshold: float = 27.0):
    """Run all 5 phases on a single episode."""
    if not episode_path.exists():
        log.error(f"Episode file not found: {episode_path}")
        return False
        
    # Assume SRT is exactly the same name but with .srt extension
    srt_path = episode_path.with_suffix(".srt")
    if not srt_path.exists():
        log.error(f"Subtitle file not found: {srt_path} (Expected exact match to mp4)")
        return False
        
    prefix = episode_path.stem
    manifest_path = f"clips/{prefix}_manifest.json"
    
    log.info(f"\n🚀 Starting Full Pipeline for: {prefix}\n")

    # Phase 1: Scene Splitter
    cmd1 = [sys.executable, "scripts/scene_splitter.py", str(episode_path), "--output", "clips", "--prefix", prefix, "--threshold", str(threshold)]
    if not run_cmd(cmd1, "Scene Splitting"): return False

    # Phase 2: Subtitle Indexer
    cmd2 = [sys.executable, "scripts/clip_indexer_subtitles.py", "--manifest", manifest_path, "--srt", str(srt_path), "--show", show_slug]
    if not run_cmd(cmd2, "Subtitle Indexing"): return False

    # Phase 3: Semantic Embeddings
    cmd3 = [sys.executable, "scripts/clip_indexer_embed.py", "--index", "clip_index.json"]
    if not run_cmd(cmd3, "Semantic Embeddings"): return False

    # Phase 4: YOLO Tagging
    # Note: --target-dir ensures we only run YOLO on this specific episode to save time
    cmd4 = [sys.executable, "scripts/clip_indexer_yolo.py", "--weights", yolo_weights, "--index", "clip_index.json", "--target-dir", prefix]
    if not run_cmd(cmd4, "YOLO Visual Tagging"): return False

    # Phase 5: Episode Summary
    # episode_indexer.py expects paths relative to the subtitles dir or absolute paths for --single
    # Passing the absolute path ensures it works securely
    cmd5 = [sys.executable, "scripts/episode_indexer.py", "--single", str(srt_path.absolute())]
    if not run_cmd(cmd5, "Episode Summary Extraction"): return False

    log.info(f"\n🎉 ALL 5 PHASES COMPLETE FOR {prefix}!\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Master orchestration script to run all 5 phases of clip indexing.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--episode", type=str, help="Path to a single episode video (e.g. episodes/s1e1.mp4)")
    group.add_argument("--batch", type=str, help="Path to a directory containing multiple .mp4 episodes")
    
    parser.add_argument("--show", type=str, required=True, help="Show slug (e.g. rick_and_morty)")
    parser.add_argument("--yolo-weights", type=str, default="yolo_wt/20epochs.pt", help="Path to YOLO weights")
    parser.add_argument("--threshold", type=float, default=27.0, help="Scene change sensitivity (default: 27.0)")
    
    args = parser.parse_args()
    
    if args.episode:
        run_single_episode(Path(args.episode), args.show, args.yolo_weights, args.threshold)
        
    elif args.batch:
        batch_dir = Path(args.batch)
        if not batch_dir.exists() or not batch_dir.is_dir():
            log.error(f"Batch directory not found: {batch_dir}")
            sys.exit(1)
            
        videos = list(batch_dir.glob("*.mp4"))
        videos.extend(batch_dir.glob("*.mkv"))
        
        if not videos:
            log.warning(f"No video files (.mp4, .mkv) found in {batch_dir}")
            sys.exit(0)
            
        log.info(f"Found {len(videos)} episodes in batch directory. Starting batch process...")
        success_count = 0
        
        for video_path in sorted(videos):
            if run_single_episode(video_path, args.show, args.yolo_weights, args.threshold):
                success_count += 1
                
        log.info(f"Batch complete. {success_count}/{len(videos)} episodes processed successfully.")

if __name__ == "__main__":
    main()
