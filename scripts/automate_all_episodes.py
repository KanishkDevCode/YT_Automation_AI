import os
import sys
import subprocess
from pathlib import Path

def main():
    season_dir = Path("clips/rick_and_morty/S8")
    show_name = "rick_and_morty"
    
    if not season_dir.exists():
        print(f"Error: Directory {season_dir} does not exist.")
        sys.exit(1)

    print("=" * 60)
    print("🚀 STARTING AUTOMATED S8 BATCH PROCESSING")
    print("   - This will process all episodes in S8.")
    print("   - It will SKIP splitting if the scenes are already cut.")
    print("   - It will run the Vision model (Phase 3) for all episodes.")
    print("=" * 60)

    # Sort episodes properly (E1, E2, ... E10) instead of alphabetically
    episodes = []
    for ep_folder in season_dir.iterdir():
        if ep_folder.is_dir() and ep_folder.name.startswith("E"):
            try:
                ep_num = int(ep_folder.name[1:])
                episodes.append((ep_num, ep_folder))
            except ValueError:
                pass
    
    episodes.sort()

    for ep_num, ep_folder in episodes:
        prefix = f"s8e{ep_num}"
        print(f"\n\n{'='*60}")
        print(f"🎬 PROCESSING EPISODE: {prefix.upper()} ({ep_folder})")
        print(f"{'='*60}")

        # Find subtitle file (.srt)
        srt_files = list(ep_folder.glob("*.srt"))
        if not srt_files:
            print(f"❌ Skipping {prefix}: No .srt subtitle file found in {ep_folder}")
            continue
        srt_path = srt_files[0]

        # Find the output folder for clips
        output_dir = ep_folder / "split_clips"
        manifest_path = output_dir / f"{prefix}_manifest.json"

        # Build the command base
        cmd = [
            sys.executable, "scripts/clip_indexer_allphase.py",
            "--srt", str(srt_path),
            "--show", show_name,
            "--prefix", prefix,
            "--output", str(output_dir)
        ]

        # Check if it's already split
        if manifest_path.exists():
            print(f"✅ Found existing manifest for {prefix}! Skipping Scene Splitting phase.")
            cmd.extend(["--manifest", str(manifest_path)])
        else:
            # We need the video file to split it
            video_files = list(ep_folder.glob("*.mkv")) + list(ep_folder.glob("*.mp4"))
            if not video_files:
                print(f"❌ Skipping {prefix}: No video file (.mkv or .mp4) and no manifest found in {ep_folder}")
                continue
            video_path = video_files[0]
            
            print(f"🔍 No manifest found for {prefix}. Starting FULL pipeline (Splitting -> Subtitles -> Vision).")
            cmd.extend(["--episode", str(video_path)])

        # NOTE: We are NOT using --skip-vision, so Phase 3 will run!
        print(f"\n▶ Executing: {' '.join(cmd)}\n")
        
        try:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"\n❌ Script failed for {prefix}. Skipping to next episode.")
            else:
                print(f"\n🎉 Successfully finished all phases for {prefix}!")
        except KeyboardInterrupt:
            print("\n⚠️ Batch processing interrupted by user.")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error processing {prefix}: {e}")

    print("\n\n🏁 BATCH PROCESSING COMPLETE!")

if __name__ == "__main__":
    main()
