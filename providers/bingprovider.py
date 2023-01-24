from pprint import pprint
import requests
import scope
import shutil


def getBingImage(query, english, multiple=False):
    subscriptionKey = "cc3f3efaad72405a841acecc1e90c375"
    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    if (english):
        mkt = "en-US"
    else:
        mkt = "pt-BR"
    params = {"q": query, "mkt": mkt}
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

    try:
        print("[bing image search]")
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        search_results = response.json()

        print("big response")
        #pprint(response.json())

        if "entities" in search_results:
            url = search_results["entities"]["value"][0]["image"]["hostPageUrl"]
            print(f"entities {url}")
            return save(url)
        
        if "images" in search_results:
            url = search_results["images"]["value"][0]["contentUrl"]
            print(f"images {url}")
            return save(url)

        print("--image not found")
        scope.imagepath_single = scope.black

        return scope.black

    except Exception as ex:
        print("*error find bing image")
        scope.imagepath_single = scope.black
        return scope.black
        
    

def save(url):
    print("dowloading...")
    response = requests.get(url, stream=True)
    with open(scope.imagepath_single, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    del response    
    
    print("...done")
    
    return scope.imagepath_single

#if __name__ == "__main__":
#    getBingImage("de volta para o futuro", False)
