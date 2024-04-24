from flask import Flask, request, jsonify
from auth import auth
from inference import infer
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from database import db


load_dotenv()

app = Flask(__name__)


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(infer, url_prefix='/infer')



app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)  

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'}), 200


socketio = SocketIO(app)

@socketio.on('segmentImage')
def segment_image_socket(data):
    image = data['image']
    
    result = image
    
    socketio.emit('segmentedImage', result)

if __name__ == '__main__':
    app.run(debug=True)

