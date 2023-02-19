import whisper

print("-> Loading model...")
model = whisper.load_model("base")
print("-> Done loading model...")

result = model.transcribe("audio.m4a")
print(result["text"])
