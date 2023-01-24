from PIL import Image
from moviepy.editor import *
import providers.articleprovider as articleprovider
import providers.voiceprovider as voiceprovider
import services.videoservice as videoservice
import services.movieservice as movieservice
import services.uploadservice as uploadservice
import scope
import os, shutil

def run(options):
    article = createArticle(options)
    finalcut = f"{scope.basedir}/{options['title']}-final.mp4"
    found = os.path.isfile(finalcut)
    if (found):
        shutil.copyfile(finalcut, f"Finalizados/{options['title']}-final.mp4")
        shutil.copyfile(scope.articlepath, f"Finalizados/{options['title']}.txt")
        shutil.copyfile(f"{scope.basedir}/scene-1.jpg", f"Finalizados/{options['title']}-thumb.jpg")
        createUpload(article, options)    
        return

    scope.totalScenes = len(article.split("."))
    if (options['short'] == 'True'):
        duration = moreThanOneMinute(article, options)
        if (duration):
            print("the article has more than 1 minute")
            return

    createVoice(article, options)
    createImages(article, options)
    createVideo(options)
    createUpload(article, options)

def createUpload(article, options):
    print(f"[create upload {options['title']}.json]")
    uploadservice.buildUpload(article, options)


def moreThanOneMinute(article, options):
    voiceprovider.createSingleVoiceOver(article, options)
    audio_clip = AudioFileClip(scope.audiopath_single)
    audio_duration = audio_clip.duration
    return audio_duration > 60

def hasMp3files(article):
    list = []
    for root, dirs, files in os.walk(scope.basedir):
        for file in files:
            if file.endswith(".mp3"):
                list.append(os.path.join(root, file))

    lines = len(article.split("."))
    
    return len(list) >= lines

def createImages(article, options):
    movieservice.createImages(article, options)

def createVideo(options):
    movieservice.createVideo(options)

def createVoice(article, options):
    
    if (hasMp3files(article)):
        print("voice exists")
        return
    
    print("[creating voice...]")
    voiceprovider.createVoiceOver(article, options)

def createArticle(options):
    if (scope.hasArticle):
        print(f"article exists: {options['title']}")
        f = open(scope.articlepath, 'r')
        article = f.read()
        f.close()
        return article

    print(f"[creating article: {options['title']}]")
    article = articleprovider.generateArticle(options).strip()
    f = open(scope.articlepath, "w")
    f.write(article)
    f.close()

    return article


