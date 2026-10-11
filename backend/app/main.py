from fastapi import FastAPI

# Make sure this variable is named 'app'
app = FastAPI(title="Budget Tracker API")

@app.get("/")
async def root():
    return {"status": "online"}