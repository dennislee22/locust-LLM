# Locust -> LLM

```
# locust --headless -u 10 --spawn-rate 10 --run-time 1m -f locustfile.py -H https://llama2-chat.cml.apps.company.com
```

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

