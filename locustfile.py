from locust import HttpUser, task, between, events
import urllib3
import threading
import os

# Disable SSL warnings (only relevant for HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Thread-safe lock and counter
write_lock = threading.Lock()
line_counter = {"count": 0}

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    output_file = "locust_output.txt"
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"[INFO] Removed existing {output_file}")

class LLMUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        self.client.verify = False

    @task
    def generate(self):
        response = self.client.post("/generate/", json={
            "prompt": "The future of AI is",
            "max_new_tokens": 10,
            "temperature": 0.7
        })
        if response.status_code == 200:
            output_text = response.json().get("generated_text", "").strip()
            with write_lock:
                line_counter["count"] += 1
                line_number = line_counter["count"]
                with open("locust_output.txt", "a", encoding="utf-8") as f:
                    f.write(f"{line_number}. {output_text}\n\n")
