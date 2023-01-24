import azure.cognitiveservices.speech as speechsdk
import scope

key = "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"

def renderAudio(text, name, voicename):
    speech_key = "726c5178ff724ac2a936950de3f90525"
    service_region = "brazilsouth"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = voicename

    audio_output = speechsdk.audio.AudioOutputConfig(filename=name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #print("Speech synthesized for text [{}]".format(text))
        print("[voice created]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def createVoiceOver(text, options):
    if (options['english'] == 'True'):
        voicename = "en-US-BrandonNeural"
    else:
        voicename = "pt-BR-AntonioNeural"
        #voicename = "pt-BR-BrendaNeural"

    if (options['single'] == 'True'):
        #scope.script['singleaudiopath'] = f"_output/{options['folder']}/{options['folder']}.mp3"
        renderAudio(text, scope.audiopath_single, voicename)
        return

    list = text.split(".")

    i=1
    for item in list:
        renderAudio(item, f"{scope.basedir}/audio-{i}.mp3", voicename)
        i+=1

    
def createSingleVoiceOver(text, options):
    if (options['english'] == 'True'):
        voicename = "en-US-BrandonNeural"
    else:
        voicename = "pt-BR-AntonioNeural"

    renderAudio(text, scope.audiopath_single, voicename)
