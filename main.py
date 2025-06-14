from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import base64
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Pixel Avatar API!'

@app.route('/generate', methods=['POST'])
def generate_pixel_avatar():
    data = request.json
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    try:
        # 解码 base64 图像
        image_data = base64.b64decode(data['image'].split(',')[-1])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')

        # 像素化处理
        pixel_size = 32
        image = image.resize((pixel_size, pixel_size), Image.NEAREST)
        image = image.resize((256, 256), Image.NEAREST)

        # 保存图像
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join("/tmp", filename)
        image.save(filepath)

        return send_file(filepath, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
