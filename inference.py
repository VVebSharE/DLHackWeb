from flask import Blueprint, request, jsonify, Flask, send_file, Response
from database import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import uuid
import os
import cv2
import numpy as np
import base64

def model(img):
    return img


infer = Blueprint('infer', __name__)


def dummy_segmentation(image_data):
    # Convert image data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Dummy segmentation (convert to grayscale)
    gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # Convert back to bytes
    _, segmented_img_data = cv2.imencode(".png", gray_img)
    segmented_img_bytes = segmented_img_data.tobytes()

    return segmented_img_bytes


@infer.route('/segmentImage', methods=['POST']) #save image if user is logged in other no
def segment_image():
    if "img" not in request.files:
        return "No image uploaded", 400

    image = request.files["img"]
    image_data = base64.b64encode(image.read())

    return jsonify({"image_data": image_data.decode("utf-8")})
