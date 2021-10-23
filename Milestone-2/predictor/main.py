import uvicorn
from pydantic import BaseModel
from ml_utils import predict, init_app
from typing import List
from datetime import  datetime
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette import requests
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
# defining the main app
app = FastAPI(title="Credit Risk assessment", docs_url="/docs")
# app = FastAPI()
templates = Jinja2Templates(directory="views")
app.mount("/static", StaticFiles(directory="static"), name="static")
# calling the load_model during startup.
# this will train the model and keep it loaded for prediction.
# app.add_event_handler("startup", load_model)
app.add_event_handler("startup", init_app)

# class which is expected in the payload
class QueryIn(BaseModel):
    credit_amount: int


# class which is returned in the response
class QueryOut(BaseModel):
    risk: str


# Route definitions
@app.get("/ping")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"ping": "pong"}

@app.get("/")
def load_Home(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})


@app.post("/predictNews", status_code=200)
# Route to do the prediction using the ML model defined.
# Payload: QueryIn containing the parameters
# Response: QueryOut containing the flower_class predicted (200)
def predict_risk(
                request: Request,
                creditAmount: str = Form(...)):
    """ name = request.form['name'] """
    """  print(request) """
    print('news text:',creditAmount)
    # risk = predict(query_data)



    message = creditAmount
    color = "alert-success" 
    response_template ='<div class="'+color+' mb-0 py-1 ml-3 alert" style="font-weight:500" ' \
                      'role="alert">'+message+'</div>'
    return templates.TemplateResponse("predict.html", {
        "request": request,
        "prediction": response_template
    })



# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
