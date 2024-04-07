import websocket
import json
import matplotlib.pyplot as plt
from threading import Thread

# Lists to store data
x_data = []
y_data = []
z_data = []

def on_message(ws, message):
    values = json.loads(message)['values']
    x = values[0]
    y = values[1]
    z = values[2]
    print("x = ", x , "y = ", y , "z = ", z )
    
    # Append data to lists
    x_data.append(x)
    y_data.append(y)
    z_data.append(z)

def on_error(ws, error):
    print("error occurred ", error)
    
def on_close(ws, close_code, reason):
    print("connection closed : ", reason)
    
def on_open(ws):
    print("connected")

def connect(url):
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws_thread = Thread(target=ws.run_forever)
    ws_thread.daemon = True
    ws_thread.start()

def plot_data():
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    while True:
        if not x_data or not y_data or not z_data:  # Check if lists are empty
            continue
        ax.clear()
        ax.plot(x_data, label='X-axis')
        ax.plot(y_data, label='Y-axis')
        ax.plot(z_data, label='Z-axis')
        ax.legend()
        plt.pause(1)  # Pause to update the plot
        plt.savefig('plot.png')  # Save the plot as an image

connect("ws://192.168.189.93:8080/sensor/connect?type=android.sensor.accelerometer")
#connect("ws://192.168.189.93:8080/sensor/connect?type=android.sensor.step")

plot_data()
