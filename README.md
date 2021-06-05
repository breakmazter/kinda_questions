# kinda_questions_2_mazanios

scheme pipeline: https://app.diagrams.net/#G1DbigctwBUQqpWsHFXY94AhV9zYPT_ekR

------------------------------------------------------------------------------------------------------------------
                                                                                        
                                                                                        
DATA_COUNT = 100 000

Time for generate data: t = 12.380579471588135 seconds

Time for generate and delivery data: t = 198.27464056015015 seconds

## create_youtube_video_worker
count vCPUs | RAM | count procces | count thread | speed | usage CPU 
--- | --- | --- | --- | --- | ---
| 2 | 1 GB | 1 | 4 | 10-11 message/sec | 
| 2 | 1 GB | 1 | 8 | 8-9 message/sec 
| 2 | 1 GB | 1 | 16 |~8 message/sec 
| 2 | 1 GB | 2 | 1 |  ~8 message/sec 
| 2 | 1 GB | 2 | 2 | ~9 message/sec
| 2 | 1 GB | 2 | 4 | 10-11 message/sec
| 2 | 1 GB | 4 | 4 | ~14 message/sec 
| 2 | 1 GB | 4 | 16 |~14 message/sec 
| 2 | 4 GB | 1 | 1 | 15-16 message/sec
| 2 | 4 GB | 4 | 4 | ~76 message/sec | 98% 
| 2 | 4 GB | 4 | 8 |  ~60 message/sec
| 2 | 4 GB | 4 | 16 | ~62 message/sec 

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 3
----------------------------------

## create_youtube_channel_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU 
--- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 24 message/sec | 
| 2 | 4 GB | 2 | 4 | 145 message/sec |
| 2 | 4 GB | 2 | 8 | 140 message/sec | 70% 
| 2 | 4 GB | 2 | 16 | 170 message/sec | 96% 
| 2 | 4 GB | 2 | 32 | 160 message/sec |
| 2 | 4 GB | 4 | 2 | 145 message/sec |
| 2 | 4 GB | 4 | 4 | 150 message/sec |
| 2 | 4 GB | 4 | 8 | 140 message/sec |
| 2 | 4 GB | 4 | 16 | 150 message/sec |

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 2
----------------------------------


## create_link_product_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU 
--- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1 | 15 message/sec | 20% 
| 2 | 4 GB | 4 | 2 | 40 message/sec | 
| 2 | 4 GB | 4 | 4 | 50 message/sec | 99% 
| 2 | 4 GB | 4 | 8 | 38 message/sec | 
| 2 | 4 GB | 4 | 16 | 30 message/sec | 

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 3
----------------------------------

## create_email_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU | 
--- | --- | --- | --- | --- | --- 
| 2 | 4 GB | 1 | 1| 5 message/sec | 10% |
| 2 | 4 GB | 1 | 16 | 25 message/sec | 40%
| 2 | 4 GB | 2 | 4 | 70 message/sec | 18% 
| 2 | 4 GB | 2 | 8 | 85 message/sec | 23% 
| 2 | 4 GB | 2 | 16 | 92 message/sec | 27%
| 2 | 4 GB | 2 | 32 | 92 message/sec | 27%
| 2 | 4 GB | 4 | 4 | 92 message/sec | 28% 
| 2 | 4 GB | 4 | 8 | 97 message/sec | 23% 
| 2 | 4 GB | 4 | 8 | 90 message/sec | 30% 


Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 3
----------------------------------

## delete_video_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU 
--- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1 | 20 message/sec | 13-14%
| 2 | 4 GB | 2 | 4 | 75 message/sec | 55% 
| 2 | 4 GB | 2 | 8 | 86 message/sec | 70%
| 2 | 4 GB | 2 | 16 | 100 message/sec | 90%

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 1
----------------------------------

## update_video_tags_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU 
--- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1 | 1-2 message/sec |
| 2 | 4 GB | 2 | 4 | 6 message/sec |
| 2 | 4 GB | 2 | 8 | 8 message/sec |
| 2 | 4 GB | 2 | 16 | 24 message/sec |
| 2 | 4 GB | 2 | 32 | 30 message/sec |
| 2 | 4 GB | 4 | 4 | 10 message/sec | 
| 2 | 4 GB | 4 | 8 | 20 message/sec | 
| 2 | 4 GB | 4 | 16 | 40 message/sec | 
| 2 | 4 GB | 4 | 32 | 30 message/sec |
| 2 | 4 GB | 4 | 64 | 2 message/sec |

Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 3
----------------------------------

## update_product_description_worker
count vCPUs | RAM | count procces | count thread| speed | usage CPU 
--- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1 |


Type MAchine: 2 vCPUs, 1GB RAM
Count MAchine: 1
----------------------------------

--------------------------------------------------------------------------------------------------------------------------

DATA_COUNT = ALL_DATA

Time for generate data: t = 643.9179027080536 seconds

Time for generate and delivery data: t = 198.27464056015015 seconds
