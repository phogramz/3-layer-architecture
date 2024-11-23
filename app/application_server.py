from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db import get_db_connection

app = FastAPI(title="Application Server API", version="1.0")

class NumberRequest(BaseModel):
    number: int

@app.post("/process-number")
async def process_number(data: NumberRequest):
    number = data.number
    if number <= 0:
        raise HTTPException(status_code=400, detail="Number must be a positive integer")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Получение текущих значений из таблицы 3lrar_received_numbers
            cursor.execute("SELECT received_number FROM public.\"3lrar_received_numbers\"")
            current_numbers = {row["received_number"] for row in cursor.fetchall()}

            # Проверка условий
            if number in current_numbers or (number + 1) in current_numbers:
                # Устанавливаем причину ошибки
                reason = (
                    "ситуация 1: значение уже имеется"
                    if number in current_numbers
                    else "ситуация 2: полученное значение на 1 меньше имеющегося"
                )

                # Логируем ошибку в таблицу 3lrar_history
                cursor.execute(
                    """
                    INSERT INTO public."3lrar_history" (received_number_id, result_status, result_desc)
                    VALUES (NULL, 'error', %s || ' ' || %s)
                    """,
                    (number, reason),
                )
                conn.commit()

                raise HTTPException(status_code=409, detail=reason)

            # Добавляем число в таблицу 3lrar_received_numbers
            cursor.execute(
                """
                INSERT INTO public."3lrar_received_numbers" (received_number)
                VALUES (%s)
                RETURNING id
                """,
                (number,),
            )
            new_id = cursor.fetchone()["id"]

            # Логируем успех в таблицу 3lrar_history
            cursor.execute(
                """
                INSERT INTO public."3lrar_history" (received_number_id, result_status, result_desc)
                VALUES (%s, 'success', %s)
                """,
                (new_id, number),
            )
            conn.commit()

        return {"message": "Number successfully added"}
    finally:
        conn.close()
