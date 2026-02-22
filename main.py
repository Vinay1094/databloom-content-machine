import os
import time
from core.llm_agent import LLMAgent
from core.tts_engine import TTSEngine
from core.comfy_client import ComfyUIClient
from utils.video_stitcher import stitch_videos_and_audio


def setup_directories():
    """Create required output directories."""
    os.makedirs("output/clips", exist_ok=True)


def main():
    print("="*50)
    print(" Databloom AI Content Pipeline")
    print(" Idea -> Script -> Audio -> Video -> Reel")
    print("="*50)

    setup_directories()

    # Get topic from user
    topic = input("\nEnter the topic for your video: ").strip()
    if not topic:
        print("No topic provided. Exiting.")
        return

    # -------------------------
    # 1. Initialize all agents
    # -------------------------
    llm = LLMAgent(model_name="llama3")
    tts = TTSEngine(voice='af_heart')
    studio = ComfyUIClient(server_address="127.0.0.1:8188")

    # -------------------------
    # 2. Generate Script & Visual Prompts
    # -------------------------
    script_data = llm.generate_script(topic)
    if not script_data:
        print("Pipeline halted: Failed to generate script.")
        return

    print("\n--- Generated Voiceover Script ---")
    print(script_data['voiceover'])
    print(f"\n--- {len(script_data['visual_prompts'])} Visual Scenes Planned ---")
    for i, p in enumerate(script_data['visual_prompts']):
        print(f"  Scene {i+1}: {p[:80]}...")
    print("")

    # -------------------------
    # 3. Generate Audio (TTS)
    # -------------------------
    audio_path = tts.generate_audio(
        script_data['voiceover'],
        output_path="output/voiceover.wav"
    )
    if not audio_path:
        print("Pipeline halted: Failed to generate audio.")
        return

    # -------------------------
    # 4. Generate Video Clips via ComfyUI (FLUX.1 -> Wan2.2)
    # -------------------------
    workflow_file = "workflows/api_workflow.json"
    visual_prompts = script_data['visual_prompts']

    for i, prompt in enumerate(visual_prompts):
        print(f"\nProcessing Scene {i+1}/{len(visual_prompts)}...")
        # prompt_node_id="6" matches the CLIPTextEncode node in api_workflow.json
        success = studio.generate_scene(
            workflow_file, prompt, prompt_node_id="6"
        )
        if not success:
            print(f"Warning: Scene {i+1} failed to queue. Skipping.")

    # -------------------------
    # 5. Stitch All Clips + Audio -> Final Reel
    # -------------------------
    final_output = f"output/final_reel_{int(time.time())}.mp4"
    stitch_videos_and_audio(
        video_folder="output/clips",
        audio_path=audio_path,
        output_path=final_output
    )

    print(f"\n{'='*50}")
    print(f" PIPELINE COMPLETE!")
    print(f" Your video is ready: {final_output}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
