"""
tts_xtts_local.py — Phase 2: Local Voice Cloning using XTTS-v2
=========================================================================
Converts script text files to .wav audio using local Coqui TTS Voice Cloning.

Usage:
    Imported dynamically by orchestrator_VoiceLocal.py
"""

import os
import sys
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config_loader import setup_logging

log = setup_logging("tts_xtts_local")

_GLOBAL_TTS = None

def get_tts_model(model_name: str):
    """Singleton pattern to load the massive XTTS model only once."""
    global _GLOBAL_TTS
    if _GLOBAL_TTS is None:
        log.info("Loading XTTS Voice Cloning model into GPU... (This may take a moment)")
        import torch
        from TTS.api import TTS
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        log.info("XTTS using device: %s", device)
        
        _GLOBAL_TTS = TTS(model_name)
        _GLOBAL_TTS.to(device)
        log.info("XTTS Model successfully loaded!")
        
    return _GLOBAL_TTS

def synthesize_file_xtts(
    text_path: Path,
    output_path: Path,
    model_name: str,
    reference_audio: str,
    language: str,
) -> bool:
    """
    Synthesize a single text file to .wav using XTTS voice cloning.

    Returns True on success, False on failure.
    """
    text = text_path.read_text(encoding="utf-8").strip()
    if not text:
        log.warning("Skipping empty file: %s", text_path.name)
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)

    log.info("Cloning voice for: %s → %s", text_path.name, output_path.name)
    
    try:
        tts = get_tts_model(model_name)
        
        if reference_audio and Path(reference_audio).exists():
            log.info("Using reference audio: %s", reference_audio)
            tts.tts_to_file(
                text=text, 
                file_path=str(output_path), 
                speaker_wav=reference_audio, 
                language=language
            )
        else:
            log.warning("No reference audio provided! Falling back to default XTTS voice.")
            tts.tts_to_file(
                text=text, 
                file_path=str(output_path), 
                language=language
            )

        if output_path.exists() and output_path.stat().st_size > 0:
            size_kb = output_path.stat().st_size / 1024
            log.info("  ✓ Generated %s (%.1f KB)", output_path.name, size_kb)
            return True
        else:
            log.error("  ✗ Output file missing or empty: %s", output_path)
            return False

    except Exception as e:
        log.error("XTTS synthesis failed for %s: %s", text_path.name, str(e))
        return False
