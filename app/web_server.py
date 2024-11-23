from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

app = FastAPI(title="Web Server API")

# Модель данных для запроса
class Numbers(BaseModel):
    num1: int = Field(..., title="Первое число", description="Целое число")
    num2: int = Field(..., title="Второе число", description="Целое число")

@app.post("/add/")
async def add_numbers(numbers: Numbers):
    # Передаем данные на сервер приложений
    try:
        response = requests.post("http://127.0.0.1:8001/process/", json=numbers.dict())
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Unknown error"))
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Ошибка связи с сервером приложений")

    return {"result": response.json()["result"]}
