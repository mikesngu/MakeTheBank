from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_test_message():
    return {"message": "MakeTheBank wys we LIVE?"}