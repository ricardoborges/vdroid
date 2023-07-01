import openai, re
import scope
import os
import pprint

key = os.environ.get("OPENAI_API_KEY")

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

    if (scope.isbook):
        if (options['english'] == 'True'):
            prompt = f"write a summary of the book {options['title']}"
        else:
            prompt = f"escreva um resumo do livro {options['title']}"
        response = create(prompt, options)
        

    #result = response['choices'][0].text
    result = setup(response)
    return result

def generateRules(name, english):
    if (english):
        promptTxt = f"explain the rules how to play the boardgame {name}"
    else:
        promptTxt = f"explique as regras de como jogar o boardgame {name}"

    response = create(promptTxt)

    return response['choices'][0].text    


def create(promptTxt, options):
    #max = 800
    #if (options['short'] == "True"):
    #    max = 300

    #response = openai.Completion.create(
    #    model="text-davinci-003",
    #    prompt=promptTxt,
    #    temperature=0,
    #    max_tokens=max,
    #    top_p=1.0,
    #    frequency_penalty=0.0,
    #    presence_penalty=0.0
    #)
    
    #return response
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente de IA especializado em criar artigos resumos sobre filmes e series. responda em ingles ou portugues de acordo com o prompt do usuario"},
                    {"role": "user", "content": f"{promptTxt}"},
                ],
                temperature=0.1,
            )

    return response.choices[0].message.content    

def setup(txt):
    txt = remove_parenteses(txt)
    txt = remove_abreviacoes(txt)
    txt = remove_lastname(txt)
    txt = remove_lastdot(txt)
    return txt

def remove_lastdot(txt):
    return txt[:-1]

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