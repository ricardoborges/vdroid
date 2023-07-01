from pprint import pprint
import requests
import scope
import shutil
from PIL import Image
import  os
from py_linq import Enumerable

def getPoster(options):

    scope.posterFound = False
    subscriptionKey = os.environ.get("BING_API_KEY")

    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    if (options['english'] == 'True'):
        mkt = "en-US"
        word = "poster of the movie " + options['title']
    else:
        mkt = "pt-BR"
        word = "poster do filme " + options['title']
    
    params = {"q": word, "mkt": mkt, "size":"large"}

    if (options['short'] == 'True'):
        params['aspect'] = "tall"

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

    try:
        print("[searching poster]")
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        search_results = response.json()

        print("bing response")
        #pprint(search_results)

        if "entities" in search_results:
            url = search_results["entities"]["value"][0]["image"]["hostPageUrl"]
            print(f"entities {url}")
            return savePoster(url)
        
        if "images" in search_results:
            url = search_results["images"]["value"][0]["contentUrl"]
            print(f"images {url}")
            return savePoster(url)

        print("--poster not found")

    except Exception as ex:
        print("*error find bing image")
        scope.imagepath_single = scope.black
        return scope.black

def countScenes():
    list = []
    for root, dirs, files in os.walk(scope.base_working_dir):
        for file in files:
            if file.endswith(".jpg"):
                list.append(os.path.join(root, file))

def getScenes(max, totalInDisc):
    subscriptionKey = os.environ.get("BING_API_KEY")

    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    if (scope.options['english'] == 'True'):
        mkt = "en-US"
        if (scope.ismovie):
            word = "scenes of the movie " + scope.options['title']
        if (scope.isbook):
            word = "book " + scope.options['title']
        
    else:
        mkt = "pt-BR"
        if (scope.ismovie):
            word = "cenas do filme " + scope.options['title']
        if (scope.isbook):
            word = "livro " + scope.options['title']

    
    params = {"q": word, "mkt": mkt, "size":"large"}
    
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

    try:
        print("[searching scenes]")
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        search_results = response.json()

        total = len(search_results["images"]["value"])

        if (totalInDisc == 1):
            i = 2
        else:
            i = totalInDisc 

        #bugfix  ?? title": "O Cavaleiro das Trevas" --nao encontra poster
        if (i == 0 and totalInDisc == 0 and not scope.posterFound):
            i = 1

        for item in search_results["images"]["value"]:
            if (i > max + 4):
            #    x = i - 1
            #    shutil.copy(vdroid_scene, f"{scope.basedir}/scene-{x}.jpg")
                return
            try:
                save(item["contentUrl"], i)
                image = Image.open(f"{scope.base_working_dir}/scene-{i}.jpg")
                i+=1
            except IOError:
                print(f"bad img! {item['contentUrl']}")

    except Exception as ex:
        print("*error find bing image")
        scope.imagepath_single = scope.black
        return scope.black


def save(url, index):
    print(f"dowloading {scope.base_working_dir}/scene-{index}.jpg...")
    response = requests.get(url, stream=True)
    with open(f"{scope.base_working_dir}/scene-{index}.jpg", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    del response    

def savePoster(url):
    print(f"dowloading poster...")
    response = requests.get(url, stream=True)
    with open(f"{scope.base_working_dir}/poster.jpg", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    del response    
    scope.posterFound = True

