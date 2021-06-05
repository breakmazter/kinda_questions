# kinda_questions_2_mazanios

scheme pipeline: https://app.diagrams.net/#G1DbigctwBUQqpWsHFXY94AhV9zYPT_ekR

------------------------------------------------------------------------------------------------------------------
                                                                                        
                                                                                        
DATA_COUNT = 100 000

Time for generate data: t = 12.380579471588135 seconds

Time for generate and delivery data: t = 198.27464056015015 seconds

## create_youtube_video_worker
count vCPUs | RAM | count procces | count thread | speed | usage CPU | usage RAM |
--- | --- | --- | --- | --- | --- | ---
| 2 | 1 GB | 1 | 4 | 10-11 message/sec | 
| 2 | 1 GB | 1 | 8 | 8-9 message/sec 
| 2 | 1 GB | 1 | 16 |~8 message/sec 
| 2 | 1 GB | 2 | 1 |  ~8 message/sec 
| 2 | 1 GB | 2 | 2 | ~9 message/sec
| 2 | 1 GB | 2 | 4 | 10-11 message/sec
| 2 | 1 GB | 4 | 4 | ~14 message/sec 
| 2 | 1 GB | 4 | 16 |~14 message/sec 
|#|#|#|#|#|#|
| 2 | 4 GB | 1 | 1 | 15-16 message/sec
| 2 | 4 GB | 4 | 4 | ~76 message/sec | 98% | 500MB |
| 2 | 4 GB | 4 | 8 |  ~60 message/sec
| 2 | 4 GB | 4 | 16 | ~62 message/sec 

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 3
----------------------------------

## create_youtube_channel_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU | usage RAM |
--- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 24 message/sec | 
| 2 | 4 GB | 2 | 4 | 145 message/sec |
| 2 | 4 GB | 2 | 8 | 140 message/sec | 70% | 480MB |
| 2 | 4 GB | 2 | 16 | 170 message/sec | 96% | 560MB |
| 2 | 4 GB | 2 | 32 | 160 message/sec |
| 2 | 4 GB | 4 | 2 | 145 message/sec |
| 2 | 4 GB | 4 | 4 | 150 message/sec |
| 2 | 4 GB | 4 | 8 | 140 message/sec |
| 2 | 4 GB | 4 | 16 | 150 message/sec |

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 2
----------------------------------


## create_link_product_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU | usage RAM |
--- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1 | 15 message/sec | 20% | 480MB |
| 2 | 4 GB | 4 | 2 | 40 message/sec | 
| 2 | 4 GB | 4 | 4 | 50 message/sec | 99% | 700MB
| 2 | 4 GB | 4 | 8 | 38 message/sec | 
| 2 | 4 GB | 4 | 16 | 30 message/sec | 

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 3
----------------------------------

## create_email_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU | usage RAM |
--- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1| 5 message/sec | 10% | 440MB |
| 2 | 4 GB | 1 | 16 | 25 message/sec | 40% | 456MB
| 2 | 4 GB | 2 | 4 | 70 message/sec | 18% | 470MB
| 2 | 4 GB | 2 | 8 | 85 message/sec | 23% | 480MB
| 2 | 4 GB | 2 | 16 | 92 message/sec | 27% | 436MB
| 2 | 4 GB | 4 | 4 | 92 message/sec | 28% | 522MB

| 2 | 4 GB | 4 | 8 | 85 message/sec | 23% | 480MB
| 2 | 4 GB | 4 | 16 | 85 message/sec | 28% | 522MB

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 3
----------------------------------

## delete_video_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU | usage RAM |
--- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1 | 20 message/sec | 13-14% | 430MB
| 2 | 4 GB | 2 | 4 | 75 message/sec | 55% | 430MB
| 2 | 4 GB | 2 | 8 | 86 message/sec | 70% | 470MB

| 2 | 4 GB | 2 | 16 | 86 message/sec | 70% | 470MB

--------------------------------------------------------------------------------------------------------------------------

DATA_COUNT = ALL_DATA

Time for generate data: t = 643.9179027080536 seconds

Time for generate and delivery data: t = 198.27464056015015 seconds
