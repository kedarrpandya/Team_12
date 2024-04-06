import websocket
import json
from flask_socketio import SocketIO
#import app
from app import socketio,app




socketio = SocketIO(app, async_mode='threading' , cors_allowed_originals="*")

def on_message(ws, message):

    try:
        
        data = json.loads(message)
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        altitude = data.get('altitude')
        bearing = data.get('bearing')
        accuracy = data.get('accuracy')
        speed = data.get('speed')
        time = data.get('time')

        print("Longitude = ", longitude, "Latitude = ", latitude, "Altitude = ", altitude,
              "Bearing = ", bearing, "Accuracy =", accuracy, "Speed = ", speed, "Time = ", time)
        

    except json.JSONDecodeError as e:
        print("JSON decoding error: ", e)
    except KeyError as e:
        print("Missing key in JSON data: ", e)
    except Exception as e:
        print("An error occurred: ")
    
    socketio.emit('gps_data', {
            'longitude': data.get('longitude'),
            'latitude': data.get('latitude'),
            'altitude': data.get('altitude'),
            'bearing': data.get('bearing'),
            'accuracy': data.get('accuracy'),
            'speed': data.get('speed'),
            'time': data.get('time')
        })


    
                               
def on_error(ws, error):
    print("error occurred ", error)
    
def on_close(ws, close_code, reason):
    print("connection closed : ", reason)
    
def on_open(ws):
    print("connected")
def process_gps_data(socketio):
    def on_message(ws, message):
        try:
            data = json.loads(message)
            socketio.emit('gps_update', {'longitude': data.get('longitude'), 'latitude': data.get('latitude')})
        except Exception as e:
            print("An error occurred: ", e)

    

def connect(url):
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
 
 
connect("ws://192.168.189.93:8080/gps")
