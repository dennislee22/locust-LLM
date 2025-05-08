# Locust -> LLM

```
# locust --headless -u 10 --spawn-rate 10 --run-time 1m -f locustfile.py -H https://llama2-chat.cml.apps.company.com
```

- Edit `locustfile.py` to configure max_new_tokens to 10. Run the locust command.

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

```
$ tail -f locust_output.txt 

203. here and it’s changing the way we do

204. in the hands of the young
The young people

205. here, and it’s called ChatG

206. in the hands of the next generation of data scient
```

<img width="796" alt="image" src="https://github.com/user-attachments/assets/bef664fd-eec1-413a-9942-cebba7f18484" />

<img width="1460" alt="image" src="https://github.com/user-attachments/assets/750ae667-b781-4063-a5ac-6a8d1104cc27" />


- Edit `locustfile.py` to configure max_new_tokens to 20. Run the locust command.

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

- Edit `locustfile.py` to configure max_new_tokens to 50. Run the locust command.

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

![kv-cache-oom](https://github.com/user-attachments/assets/68f9078c-17ae-434c-aae0-5e9e526921c8)

```
torch.OutOfMemoryError: CUDA out of memory
```



