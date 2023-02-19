import subprocess
import ffmpeg 
import whisper


def stream_record():
    subprocess.run("ffmpeg -f avfoundation -i ':0' output.mp3 -y", shell=True);   

print("-> Loading model...")
model = whisper.load_model("base")
print("-> Done loading model...")

stream_record()

result = model.transcribe("output.mp3")
print(result["text"])
