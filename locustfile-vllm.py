from locust import HttpUser, task, between, events
import urllib3
import threading
import os
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

write_lock = threading.Lock()
line_counter = {"count": 0}
start_time = {"value": None}
end_time = {"value": None}

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    output_file = "locust_output.txt"
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"[INFO] Removed existing {output_file}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    end_time["value"] = time.time()
    if start_time["value"] and end_time["value"]:
        total_duration = end_time["value"] - start_time["value"]
        with open("locust_output.txt", "a", encoding="utf-8") as f:
            f.write(f"\n=== Total Duration: {total_duration:.3f} seconds ===\n")
        print(f"[INFO] Test completed in {total_duration:.3f} seconds")

class LLMUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        self.client.verify = False

    @task
    def generate(self):
        with write_lock:
            if start_time["value"] is None:
                start_time["value"] = time.time()

        request_start = time.time()
        response = self.client.post("/v1/completions", json={
            "model": "Llama-2-7b-hf",
            "prompt": "The future of AI is",
            "max_tokens": 10,
            "temperature": 0.7
        })
        request_end = time.time()
        duration = request_end - request_start

        if response.status_code == 200:
            output_text = response.json().get("choices", [{}])[0].get("text", "").strip()
            with write_lock:
                line_counter["count"] += 1
                line_number = line_counter["count"]
                with open("locust_output.txt", "a", encoding="utf-8") as f:
                    f.write(f"{line_number}. {output_text}\n")
                    f.write(f"   [Processed Duration: {duration:.3f} seconds]\n\n")
