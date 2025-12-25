import paho.mqtt.client as mqtt
import ssl
import json

# Connection details
MQTT_BROKER = "fe1df1d124e943fd804cd457eaad464b.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "esp_esp"
MQTT_PASSWORD = "Ahmed1234"
MQTT_CLIENT_ID = "PythonSubscriber_54321"
MQTT_SUBSCRIBE_TOPIC = "esp8266/data/sensor1"

# 1. This variable will hold the data that your API file will read
latest_data = {"payload": None}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(MQTT_SUBSCRIBE_TOPIC)
    else:
        print(f"❌ Failed to connect, code {rc}")

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode()
    
    # 2. Update the shared variable instead of returning it
    latest_data["payload"] = payload_str
    
    print(f"New Message Received: {payload_str}")

# 3. Wrap everything in a function that your main file can call
def start_mqtt():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    print(f"Connecting to HiveMQ...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # 4. Use loop_start() instead of loop_forever()
    # This creates a background thread so your API can keep running
    client.loop_start()
    return client


#start_mqtt()