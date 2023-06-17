# Front-end application:

website where users upload audio/video content to generate subtitles
a piece of a/v media is returned with subtitles 


# Back-end application:

store the media content ... 

if: video --> generate transcript of the video content and then translate and encode subtitles

if audio --> generate transcript and return a subtitle for it... .srt could be possible premium option

deepl.com would be used for the translation component.
before api access is used, a selenium bot could be used to get translation after transcript is acquired.


# Technologies:

docker is used for containerizing the backend component.

react for the frontend

ffmpeg for video compression

tokenize the transcript by sentences ==> each token is sent to deepl for translation... cache may be used in the future to reduce load on selenium threads.