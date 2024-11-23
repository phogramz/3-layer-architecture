import uvicorn
from multiprocessing import Process

def run_web_server():
    from app.web_server import app
    uvicorn.run(app, host="127.0.0.1", port=8000)

def run_application_server():
    from app.application_server import app
    uvicorn.run(app, host="127.0.0.1", port=8001)

if __name__ == "__main__":
    # Запуск серверов в разных процессах
    web_server_process = Process(target=run_web_server)
    application_server_process = Process(target=run_application_server)

    web_server_process.start()
    application_server_process.start()

    print("Оба сервера запущены.")
    print("Swagger для веб-сервера доступен по адресу: http://127.0.0.1:8000/docs")
    print("Swagger для сервера приложений доступен по адресу: http://127.0.0.1:8001/docs")

    # Ожидание завершения процессов
    web_server_process.join()
    application_server_process.join()
