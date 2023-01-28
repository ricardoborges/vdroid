import typer, os, json
from yaspin import yaspin
from pprint import pprint
import builders.articlebuilder as articlebuilder, builders.bgbuilder as bgbuilder
import builders.moviebuilder as moviebuilder
import scope

app = typer.Typer()

@yaspin(text="[book for book.config]\n")
@app.command()
def article(
    desc: str = typer.Option(..., prompt=True),
    folder: str = typer.Option(..., prompt=True),
    keyword: str = typer.Option(..., prompt=True),
    english: bool = False,
    bing: bool = False,
    single: bool = True):
    
    english = False
    bing = True
    single = True

    options = {'description': desc, 
               'folder':folder, 
               'english':english, 
               'bing':bing, 
               'single':single,
               'keyword': keyword}

    scope.basedir = f"_output/{options['folder']}"

    os.makedirs("_output", exist_ok=True)
    os.makedirs(scope.basedir, exist_ok=True)

    scope.isarticle = True
    scope.articlepath = f"{scope.basedir}/{options['folder']}.txt"
    scope.audiopath_single = f"{scope.basedir}/{options['folder']}.mp3"
    scope.imagepath_single = f"{scope.basedir}/{options['folder']}.jpg"
    scope.finalcut = f"{scope.basedir}/{options['folder']}.mp4"

    scope.hasArticle = os.path.isfile(scope.articlepath)
    scope.hasSingleAudio = os.path.isfile(scope.audiopath_single)
    scope.hasSingleImage = os.path.isfile(scope.imagepath_single)

    articlebuilder.run(options)

def runmovie():
    scope.basedir = f"_output/{scope.options['title']}"

    os.makedirs("_output", exist_ok=True)
    os.makedirs(scope.basedir, exist_ok=True)

    scope.options['single'] = 'False'

    scope.articlepath = f"{scope.basedir}/{scope.options['title']}.txt"
    scope.audiopath_single = f"{scope.basedir}/{scope.options['title']}.mp3"
    
    scope.finalcut = f"{scope.basedir}/{scope.options['title']}.mp4"
    scope.hasArticle = os.path.isfile(scope.articlepath)
    scope.hasSingleAudio = os.path.isfile(scope.audiopath_single)
    scope.ismovie = True

    moviebuilder.run()


@yaspin(text="[movie for movie.config]\n")
@app.command()
def movie(batch: bool = False):  
    file ="movie.config"
    with open(file, 'r') as json_file:
        content = json_file.read()

    list = json.loads(content)

    if (batch):
        print(f"[batch size: {len(list)}]")
        x = 1
        for options in list:
            print(f"[position: {x}/{len(list)}]")
            try:
                scope.options = options
                runmovie()
                x+=1
            except:
                print(f"******** erro {scope.options['title']}")
    else:
        options = list[0]
        scope.options = options
        runmovie()
            

    
@yaspin(text="[boardgame for bg.config]\n")
@app.command()
def bg(name: str = typer.Option(..., prompt=True),
       english: bool = False):
    os.makedirs("_output", exist_ok=True)
    os.makedirs("_output/bg", exist_ok=True)
    bgbuilder.run(name, english)



if __name__ == "__main__":
    app()
