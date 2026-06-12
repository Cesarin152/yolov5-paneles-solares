# Actividad 3: detección de anomalías en paneles solares

Fine-tuning de YOLOv5 para detectar las clases `cover`, `crack`, `dust` y
`normal`.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Cesarin152/yolov5-paneles-solares/blob/main/YOLOv5_alumnos.ipynb)

## Ejecución

Todo el proyecto se ejecuta desde un único notebook:
`YOLOv5_alumnos.ipynb`.

1. Abre el notebook con el botón **Abrir en Colab**.
2. Selecciona **Entorno de ejecución > Cambiar tipo de entorno de ejecución >
   GPU**.
3. Ejecuta las celdas en orden o usa **Ejecutar todas**.

La primera celda de código clona automáticamente este repositorio en
`/content/ProyectoYOLOv5`, descarga una versión fijada de YOLOv5 oficial, instala sus
dependencias y obtiene los pesos preentrenados `yolov5s.pt`. No es necesario
editar rutas ni subir manualmente el dataset.

## Flujo del notebook

- Validación de GPU y preparación del entorno.
- Comprobación del dataset y generación del archivo YAML.
- Visualización de ejemplos anotados.
- Entrenamiento de YOLOv5s durante 50 épocas.
- Informe de métricas y evaluación sobre el conjunto de prueba.
- Inferencia y visualización de predicciones.

## Parámetros de entrenamiento

- `IMG_SIZE = 640`
- `BATCH_SIZE = 16`
- `EPOCHS = 50`

Reduce `BATCH_SIZE` a 8 o 4 si Colab informa falta de memoria de GPU.

## Dataset

- Entrenamiento: 1.598 imágenes.
- Validación: 456 imágenes.
- Prueba: 226 imágenes.
- Clases: `cover`, `crack`, `dust`, `normal`.

Fuente: [Solar Panel, Roboflow Universe](https://universe.roboflow.com/workshop-pydqh/solar-panel-0swal-vrqxd-seo7f/dataset/1),
licencia CC BY 4.0.

Los pesos, entornos virtuales, resultados, cachés y el clon local de YOLOv5
permanecen fuera de Git mediante `.gitignore`.
