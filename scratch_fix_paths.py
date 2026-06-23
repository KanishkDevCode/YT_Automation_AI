import json
from pathlib import Path

def main():
    index_path = Path("clip_index.json")
    if not index_path.exists():
        print("clip_index.json not found")
        return
        
    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    clips_dir = Path("clips")
    updated = 0
    
    for clip in data.get("clips", []):
        filename = clip.get("filename")
        if filename:
            # find the actual file dynamically
            found = list(clips_dir.rglob(filename))
            if found:
                actual_path = str(found[0])
                # Only update if different (normpath handles slash differences loosely, but let's just assign)
                if clip.get("filepath") != actual_path:
                    clip["filepath"] = actual_path
                    updated += 1
                    
    if updated > 0:
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Updated {updated} filepaths in clip_index.json to point to new nested folders.")
    else:
        print("Everything is already up to date.")

if __name__ == "__main__":
    main()
