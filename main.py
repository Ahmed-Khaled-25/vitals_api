from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import json
from mqesp_subscriber import start_mqtt, latest_data




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



#with open('patient_vitals_data.json') as json_file:
#    data = json.load(json_file)




app = FastAPI()

mqtt_client = start_mqtt()



###############################################################################


#information like name, age ...

@app.get("/patient_info", dependencies=[Depends(api_key_auth)])
async def read_root():
    #Data = data["patient_info"]
    Data = latest_data["payload"]
    print(Data)
    return {f"{Data}"}

