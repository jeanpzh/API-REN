# NER API

Esta es una API simple construida con **FastAPI** que utiliza un modelo preentrenado (basado en BioBERT) para realizar Reconocimiento de Entidades Nombradas (NER).

Específicamente, está diseñada para identificar entidades de **Químicos** (CHEMICAL) y **Enfermedades** (DISEASE) en un texto dado.

## Tecnologías

* **Python 3.10**
* **FastAPI:** Para el servidor web.
* **Hugging Face `transformers`:** Para cargar el modelo y ejecutar el pipeline de NER.
* **Pydantic:** Para la validación de datos de entrada.
* **Docker:** Para la contenedorización.


## Ejecución Local

1.  **Clonar el repositorio** (o asegurarse de tener los archivos).
2.  **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (En Windows: venv\Scripts\activate)
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Colocar el modelo:** Asegurarse de que el modelo entrenado esté en una carpeta llamada `./ner_model` en la raíz del proyecto.
5.  **Iniciar el servidor:**
    ```bash
    uvicorn app:app --reload
    ```
El servidor estará disponible en `http://127.0.0.1:8000`.

