import os
import subprocess

def convertir_archivo(archivo):
    nombre_temporal = f"temp_{os.path.splitext(archivo)[0]}.mp4"
    nombre_final = f"{os.path.splitext(archivo)[0]}.mp4"
    
    comando = [
        "ffmpeg", "-i", archivo,
        "-c:v", "copy",              # Copiar video sin recodificar
        "-c:a", "aac", "-ac", "2",   # Convertir audio a AAC 2.0
        "-q:a", "2",                 # Calidad variable (mejor compresión que -b:a fijo)
        "-y", nombre_temporal        # Guardar en nombre temporal
    ]
    
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linea in proceso.stdout:
        print(linea, end="")
    proceso.wait()
    
    if os.path.exists(nombre_temporal):  # Verificar que la conversión fue exitosa
        os.remove(archivo)  # Borrar archivo original
        os.rename(nombre_temporal, nombre_final)  # Renombrar archivo temporal al nombre final
        print(f"Convertido: {nombre_final} y eliminado el original {archivo}")
    else:
        print(f"Error en la conversión de {archivo}, archivo original no eliminado.")

# Obtener archivos MP4 y MKV en el directorio actual
archivos = [f for f in os.listdir() if f.endswith((".mp4", ".mkv"))]

if not archivos:
    print("No se encontraron archivos MP4 o MKV en la carpeta.")
else:
    for archivo in archivos:
        convertir_archivo(archivo)
