import providers.articleprovider as articleprovider
import providers.voiceprovider as voiceprovider
import services.videoservice as videoservice
import scope
import os

def run(options):
    options['final'] = ""
    article = createArticle(options)
    createVoice(article, options)
    videoservice.createVideo(article, options)


def createVoice(article, options):
    if (scope.hasSingleAudio and options['single']):
        print("voice exists")
        return
    
    print("[creating voice...]")
    voiceprovider.createVoiceOver(article, options)

def createArticle(options):
    if (scope.hasArticle):
        print("article exists")
        f = open(scope.articlepath, 'r')
        article = f.read()
        f.close()
        return article

    print("[creating article...]")
    article = articleprovider.generateArticle(options).strip()
    f = open(scope.articlepath, "w")
    f.write(article)
    f.close()

    return article


