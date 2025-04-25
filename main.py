from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import json


api_keys = [
    "akljnv13bvi2vfo0b0bmw"
]  # This is encrypted in the database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )



with open('patient_vitals_data.json') as json_file:
    data = json.load(json_file)




app = FastAPI()

@app.get("/patient_info", dependencies=[Depends(api_key_auth)])
async def read_root():
    Data = data["patient_info"]

    return {f"{Data}"}
            


@app.get("/patient_vitals/{day_num}/{d_num}/{hour_num}/{h_num}", dependencies=[Depends(api_key_auth)])
async def read_root(day_num: str, d_num: int, hour_num: str, h_num: int):
    day_number = d_num - 1
    #day_path = day_num + "_" + str(d_num)
    hour_number = h_num - 1
    #hour_path = day_num + "_" + str(h_num)
    
    Data = data["patient_vitals"][day_number][f"day_{d_num}"][hour_number][f"hour_{h_num}"]

    return {f"{Data}"}





@app.get("/Ai", dependencies=[Depends(api_key_auth)])
async def reead_root():
    return {"AI_response": "MY AI root Works"}


@app.post("/Ai/receive_ai_text", dependencies=[Depends(api_key_auth)])
async def receive_ai_text(text_data: str):
    #print(f"Response from simple endpoint: {response_explicit.json()}")

    return {"message": f"Received text (simple): {text_data}"}