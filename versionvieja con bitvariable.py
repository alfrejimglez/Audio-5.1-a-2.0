import os
import subprocess

def convertir_archivo(archivo):
    nombre_temporal = f"temp_{os.path.splitext(archivo)[0]}.mp4"
    nombre_final = f"{os.path.splitext(archivo)[0]}.mp4"
    
    comando = [
        "ffmpeg", "-i", archivo,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ac", "2",
        "-y", nombre_temporal
    ]
    
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

archivos = [f for f in os.listdir() if f.endswith((".mp4", ".mkv"))]

if not archivos:
    print("No se encontraron archivos MP4 o MKV en la carpeta.")
else:
    for archivo in archivos:
        convertir_archivo(archivo)
