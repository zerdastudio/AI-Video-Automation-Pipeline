# AI Video Automation Pipeline

An automated programmatic architecture that eliminates manual video editing bottlenecks. This system integrates OpenAI's Whisper model, Python processing, and FFmpeg to execute tasks that traditionally require hours of manual work in seconds.

## System Architecture
* **Transcription & Timestamping:** Utilizes local Whisper AI to map exact audio timestamps.
* **Psychological Color Mapping:** A Python script applies Regex to map specific HEX color codes to high-retention trigger words.
* **Master Burn-in:** Executes a programmatic FFmpeg render to hardcode dynamic subtitles with drop-shadows and formatting without ever opening a traditional NLE (Non-Linear Editor).

Built to reduce human involvement and scale video operations.
