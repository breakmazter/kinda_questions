# kinda_questions_2_mazanios

scheme pipeline: https://app.diagrams.net/#G1DbigctwBUQqpWsHFXY94AhV9zYPT_ekR

------------------------------------------------------------------------------------------------------------------
                                                                                        
                                                                                        
DATA_COUNT = 100 000

Time for generate data: t = 12.380579471588135 seconds

Time for generate and delivery data: t = 198.27464056015015 seconds

## create_youtube_video_worker
count vCPUs | RAM | count pool | count thread | usage CPU | usage RAM | speed | time 
--- | --- | --- | --- | --- | --- | --- | ---
| 2 | 1 GB | 1 | 4 | 80.7% | 5.0% | 10-11 message/sec| ~2 hour
| 2 | 1 GB | 1 | 8 | 94.7% | 5.0% | 8-9 message/sec | ~2.2 hour
| 2 | 1 GB | 1 | 16 | 98.9% | 5.4% | ~8 message/sec | ~2.2 hour
| 2 | 1 GB | 2 | 1 | 34.5% | 4.3% | ~8 message/sec | ~2.2 hour
| 2 | 1 GB | 2 | 2 | 51.4% | 5.1% | ~9 message/sec | ~2.2 hour
| 2 | 1 GB | 2 | 4 | 65.6% | 6.6% | 10-11 message/sec | 2 hour
| 2 | 1 GB | 4 | 4 | 40% | 5% | ~14 message/sec | ~1.8 hour
| 2 | 1 GB | 4 | 16 | 40% | 5% | ~14 message/sec | ~1.8 hour
|#|#|#|#|#|#|#|#
| 2 | 4 GB | 1 | 1 | - | - | 15-16 message/sec | ~1.6 hour
| 2 | 4 GB | 4 | 4 | 40% | 1.2% | ~76 message/sec | ~0.4 hour
| 2 | 4 GB | 4 | 8 | 38.6% | 1.6% | ~60 message/sec | ~0.4 hour
| 2 | 4 GB | 4 | 16 | 38.6% | 1.6% | ~62 message/sec | ~0.4 hour

## create_youtube_channel_worker
count vCPUs | RAM | count pool | count thread | usage CPU | usage RAM | speed | time 
--- | --- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 99% | 9.7% | 24 message/sec | 

## create_email_worker
count vCPUs | RAM | count pool | count thread | usage CPU | usage RAM | speed | time 
--- | --- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 99% | 9.7% | 24 message/sec | 

## create_link_product_worker
count vCPUs | RAM | count pool | count thread | usage CPU | usage RAM | speed | time 
--- | --- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 99% | 9.7% | 24 message/sec | 

## update_product_description_worker
count vCPUs | RAM | count pool | count thread | usage CPU | usage RAM | speed | time 
--- | --- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 99% | 9.7% | 24 message/sec | 

## update_video_tags_worker
count vCPUs | RAM | count pool | count thread | usage CPU | usage RAM | speed | time 
--- | --- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 99% | 9.7% | 24 message/sec | 

## delete_video_worker
count vCPUs | RAM | count pool | count thread | usage CPU | usage RAM | speed | time 
--- | --- | --- | --- | --- | --- | --- | ---
| 2 | 4 GB | 1 | 1
| 2 | 4 GB | 1 | 16 | 99% | 9.7% | 24 message/sec | 

