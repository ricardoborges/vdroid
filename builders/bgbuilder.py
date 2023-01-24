import providers.articleprovider as articleprovider
import providers.voiceprovider as voiceprovider
import services.videoservice as videoservice

def run(name, english):
    print("[creating boardgame rules...]")

    rules = articleprovider.generateRules(name, english)

    f = open("rules.txt", "w")
    f.write(rules)
    f.close()

    print("[creating voice...]")
    voiceprovider.createVoiceOver(rules, "_output/bg/rules.mp3", english)
    videoservice.createVideo("_output/bg/rules.mp3", "catan.jpg")

