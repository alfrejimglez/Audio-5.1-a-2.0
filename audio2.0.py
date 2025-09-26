import os
import subprocess
import json

def obtener_streams_audio(archivo):
    comando = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", archivo
    ]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(resultado.stdout)
    return [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]

def calcular_bitrate_estereo(bitrate_original, channels):
    if channels >= 6:
        bitrate_estereo = int((bitrate_original / channels) * 2)
    else:
        bitrate_estereo = int(bitrate_original)
    return max(64000, min(192000, bitrate_estereo))

def convertir_archivo(archivo):
    audio_streams = obtener_streams_audio(archivo)
    if not audio_streams:
        print(f"No se encontraron streams de audio en {archivo}")
        return

    comando = ["ffmpeg", "-i", archivo]
    # Mapear video
    comando += ["-map", "0:v"]
    # Mapear y procesar cada stream de audio
    for idx, stream in enumerate(audio_streams):
        comando += ["-map", f"0:a:{idx}"]

    # Copiar video
    comando += ["-c:v", "copy"]

    # Procesar audio streams
    for idx, stream in enumerate(audio_streams):
        bit_rate = int(stream.get("bit_rate", 192000))
        channels = int(stream.get("channels", 2))
        codec = stream.get("codec_name", "")

        if codec != "aac" or channels != 2:
            bitrate_estereo = calcular_bitrate_estereo(bit_rate, channels)
            comando += [f"-c:a:{idx}", "aac", f"-b:a:{idx}", str(bitrate_estereo), "-ac", "2"]
        else:
            comando += [f"-c:a:{idx}", "copy"]

    nombre_temporal = f"temp_{os.path.splitext(archivo)[0]}.mp4"
    nombre_final = f"{os.path.splitext(archivo)[0]}.mp4"
    comando += ["-y", nombre_temporal]

    print("Ejecutando:", " ".join(comando))
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linea in proceso.stdout:
        print(linea, end="")
    proceso.wait()

    if os.path.exists(nombre_temporal):
        os.remove(archivo)
        os.rename(nombre_temporal, nombre_final)
        print(f"Convertido: {nombre_final} y eliminado el original {archivo}")
    else:
        print(f"Error en la conversión de {archivo}, archivo original no eliminado.")

archivos = [f for f in os.listdir() if f.endswith((".mp4", ".mkv", ".mka"))]

if not archivos:
    print("No se encontraron archivos MP4, MKV o MKA en la carpeta.")
else:
    for archivo in archivos:
        convertir_archivo(archivo)