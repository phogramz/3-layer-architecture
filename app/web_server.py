from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Web Server API", version="1.0")

class NumberRequest(BaseModel):
    number: int

@app.post("/process-number")
async def process_number(data: NumberRequest):
    number = data.number
    if number <= 0:
        raise HTTPException(status_code=400, detail="Number must be a positive integer")

    # Отправляем запрос на сервер приложений
    try:
        response = requests.post(
            "http://localhost:8001/process-number", json={"number": number}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as err:
        raise HTTPException(status_code=500, detail="Failed to connect to application server")
