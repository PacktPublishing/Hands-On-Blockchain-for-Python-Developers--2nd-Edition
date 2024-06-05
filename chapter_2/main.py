from fastapi import FastAPI
import os

app = FastAPI()

counter_file = "counter.txt"

counter = 0

@app.get("/")
async def root():
    global counter
    if os.path.isfile(counter_file):
        with open(counter_file, "r") as f:
            try:
                counter = int(f.read().strip())
            except ValueError:
                counter = 0
    counter += 1
    with open(counter_file, "w") as f:
        f.write(str(counter))
    return {"counter": counter}
