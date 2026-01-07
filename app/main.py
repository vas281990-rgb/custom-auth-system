from fastapi import FastAPI

app = FastAPI(title="Custom Auth System")

@app.get("/")
def health_check():
    return {"status": "ok"}
