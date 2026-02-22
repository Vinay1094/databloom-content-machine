# Databloom AI Content Pipeline

> A 100% free, local, open-source pipeline that converts a text idea into a fully rendered, voiced, and edited video reel.

This engine chains together local LLMs (Ollama + Llama-3), local TTS (Kokoro), and local Image/Video generation (FLUX.1 + Wan2.2 via ComfyUI) using Python — **zero subscription fees, full creative ownership.**

---

## Architecture

```
Your Idea
    |
    v
[LLM Agent] Ollama + Llama-3  -->  Voiceover Script + Visual Prompts (JSON)
    |
    +---> [TTS Engine] Kokoro TTS  -->  voiceover.wav
    |
    +---> [ComfyUI Studio] FLUX.1 (Image) --> Wan2.2 (Video)  -->  clip_1.mp4 ... clip_N.mp4
    |
    v
[FFmpeg Stitcher]  -->  final_reel.mp4
```

---

## Tech Stack

| Component | Tool |
|---|---|
| Orchestration | Python (this repo) |
| LLM / Scripting | Ollama + Llama-3 (local) |
| Text-to-Speech | Kokoro TTS (82M, local) |
| Image Generation | FLUX.1 Schnell via ComfyUI |
| Video Generation | Wan2.2 I2V via ComfyUI |
| Video Assembly | FFmpeg |
| Containerization | Docker + docker-compose |
| CI/CD | GitHub Actions + GCP |

---

## Prerequisites

- **OS:** Windows, Linux, or macOS
- **Hardware:** NVIDIA GPU with 16GB+ VRAM, or Apple Silicon with 32GB+ Unified Memory
- **Software:**
  - [Python 3.10+](https://www.python.org/)
  - [FFmpeg](https://ffmpeg.org/download.html) (installed and added to system PATH)
  - [Ollama](https://ollama.com/)
  - [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

---

## Project Structure

```
databloom-content-machine/
├── .gitignore
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── comfy_client.py
│   ├── llm_agent.py
│   └── tts_engine.py
├── utils/
│   ├── __init__.py
│   └── video_stitcher.py
└── workflows/
    └── api_workflow.json
```

---

## Setup Instructions

### 1. Clone the repository & install dependencies

```bash
git clone https://github.com/Vinay1094/databloom-content-machine.git
cd databloom-content-machine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the LLM Server

```bash
ollama pull llama3
```

### 3. Configure the Visual Studio (ComfyUI)

1. Start your local ComfyUI instance.
2. Build your **Text → FLUX.1 → Wan2.2** workflow.
3. Enable "Dev Mode" in ComfyUI settings → "Save (API Format)".
4. Save the exported JSON as `workflows/api_workflow.json`.
5. Open `main.py` and update `prompt_node_id="6"` to match your workflow's text node ID.

### 4. Run the Pipeline

Ensure ComfyUI is running at `http://127.0.0.1:8188`, then:

```bash
python main.py
```

Enter your topic when prompted. Walk away. Your video will be waiting in `output/`.

---

## Docker (Run with One Command)

```bash
docker-compose up
```

This spins up Ollama, ComfyUI, and the Python orchestrator as three GPU-enabled microservices.

---

## CI/CD (GitHub Actions + GCP)

Every push to `main` automatically:
1. Runs a smoke test on core modules
2. Builds and pushes the Docker image to Google Artifact Registry
3. Deploys to a GPU-backed Compute Engine VM

See `.github/workflows/deploy.yml` and configure `GCP_PROJECT_ID` and `GCP_SA_KEY` in GitHub Secrets.

---

## Built by

**[Databloom AI & Tech](https://github.com/Vinay1094)** — Democratizing AI-powered content creation.

---

## License

MIT License — free to use, modify, and distribute.
