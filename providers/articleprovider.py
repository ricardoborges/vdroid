import openai, re
import scope

key = "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"

openai.api_key = key

def generateArticle(options):
    if (scope.isarticle):
        response = create(options['description'])

    if (scope.ismovie):
        if (options['english'] == 'True'):
            prompt = f"write a summary of the movie {options['title']}"
        else:
            prompt = f"escreva um resumo do filme {options['title']}"
        response = create(prompt, options)

    result = response['choices'][0].text + options['final']
    result = setup(result)
    return result

def generateRules(name, english):
    if (english):
        promptTxt = f"explain the rules how to play the boardgame {name}"
    else:
        promptTxt = f"explique as regras de como jogar o boardgame {name}"

    response = create(promptTxt)

    return response['choices'][0].text    


def create(promptTxt, options):
    max = 800
    if (options['short'] == "True"):
        max = 300

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=promptTxt,
        temperature=0,
        max_tokens=max,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    return response

def setup(txt):
    txt = remove_parenteses(txt)
    txt = remove_abreviacoes(txt)
    txt = remove_lastname(txt)
    return txt

def remove_abreviacoes(txt):
    txt = txt.replace("Dr.", "doutor")
    txt = txt.replace("DR.", "doutor")
    txt = txt.replace("Jr.", "junior")
    txt = txt.replace("JR.", "junior")
    txt = txt.replace("S.H.I.E.L.D.", "SHIELD")
    return txt

def remove_lastname(txt):
    list = txt.split(" ")
    for item in list:
        if (len(item) == 2):
            if (item[1] == "."):
                txt = txt.replace(item, item[0])
    return txt

def remove_parenteses(txt):
    return re.sub("[\(\[].*?[\)\]]", "", txt)