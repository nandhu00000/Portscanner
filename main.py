from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import socket
import uvicorn

app = FastAPI()

# Make sure index.html is inside a folder named "templates"
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": None
        }
    )


@app.post("/scan", response_class=HTMLResponse)
async def scan(request: Request, ip: str = Form(...)):
    ports = [22, 80, 443]
    results = []

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            result = sock.connect_ex((ip, port))

            status = "OPEN" if result == 0 else "CLOSED"

            results.append({
                "port": port,
                "status": status
            })

            sock.close()

        except Exception as e:
            print(f"Error scanning port {port}: {e}")

            results.append({
                "port": port,
                "status": "ERROR"
            })

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "ip": ip,
            "results": results
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )