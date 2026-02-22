import json
import ollama


class LLMAgent:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.system_prompt = """
You are an expert cinematic video producer. Given a topic, write a short video script.
You MUST respond ONLY with a valid JSON object in the exact following structure,
with no markdown formatting or extra text:
{
  "voiceover": "The full spoken narrative text here, written naturally.",
  "visual_prompts": [
    "Prompt 1 describing the first scene in extreme visual detail for an AI image generator.",
    "Prompt 2 describing the second scene...",
    "Prompt 3 describing the third scene..."
  ]
}
Keep the voiceover under 60 seconds and provide exactly 3 to 5 visual prompts.
"""

    def generate_script(self, topic):
        print(f"Generating script and prompts for: '{topic}'...")
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Create a video script about: {topic}"}
                ]
            )
            # Clean up potential markdown formatting from the LLM response
            raw_content = response['message']['content'].strip()
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3]
            elif raw_content.startswith("```"):
                raw_content = raw_content[3:-3]
            return json.loads(raw_content)
        except Exception as e:
            print(f"Error generating script: {e}")
            return None
