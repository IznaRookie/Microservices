import os
import random
import requests
import uvicorn as uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    r_id = random.randint(1, 54)
    r = requests.get(f"https://books-api7.p.rapidapi.com/books/{r_id}?&rapidapi-key=da49fae300mshebbea2dd9d3366ep1b564bjsn07af1562a9d7")
    return r.json()

@app.get("/list/")
async def get_list(q: list | None = Query()):
    book_list = []
    for id in q:
        r = requests.get(f"https://books-api7.p.rapidapi.com/books/{id}?&rapidapi-key=da49fae300mshebbea2dd9d3366ep1b564bjsn07af1562a9d7")
        book_list.append(r.json())
    return book_list

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))