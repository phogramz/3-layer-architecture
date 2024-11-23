from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Application Server API")

# Модель данных для запроса
class Numbers(BaseModel):
    num1: int
    num2: int

@app.post("/process/")
async def process_numbers(numbers: Numbers):
    total = numbers.num1 + numbers.num2

    # Проверка суммы
    if total >= 10:
        raise HTTPException(status_code=409, detail="Сумма чисел должна быть меньше 10")

    return {"result": total}
