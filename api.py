from fastapi import FastAPI
import json
from rotation import generate_rotation
from lua_seed_adapter import seed_from_worldstate

app = FastAPI()

with open("data/cetus_bounties.json") as f:
    BOUNTY_DATA = json.load(f)

@app.get("/cetus")
def get_cetus():
    seed = seed_from_worldstate({"timestamp": "auto"})
    rotation = generate_rotation(BOUNTY_DATA, seed)
    return {"seed": seed, "rotation": rotation}