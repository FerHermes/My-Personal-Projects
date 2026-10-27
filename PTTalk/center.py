import keyboard
import sounddevice as sd
import numpy as np
import wave
import os
import webbrowser
import whisper

samplerate = 44100
channels = 1
duration = 5

def grabar_audio(nombre_archivo="grabacion.wav"):
    print("🎙️ Grabando...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()
    print("✅ Grabación terminada")

    with wave.open(nombre_archivo, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())

    return nombre_archivo

def transcribir_audio(nombre_archivo):
    model = whisper.load_model("base")
    result = model.transcribe(nombre_archivo)
    return result["text"]

def ejecutar_accion(texto):
    texto = texto.lower()
    if "abrir word" in texto:
        os.system("start winword")
    elif "abrir excel" in texto:
        os.system("start excel")
    elif "abrir bloc de notas" in texto:
        os.system("notepad")
    elif "buscar" in texto:
        consulta = texto.replace("buscar", "").strip()
        url = f"https://www.bing.com/search?q={consulta}"
        webbrowser.open(url)
    else:
        print("⚡ No se reconoció una acción específica.")

print("Presiona Ctrl+F para hablar...")

while True:
    if keyboard.is_pressed("ctrl+f"):
        archivo = grabar_audio()
        texto = transcribir_audio(archivo)
        print(f"📝 Texto reconocido: {texto}")
        ejecutar_accion(texto)
        keyboard.wait("ctrl+f", suppress=False)