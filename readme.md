# Front-end application:
website where users upload audio/video content to generate subtitles
subtitles would be returned. video may be a premium only feature.


# Back-end application:
https://github.com/abdeladim-s/subsai
SubsAI used for subs generation.

deepl.com would be used for the translation component.

before api access is used, a selenium bot could be used to get translation after transcript is acquired.

# Technologies:

docker is used for containerizing the backend component.
react for the frontend
.ogg file format seems to be the smallest. try to compress more.

# Parallel Workflow:

A central backend node will share work across several other nodes. This may be controlled with Docker Swarm, but will likely be done manually.

Parallel processing practices will be employed to:
- Send transcription tokens to nodes running Selenium backend
- Encoding subtitles (for video)

# Notes about Models

guillaumekln/faster-whisper is the default model for all transcription needs. 
performance is great. 

Use https://gist.github.com/carlopires/1262033/c52ef0f7ce4f58108619508308372edd8d0bd518 for country codes.

TODO: Complete testing with the load balancer and multiple workers. Slower inference speed is acceptable when there are more workers to balance the load.
TODO: Load balancer should be reconfigured so that the workers with the least jobs are assigned new jobs. CPU load is too inconsistent.

## BENCHMARKS

### Small model

16GB RAM 3CPUS: 3500ms (4.28x) accuracy: ?

6GB RAM 2CPUS: 4800ms (3.06x) accuracy: ?

### Base model
