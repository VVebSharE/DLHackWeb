from flask import Blueprint, request, jsonify, Flask, send_file, Response
from database import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import uuid
import os
import numpy as np
import base64
from PIL import Image
from io import BytesIO

from Model.model import ImageSegmenter

segmenter = ImageSegmenter('fcn_resnet50')

def model(image_data: Image) -> Image:
    return segmenter.segment_image(image_data)


infer = Blueprint('infer', __name__)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@infer.route('/segmentImage', methods=['POST']) #save image if user is logged in other no
def segment_image():
    if "img" not in request.files:
        return "No image uploaded", 400

    image = request.files["img"]
    image_pil = Image.open(image)
    mask= model(image_pil)


    return serve_pil_image(mask)
