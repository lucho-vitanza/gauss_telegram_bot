import whisper

def translator(audio_file):

    try:
        model = whisper.load_model("base")
        result= model.transcribe(audio_file)
        transcripction = result["text"]

        
    except Exception as e:
        raise 
    