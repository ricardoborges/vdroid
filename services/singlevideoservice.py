from moviepy.editor import *

import providers.bingprovider as bingprovider
import scope

def createVideo(article, options):
    if (options['bing']):
        bingprovider.getBingImage(options['keyword'], options['english'])
    
    createImageScene(scope.audiopath_single, scope.imagepath_single, scope.finalcut)

        


def createImageScene(audiofilepath, imagefilepath, outputfile):
  
    print(f"audio = {audiofilepath}")
    print(f"image = {imagefilepath}")
    print(f"final = {outputfile}")

    audio_clip = AudioFileClip(audiofilepath)
    audio_duration = audio_clip.duration

    image_clip = ImageClip(imagefilepath).set_duration(audio_duration)
    clip = image_clip.set_audio(audio_clip)

    video = CompositeVideoClip([clip])

    video = video.write_videofile(outputfile, fps=24)


