import typer, os, json
import builders.moviebuilder as moviebuilder
import builders.bookbuilder as bookbuilder
import scope
from dotenv import load_dotenv

app = typer.Typer()

load_dotenv()

#@app.command()
#def article(
#    keyword: str = typer.Option(..., prompt=True),
#    english: bool = False)
    

def run_movie():
    scope.base_working_dir = f"_output/{scope.options['title']}"

    os.makedirs("_output", exist_ok=True)
    os.makedirs(scope.base_working_dir, exist_ok=True)

    scope.options['single'] = 'False'

    scope.article_path = f"{scope.base_working_dir}/{scope.options['title']}.txt"
    scope.audiopath_single = f"{scope.base_working_dir}/{scope.options['title']}.mp3"
    
    #scope.finalcut = f"{scope.base_working_dir}/{scope.options['title']}.mp4"
    scope.has_article = os.path.isfile(scope.article_path)
    scope.has_single_audio = os.path.isfile(scope.audiopath_single)
    scope.ismovie = True

    moviebuilder.run()

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
                run_movie()
                x+=1
            except:
                print(f"******** erro {scope.options['title']}")
    else:
        options = list[0]
        scope.options = options
        run_movie()
            

def run_book():
    scope.base_working_dir = f"_output/{scope.options['title']}"

    os.makedirs("_output", exist_ok=True)
    os.makedirs(scope.base_working_dir, exist_ok=True)

    scope.options['single'] = 'False'

    scope.article_path = f"{scope.base_working_dir}/{scope.options['title']}.txt"
    scope.audiopath_single = f"{scope.base_working_dir}/{scope.options['title']}.mp3"
    
    scope.has_article = os.path.isfile(scope.article_path)
    scope.has_single_audio = os.path.isfile(scope.audiopath_single)
    scope.isbook = True

    bookbuilder.run()

@app.command()
def book(batch: bool = False):
    file ="book.config"
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
                run_book()
                x+=1
            except:
                print(f"******** erro {scope.options['title']}")
    else:
        options = list[0]
        scope.options = options
        run_book()
if __name__ == "__main__":
    app()
