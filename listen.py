import subprocess
import whisper
import re
import tempfile

fd, path =tempfile.mkstemp(suffix = '.mp3')

def undo(text):
    sentences = text.split(".")
    i = 0
    filtered_sentences = []

    while i < len(sentences):
        sentence = sentences[i]
        words = sentence.split()
        filtered_words = []

        ii = 0
        while ii < len(words):
            word = words[ii]
            filtered_words.append(word)

            if word.lower() not in [ "undo", "fuck" ]:
                ii += 1
                continue

            next_word = words[ii + 1]

            if next_word == "sentence":
                filtered_sentences.pop()
                filtered_words = []
                break
            else:
                filtered_words.pop() # pop the undo
                if len(filtered_words) > 0:
                    filtered_words.pop() # pop the undoed word

            ii += 1


        if len(filtered_words) > 0:
            filtered_sentences.append(" ".join(filtered_words))

        i += 1                

    return ". ".join(filtered_sentences)

def copy(t):
    t = t.replace('"', "\"")
    subprocess.run(f'echo "{t}" | pbcopy', shell=True)

def stream_record():
    subprocess.run(f"time ffmpeg -loglevel info -f avfoundation -i ':0' -sample_rate 48000 -b:a 320k {path} -y", shell=True);   

def consume_result(result):
    text = result["text"]
    print("\n[LISTEN] Here's what you said:\n")
    print(text)

    print("\n[LISTEN] Here's the processed version:\n ")
    text = undo(text)
    print(text)

    copy(text)
    print("\n[LISTEN] copied to clipboard")

print("[LISTEN] Speak. Press [q] when you're done")
print("[LISTEN] Loading model...")
model = whisper.load_model("base")

print(f"[LISTEN] Init recorder. Will temporary save recording to {path}")
stream_record()

print("[LISTEN] Transcribing...")
result = model.transcribe(path)
consume_result(result)

print(f"[LISTEN] Done. Purging {path}")
subprocess.run(f'rm "{path}"', shell=True)
