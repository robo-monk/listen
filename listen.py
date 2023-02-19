import subprocess
import whisper

def copy(t):
    subprocess.run(f"echo '{t}' | pbcopy", shell=True)

def stream_record():
    subprocess.run("ffmpeg -loglevel info -f avfoundation -i ':0' -sample_rate 48000 -b:a 320k output.mp3 -y", shell=True);   

def consume_result(result):
    text = result["text"]
    print("\n[LISTEN] Here's what you said:\n")
    print(text)
    copy(text)
    print("\n[LISTEN] copied to clipboard -")

print("-> [LISTEN] Loading model...")
model = whisper.load_model("base")

print("-> [LISTEN] Init recorder...")
stream_record()

print("-> [LISTEN] Transcribing...")
result = model.transcribe("output.mp3")
consume_result(result)
