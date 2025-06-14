from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import base64
import os
import uuid
import random
from datetime import datetime

app = Flask(__name__)

# ✅ 随机罪名列表（可扩展）
CRIMES = [
    "凌晨三点还在debug，影响他人休息",
    "上传自拍假装AI图，被识破",
    "CSS命名为final_final_use_this_one",
    "连续三天吃泡面还说自己很健康",
    "偷偷用console.log debug被发现",
    "Star了自己的项目",
    "上班摸鱼被举报",
    "写了5年还分不清==和===",
    "删库跑路未遂",
    "偷偷在注释里写脏话",
]

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

        # ✅ 1. 像素化处理
        pixel_size = 32
        image = image.resize((pixel_size, pixel_size), Image.NEAREST)
        image = image.resize((256, 256), Image.NEAREST)

        # ✅ 2. 加载随机通缉照背景图（必须放在 assets/wanted_bg/）
        bg_dir = "assets/wanted_bg"
        bg_files = [f for f in os.listdir(bg_dir) if f.endswith('.png')]
        if not bg_files:
            raise Exception("没有找到任何通缉背景图，请在 assets/wanted_bg/ 中放置 PNG 文件")

        bg_path = os.path.join(bg_dir, random.choice(bg_files))
        bg = Image.open(bg_path).convert("RGBA").resize((256, 300))

        # ✅ 3. 合成像素头像到背景上
        bg.paste(image, (0, 0))

        # ✅ 4. 添加罪名文字
        draw = ImageDraw.Draw(bg)
        try:
            font = ImageFont.truetype("assets/SmileySans-Oblique.ttf", size=28)
        except:
            font = ImageFont.load_default()

        crime = random.choice(CRIMES)
        date = datetime.now().strftime("%Y-%m-%d")

        draw.text((10, 260), f"📝 罪名：{crime}", fill="black", font=font)
        draw.text((10, 280), f"📆 报道时间：{date}", fill="gray", font=font)

        # ✅ 5. 保存文件
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join("/tmp", filename)
        bg.save(filepath)

        return send_file(filepath, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Railway 启动服务
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
