import socket
import os
import threading
import json
from flask import Flask, render_template, request, redirect
from datetime import datetime

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'storage', 'data.json')

app = Flask(__name__)


def save_to_json(data):
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = {}
    timestamp = str(datetime.now())
    existing_data[timestamp] = data
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(existing_data, file, indent=4)



def send_data_to_socket(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    try:
        sock.sendto(json.dumps(data).encode('utf-8'), ('localhost', 5000))
    finally:
        sock.close()


def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))
    print("Socket server is running on port 5000...")

    while True:
        data,addr = server_socket.recvfrom(1024) 
        decoded_data = json.loads(data.decode('utf-8'))  
        save_to_json(decoded_data)        
        
def run_flask():
    app.run(debug=True, port=3000)

    
@app.route('/')
def render_homepage():
    return render_template('index.html')



@app.route('/message',methods=['GET','POST'])
def render_message_page():
    if request.method == 'GET':
        return render_template('message.html')
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('message')
        send_data_to_socket({'username': username, 'message': message})
        return redirect('/message')


@app.errorhandler(404)
def page_not_found(exc):
    return render_template('error.html'),404


if __name__ == "__main__":
    socket_thread = threading.Thread(target=socket_server)
    socket_thread.start()
    run_flask()
    socket_thread.join()