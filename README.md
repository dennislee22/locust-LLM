# Locust -> LLM
<img width="259" alt="image" src="https://github.com/user-attachments/assets/9de4642e-ffc6-42fb-a631-9a1edf0325fe" />

This article describes the performance of a LLM model serving end-users' chat requests with different settings such as number of tokens, and response lengths, using Locust as the stress testing tool. Locust enables simulation of user traffic by generating concurrent requests to the model's API, allowing us to observe how the system behaves under varying loads. 

## LLM Setup
- Download Llama-2-7B model from the HF site.
- Install the necessary Python libraries.
```
pip install transformers ipywidgets nvitop fastapi torch uvicorn
```
- Create the inference script `llm-inference.py`.
- Run the inference script by selecting 2vCPU, 64GB with 1 GPU profile.
<img width="463" alt="image" src="https://github.com/user-attachments/assets/73b391df-b661-488e-8523-b231ad78a787" />
<img width="1442" alt="image" src="https://github.com/user-attachments/assets/f7f9f607-35bb-4ae2-948a-99a79896f1ac" />

- Test querying the LLM API using the following command.
```
curl -X POST https://llama2-chat.cml.apps.company.com/generate/ \
>   -H "Content-Type: application/json" \
>   -d '{
>     "prompt": "Once upon a time,",
>     "max_new_tokens": 20,
>     "temperature": 0.7
>   }'
{"generated_text":"Once upon a time, there was a little girl who loved to read. She loved to read so much that she would read"}
```

## Locust Setup

- Install Locust library.
```
pip install locust
```

## Run Locust

1. Prepare `locustfile.py` file, configure `max_new_tokens = 10`.
2. Run Locust with parameters `--headless -u 10 --spawn-rate 10 --run-time 1m` targeting the FASTAPI/locally hosted LLM with 10 virtual users for 1 minute, using a single LLaMA-2-7B model deployed on a GPU with 40GB of memory. 

```
locust --headless -u 10 --spawn-rate 10 --run-time 1m -f locustfile.py -H https://llama2-chat.cml.apps.company.com
```

3. Monitor the `nvitop` output in the hosting node.
<img width="1460" alt="image" src="https://github.com/user-attachments/assets/750ae667-b781-4063-a5ac-6a8d1104cc27" />

4. Capture the output upon successful completion of the Locust command.
```
Type     Name                                                     # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|-------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
POST     /generate/                                                  206     0(0.00%) |   2537     445    6095   2400 |    3.46        0.00
--------|-------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                  206     0(0.00%) |   2537     445    6095   2400 |    3.46        0.00

Response time percentiles (approximated)
Type     Name                                                             50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-----------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
POST     /generate/                                                      2400   2500   2500   2600   2700   4700   5300   5500   6100   6100   6100    206
--------|-----------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                      2400   2500   2500   2600   2700   4700   5300   5500   6100   6100   6100    206
```

5. Check the generated LLM output in the file.
```
$ tail -f locust_output.txt 

203. here and it’s changing the way we do

204. in the hands of the young
The young people

205. here, and it’s called ChatG

206. in the hands of the next generation of data scient
```

6. Configure `locustfile.py` with `max_new_tokens = 20` parameter. Repeat step 2 to 5. 

```
Type     Name                                                     # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|-------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
POST     /generate/                                                   86     0(0.00%) |   5036     703    5792   5200 |    1.78        0.00
--------|-------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                   86     0(0.00%) |   5036     703    5792   5200 |    1.78        0.00

Response time percentiles (approximated)
Type     Name                                                             50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-----------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
POST     /generate/                                                      5200   5300   5400   5400   5400   5400   5500   5800   5800   5800   5800     86
--------|-----------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                      5200   5300   5400   5400   5400   5400   5500   5800   5800   5800   5800     86
```

```
$ tail -f locust_output.txt 

84. bright, but it’s not here yet
The future of AI is bright, but it

85. not about the technology. It is about the people who will use it.
The future of A

86. in the hands of the people
The future of AI is in the hands of the people.
```

7. Configure `locustfile.py` with `max_new_tokens = 50` parameter. Repeat step 2 to 5. 

```
Type     Name                                                     # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|-------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
POST     /generate/                                                   43     0(0.00%) |  12061    1521   13879  13000 |    0.73        0.00
--------|-------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                   43     0(0.00%) |  12061    1521   13879  13000 |    0.73        0.00

Response time percentiles (approximated)
Type     Name                                                             50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-----------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
POST     /generate/                                                     13000  13000  14000  14000  14000  14000  14000  14000  14000  14000  14000     43
--------|-----------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                     13000  13000  14000  14000  14000  14000  14000  14000  14000  14000  14000     43

```

```
$ tail -f locust_output.txt 
41. in the hands of the people
A few weeks ago, I was invited to speak at the 2018 Artificial Intelligence Conference in San Francisco. The conference was a gathering of the world’s leading AI experts

42. bright, but it will take a lot of work to get there.
The future of AI is bright, but it will take a lot of work to get there. AI is a rapidly growing field that is being used in a variety of

43. not a single technology but a combination of many
AI is no longer just about computers that can think like humans. The future of AI is a combination of many technologies, including machine learning, natural language processing, and computer vision.
```

## Conclusion:
✅ Increasing the value of max_new_tokens results in lower transactions per second (tps). This suggests that longer text generation per request reduces overall throughput, due to increased computation time per request using 1 GPU.

## KV Cache
- KV cache (key-value cache) can help to optimize inference by reusing key-value states from previous tokens, especially in autoregressive generation tasks (where you generate one token at a time). This could help to increase tps as it accelerates token-by-token generation when you’re generating a long output. This significantly improves the speed and efficiency of generating long sequences of text since it avoids recomputing the key-value states for every new token in the sequence. In the context of HF Transformers, KV cache can be enabled by using the `use_cache=True` flag when calling the model for generation.
- To simulate KV cache activation, run LLM application with `llm-kvcache.py` script using `use_cache=True` parameter enables KV cache. `kv_cache` is a Python dictionary storing everything indefinitely. In contrast, `use_cache=False` recomputes every token from scratch each time.
- Run Locust test again, this time with `locustfile-5prompts.py`. This script simulates 5 prompts per user session, each user continues from the previous prompt. 
- ⚠️ When using KV cache manually, GPU memory usage grows quickly because it stores the full attention history (past_key_values) for every unique cache_key. No limit or cleanup means GPU RAM just keeps filling up. As a result, `torch.OutOfMemoryError: CUDA out of memory` will occur.

![kv-cache-oom](https://github.com/user-attachments/assets/68f9078c-17ae-434c-aae0-5e9e526921c8)


