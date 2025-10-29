from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

class TextIn(BaseModel):
    text: str

# Debido a temas de espacio en Github, cargamos el modelo en Hugging Face Hub
model= "jeanpzh/ner" 

loaded_model = AutoModelForTokenClassification.from_pretrained(model)
loaded_tokenizer = AutoTokenizer.from_pretrained(model)

# Crear el pipeline de NER con el modelo y tokenizer cargados
ner_pipeline = pipeline(
    "token-classification",
    model=loaded_model,
    tokenizer=loaded_tokenizer,
    aggregation_strategy="simple" 
)

app = FastAPI(
    title="API de Reconocimiento de Entidades (NER)",
    description="Una API para encontrar Químicos y Enfermedades en texto usando un modelo BioBERT."
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/predict")
def predict(item: TextIn):
    """
    Recibe un texto y devuelve las entidades (Químicos, Enfermedades) encontradas.
    """
    try:

        results = ner_pipeline(item.text)
        
        # Results devuelve una lista de diccionarios con las entidades encontradas, por ello debemos limpiarlo antes de retornarlo al usuario
        clean_results = []
        for entity in results:
            clean_results.append({
                "entity_group": entity["entity_group"],
                "score": float(entity["score"]),  
                "word": entity["word"],
                "start": int(entity["start"]),
                "end": int(entity["end"])
            })

        return {"predictions": clean_results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def root():
    return {"message": "API de NER está funcionando. Usa el endpoint POST /predict."}

if __name__ == "__main__":
    print("Iniciando servidor Uvicorn en http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)

