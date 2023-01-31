import json, scope

def buildUpload(article):
    cta = "Deseja ver algum conteúdo (filme, serie, anime, livro, etc)? solicite nos comentários"
    disclaimer = "\nATENÇÂO: Pode conter spoilers! Este video foi gerado por inteligência artificial.\n\n"
    hashtags = "\n\n#Filme #ResumoDeFilme #Aventura #InteligenciaArtificial #IAExplorando #FilmeIA #AventuraComIA #IAEFilmes #FuturoDaIA #movies #filmreviews #moviereviews #filmsummary #movieanalysis #filmcritic #cinema #hollywood #boxoffice #IA #MidJourney #ChatGPT #TextToSpeech "
    description = cta + disclaimer + article + hashtags

    upload = {
        "--title": scope.options['title'],
        "--description": description,
        "--category": "Film & Animation",
        "--tags": "filme,filmereview,movie,moviesummary,ai,ia,midjourney,chatgpt,resumo,resumodefilme,inteligenciaartificial,cinema,review,hollywood,netflix,prime video,hbo max,disney,startplus,globoplay",
        "--default-language": "pt-br",
        "--default-audio-language": "pt-br",
        "--privacy": "private",
        "--thumbnail": f"Finalizados/{scope.options['title']}-thumb.jpg",
        "--playlist": "Resumo de Filmes",
        "--embeddable": "True",
        "--madeForKids": "False",
        f"Finalizados/{scope.options['title']}-final.mp4": ""
    }

    with open(f"Finalizados/{scope.options['title']}.json", "w") as outfile:
        json.dump(upload, outfile)

