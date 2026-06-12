# Actividad 3: detección de anomalías en paneles solares

Proyecto local de fine-tuning de YOLOv5 para las clases `cover`, `crack`,
`dust` y `normal`.

## Inicio rápido en Windows

1. Ejecuta `iniciar_notebook_local.bat`.
2. En Jupyter abre `YOLOv5_alumnos.ipynb`.
3. Ejecuta las celdas en orden.

## Clonar desde GitHub

```bash
git clone https://github.com/Cesarin152/yolov5-paneles-solares.git
cd yolov5-paneles-solares
```

Después ejecuta `instalar_entorno_local.bat` y
`iniciar_notebook_local.bat`.

El proyecto ya incluye:

- Entorno virtual `.venv`.
- Repositorio oficial YOLOv5 en `vendor/yolov5`.
- Dataset validado en `data/solar_panels`.
- Notebook configurado con rutas locales automáticas.

Este equipo no presenta una GPU NVIDIA detectable. El notebook seleccionará
`cpu`; el entrenamiento completo de 50 épocas funcionará, pero puede tardar
muchas horas. Para verificar rápidamente la instalación ejecuta
`probar_proyecto_local.bat`.

## Recrear el entorno

Si se mueve el proyecto a otro equipo:

1. Ejecuta `instalar_entorno_local.bat`.
2. Después ejecuta `iniciar_notebook_local.bat`.

## Parámetros de entrenamiento

En el notebook puedes cambiar:

- `BATCH_SIZE`: 16 por defecto; reduce a 8 o 4 si hay falta de memoria.
- `EPOCHS`: 50, según la actividad.
- `IMG_SIZE`: 640.

## Dataset

- Entrenamiento: 1.598 imágenes.
- Validación: 456 imágenes.
- Prueba: 226 imágenes.
- Cero imágenes dañadas, etiquetas inválidas o grupos fuente compartidos.

Fuente: Solar Panel, Roboflow Universe, licencia CC BY 4.0:
https://universe.roboflow.com/workshop-pydqh/solar-panel-0swal-vrqxd-seo7f/dataset/1
