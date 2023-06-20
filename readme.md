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

mozilla's deepspeech and Coqui STT used for transcription

tokenize the transcript by sentences ==> each token is sent to deepl for translation... cache may be used in the future to reduce load on selenium threads.

using the following git repo for subs generation: https://github.com/abhirooptalasila/AutoSub

# Parallel Workflow:

A central backend node will share work across several other nodes. This may be controlled with Docker Swarm, but will likely be done manually.

Parallel processing practices will be employed to:
- Send transcription tokens to nodes running Selenium backend
- Encoding subtitles (for video)
