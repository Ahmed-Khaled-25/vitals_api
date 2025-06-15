from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import json
import groooooq




######### NOTEEE #########
# to run api run this file first main.py 
#by writing --> uvicorn main:app in vscode terminal
##########################




api_keys = [
    "akljnv13bvi2vfo0b0bmw"
]  # This is encryption key

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





###############################################################################


#information like name, age ...

@app.get("/patient_info", dependencies=[Depends(api_key_auth)])
async def read_root():
    Data = data["patient_info"]

    return {f"{Data}"}



###############################################################################


#all vitals includ ECG signals, O2 and temp.
#by passing day number and spesific hour needed the data will be sent

@app.get("/patient_vitals/day/{d_num}/hour/{h_num}", dependencies=[Depends(api_key_auth)])
async def read_root(d_num: int, h_num: int):
    day_number = d_num - 1
    hour_number = h_num - 1
    Data = data["patient_vitals"][day_number][f"day_{d_num}"][hour_number][f"hour_{h_num}"]

    return {f"{Data}"}



###############################################################################

#AI part

@app.get("/Ai/Ai_response", dependencies=[Depends(api_key_auth)])
async def reead_root():
    return {"AI_response": "MY AI root Works"}


@app.post("/Ai/receive_ai_text", dependencies=[Depends(api_key_auth)])
async def receive_ai_text(text_data: string):
    #print(f"Response from simple endpoint: {response_explicit.json()}")
    response = groooooq.get_groq_response(text_data)
    return {"AI_response": response}



###############################################################################

#Reciving data from arduino throw PC
@app.post("/post_temp", dependencies=[Depends(api_key_auth)])
async def receive_data(readings: dict):
    print(readings['temp_hw'])
    data['patient_vitals'][0]['day_1'][0]['hour_1'][2]['body_temprature'] = readings['temp_hw']
    json.dumps(data)
    print(data['patient_vitals'][0]['day_1'][0]['hour_1'][2]['body_temprature'])
    return {f"done"}

@app.post("/post_o2", dependencies=[Depends(api_key_auth)])
async def receive_data(readings: dict):
    print(readings['o2_level'])
    data['patient_vitals'][0]['day_1'][0]['hour_1'][2]['blood_o2_level'] = readings['o2_level']
    json.dumps(data)
    print(data['patient_vitals'][0]['day_1'][0]['hour_1'][2]['blood_o2_level'])
    return {f"done"}








###############################################################################

#Others reading for patient and ecg state
@app.get("/beat_per_min", dependencies=[Depends(api_key_auth)])
async def reead_bpm():
    Data = data["beat_per_min"]
    return {f"{Data}"}


@app.get("/ECG_reading", dependencies=[Depends(api_key_auth)])
async def reead_ecg():
    Data = data["ECG_reading"]
    return {f"{Data}"}


@app.get("/ECG_state", dependencies=[Depends(api_key_auth)])
async def reead_ecg_s():
    Data = data["ECG_state"]
    return {f"{Data}"}


