from moviepy.editor import *
import providers.articleprovider as articleprovider
import providers.voiceprovider as voiceprovider
import services.movieservice as movieservice
import services.uploadservice as uploadservice
import scope
import os, shutil

def run():
    article = createArticle()
    found = os.path.isfile(scope.finalcut)

    if (found):
        shutil.copyfile(scope.finalcut, f"Finalizados/{scope.options['title']}-final.mp4")
        shutil.copyfile(scope.article_path, f"Finalizados/{scope.options['title']}.txt")
        #shutil.copyfile(f"{scope.base_working_dir}/scene-1.jpg", f"Finalizados/{scope.options['title']}-thumb.jpg")
        #createUpload(article)    
        return

    scope.totalScenes = len(article.split("."))
    if (scope.options['short'] == 'True'):
        duration = moreThanOneMinute(article)
        if (duration):
            print("the article has more than 1 minute")
            return

    createVoice(article)
    createImages()
    #createVideo()
    #createUpload(article)

#def createUpload(article):
#    print(f"[create upload {scope.options['title']}.json]")
#    uploadservice.buildUpload(article)


def moreThanOneMinute(article):
    voiceprovider.createSingleVoiceOver(article)
    audio_clip = AudioFileClip(scope.audiopath_single)
    audio_duration = audio_clip.duration
    return audio_duration > 60

def hasMp3files(article):
    list = []
    for root, dirs, files in os.walk(scope.base_working_dir):
        for file in files:
            if file.endswith(".mp3"):
                list.append(os.path.join(root, file))

    lines = len(article.split("."))
    
    return len(list) >= lines

def createImages():
    movieservice.createImages()

#def createVideo():
#    movieservice.createVideo()

def createVoice(article):
    
    if (hasMp3files(article)):
        print("voice exists")
        return
    
    print("[creating voice...]")
    voiceprovider.createVoiceOver(article)

def createArticle():
    if (scope.has_article):
        print(f"article exists: {scope.options['title']}")
        f = open(scope.article_path, 'r')
        article = f.read()
        f.close()
        return article

    print(f"[creating article: {scope.options['title']}]")
    article = articleprovider.generateArticle(scope.options).strip()
    f = open(scope.article_path, "w")
    f.write(article)
    f.close()

    return article


