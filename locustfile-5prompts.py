from locust import HttpUser, task, between, events
import urllib3
import threading
import os
import random
import string
import time

# Disable SSL warnings (for self-signed certs or insecure test servers)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Thread-safe output file write
write_lock = threading.Lock()
line_counter = {"count": 0}

# Toggle to test with or without KV cache
USE_KV_CACHE = True

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    output_file = "locust_output.txt"
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"[INFO] Removed existing {output_file}")

# Generate unique cache keys
def generate_cache_key():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

class LLMUser(HttpUser):
    wait_time = between(0.5, 1.0)

    def on_start(self):
        self.client.verify = False
        self.cache_key = generate_cache_key()
        self.step = 0
        self.prompt_context = "Once upon a time"

    @task
    def generate(self):
        prompt = self.prompt_context

        start = time.time()
        response = self.client.post("/generate/", json={
            "prompt": prompt,
            "max_new_tokens": 100,
            "temperature": 0.7,
            "cache_key": self.cache_key,
            "use_cache": USE_KV_CACHE
        })
        latency = time.time() - start

        if response.status_code == 200:
            generated_text = response.json().get("generated_text", "")
            self.prompt_context = generated_text  # Update prompt for next step

            with write_lock:
                line_counter["count"] += 1
                line_number = line_counter["count"]
                with open("locust_output.txt", "a", encoding="utf-8") as f:
                    f.write(f"{line_number}. Step {self.step + 1} | Latency: {latency:.2f}s\n")
                    f.write(f"Prompt: {prompt}\n")
                    f.write(f"Output: {generated_text.strip()}\n")
                    f.write("-" * 60 + "\n\n")

        self.step += 1
        if self.step >= 5:
            self.environment.runner.quit()
