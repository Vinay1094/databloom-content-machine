import json
import urllib.request
import websocket  # pip install websocket-client
import uuid


class ComfyUIClient:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        # Generate a unique client ID for the websocket connection
        self.client_id = str(uuid.uuid4())

    def queue_prompt(self, prompt_workflow):
        """Sends the workflow JSON to the ComfyUI API queue."""
        p = {"prompt": prompt_workflow, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(
            f"http://{self.server_address}/prompt", data=data
        )
        try:
            response = urllib.request.urlopen(req)
            return json.loads(response.read())
        except Exception as e:
            print(f"Error communicating with ComfyUI: {e}")
            return None

    def wait_for_execution(self, prompt_id):
        """
        Connects via WebSocket and blocks until the specific prompt finishes.
        Replaces time.sleep() with a real-time event listener.
        """
        print("Waiting for ComfyUI to finish rendering...")
        ws_url = f"ws://{self.server_address}/ws?clientId={self.client_id}"
        ws = websocket.WebSocket()
        ws.connect(ws_url)

        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                # When node is None, the entire prompt pipeline is finished
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data.get('prompt_id') == prompt_id:
                        print(f"Render complete for Prompt ID: {prompt_id}")
                        break
        ws.close()

    def generate_scene(self, workflow_path, positive_prompt, prompt_node_id="6"):
        """
        Loads the ComfyUI workflow JSON, injects the LLM-generated prompt,
        queues the job, and waits for it to complete via WebSocket.
        """
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)

        # Inject the LLM-generated visual prompt into the correct text node
        workflow[prompt_node_id]["inputs"]["text"] = positive_prompt
        print(f"Queueing scene: {positive_prompt[:50]}...")

        queued_data = self.queue_prompt(workflow)
        if queued_data:
            prompt_id = queued_data['prompt_id']
            # Block until ComfyUI signals completion
            self.wait_for_execution(prompt_id)
            return True
        return False
