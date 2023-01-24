from moviepy.editor import *
import services.singlevideoservice as singlevideoservice 
import scope

def createVideo(article, options):
    if (options['single']):
        singlevideoservice.createVideo(article, options)
    else:
        multiple()

def multiple():
    print("")
