import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

import pymongo
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.pipeline.training_pipeline import TrainingPipline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from Networksecurity.utils.main_utils.utils import load_object
from Networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from Networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from Networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Load the input data
        df = pd.read_csv(file.file)

        # Load the preprocessor and trained model
        preprocessor = load_object("final_model/preprocessor.pkl")
        trained_model = load_object("final_model/model.pkl")

        # Create the NetworkModel object
        network_model = NetworkModel(preprocessor=preprocessor, model=trained_model)

        # Make predictions
        y_pred = network_model.predict(df)

        # Add predictions to the DataFrame
        df['predicted_column'] = y_pred

        # Save the predictions to a CSV file
        df.to_csv('prediction_output/output.csv')

        # Convert the DataFrame to an HTML table
        table_html = df.to_html(classes='table table-striped')

        # Return the HTML table as a response
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    


if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)