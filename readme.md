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

ggerganov/whisper.cpp is great for English, but guillaumekln/faster-whisper and linto-ai/whisper-timestamped perform better with foreign languages. 

As such, it may be necessary in the future to deploy workers that are 'extended,' meaning that they can process a wider variety of languages. 

English and common language inference can be done with 'tiny' or 'base,' model size but foreign should be done on 'small' or higher.

More testing will need to be done on which languages are most accurate.

Use https://gist.github.com/carlopires/1262033/c52ef0f7ce4f58108619508308372edd8d0bd518 for country codes.