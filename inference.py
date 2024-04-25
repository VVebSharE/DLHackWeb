from flask import Blueprint, request, jsonify, Flask, send_file, Response
from database import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import uuid
import os
import numpy as np
import base64

def model(img):
    return img


infer = Blueprint('infer', __name__)



@infer.route('/segmentImage', methods=['POST']) #save image if user is logged in other no
def segment_image():
    if "img" not in request.files:
        return "No image uploaded", 400

    image = request.files["img"]
    image_data = base64.b64encode(image.read())

    return jsonify({"image_data": image_data.decode("utf-8")})
