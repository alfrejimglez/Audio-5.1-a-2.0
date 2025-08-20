import os
import subprocess
import json

def obtener_bitrate(archivo):
    comando = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-select_streams", "a:0", archivo
    ]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(resultado.stdout)
    if "streams" in info and len(info["streams"]) > 0 and "bit_rate" in info["streams"][0]:
        return int(info["streams"][0]["bit_rate"])
    return 192000  # valor por defecto si no se detecta

def convertir_archivo(archivo):
    bitrate_original = obtener_bitrate(archivo)
    bitrate_estereo = int((bitrate_original / 6) * 2)  # de 5.1 (6 canales) a 2.0 (2 canales)
    if bitrate_estereo < 64000:
        bitrate_estereo = 64000
    if bitrate_estereo > 192000:
        bitrate_estereo = 192000

    nombre_temporal = f"temp_{os.path.splitext(archivo)[0]}.mp4"
    nombre_final = f"{os.path.splitext(archivo)[0]}.mp4"
    
    comando = [
        "ffmpeg", "-i", archivo,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", str(bitrate_estereo), "-ac", "2",
        "-y", nombre_temporal
    ]
    
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linea in proceso.stdout:
        print(linea, end="")
    proceso.wait()
    
    if os.path.exists(nombre_temporal):
        os.remove(archivo)
        os.rename(nombre_temporal, nombre_final)
        print(f"Convertido: {nombre_final} con bitrate {bitrate_estereo/1000:.0f} kbps y eliminado el original {archivo}")
    else:
        print(f"Error en la conversión de {archivo}, archivo original no eliminado.")

archivos = [f for f in os.listdir() if f.endswith((".mp4", ".mkv"))]

if not archivos:
    print("No se encontraron archivos MP4 o MKV en la carpeta.")
else:
    for archivo in archivos:
        convertir_archivo(archivo)
