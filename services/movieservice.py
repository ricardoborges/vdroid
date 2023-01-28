from moviepy.editor import *
import services.imageservice as imageservice
import providers.movieimgprovider as movieimgprovider
import scope
import shutil, pprint

def countVideos():
    list = []
    for root, dirs, files in os.walk(scope.basedir):
        for file in files:
            if file.endswith(".mp4"):
                list.append(os.path.join(root, file))

    return len(list)

def countScenes():
    list = []
    for root, dirs, files in os.walk(scope.basedir):
        for file in files:
            if file.endswith(".jpg"):
                list.append(os.path.join(root, file))

    return len(list)

def hasVideos():
    return countVideos() >= scope.totalScenes        

def hasScenes():
    return countScenes() >= scope.totalScenes    

def createImages(article, options):
    hasPoster = os.path.isfile(f"{scope.basedir}/poster.jpg")

    if (hasPoster):
        print("[poster exists]")
    else:
        movieimgprovider.getPoster(options)

    totalInDisk = countScenes()

    #if (hasScenes()):
    ##    print("scenes exists")
    #else:
    print("[creating videos]")
    movieimgprovider.getScenes(options, scope.totalScenes, totalInDisk)

def createVideo( options):
    if (hasVideos()):
        print("videos exists")
    else:
        totalVideos = countVideos()

        i = totalVideos 
        scope.totalScenes = scope.totalScenes - i

        images = imageservice.select_images()

        


        if (len(images) < scope.totalScenes):
            images = images + images + images

        for item in range(scope.totalScenes):  
            print(f"[create video scene {scope.basedir}/scene-{i+1}.mp4")
            createVideoScene(i, images[i])
            i+=1

    createFinalCut(options)



def createVideoScene(i, image):
    found = os.path.isfile(image['path'])

    if (not found):
        return

    os.makedirs(f"{scope.basedir}/scenes/", exist_ok=True)
    shutil.copy(image['path'], f"{scope.basedir}/scenes/{image['filename']}")

    #print(image)
    #sys.exit()


    audio = f"{scope.basedir}/audio-{i+1}.mp3"
    image = image['path']
    scene = f"{scope.basedir}/scene-{i+1}.mp4"

    audio_clip = AudioFileClip(audio)
    audio_duration = audio_clip.duration

    try:
        image_clip = ImageClip(image).set_duration(audio_duration)
    except Exception as ex:
        image_clip = ImageClip(scope.black).set_duration(audio_duration)

    clip = image_clip.set_audio(audio_clip)

    video = CompositeVideoClip([clip])

    video = video.write_videofile(scene, fps=24)


def createFinalCut(options):
    finalcut = f"{scope.basedir}/{options['title']}-final.mp4"
    
    found = os.path.isfile(finalcut)
    if (found):
        print("final cut exists")
        return
    
    print("[Creating final cut]")
    clips = []

    i = 1
    while(i <= scope.totalScenes):
        clip = VideoFileClip(f"{scope.basedir}/scene-{i}.mp4")
        clips.append(clip)
        i+=1

    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.write_videofile(finalcut)

    shutil.copyfile(finalcut, f"Finalizados/{options['title']}-final.mp4")
    shutil.copyfile(scope.articlepath, f"Finalizados/{options['title']}.txt")

    if (scope.posterFound):
        shutil.copyfile(f"{scope.basedir}/poster.jpg", f"Finalizados/{options['title']}-thumb.jpg")
    else:
        shutil.copyfile(f"{scope.basedir}/scene-1.jpg", f"Finalizados/{options['title']}-thumb.jpg")
    return