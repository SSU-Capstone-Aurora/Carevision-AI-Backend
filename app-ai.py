from fastapi import FastAPI

app = FastAPI()

@app.get('/ai-health')
def health_check():
    return {"I'm healthy!!!"}