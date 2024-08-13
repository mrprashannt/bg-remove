from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img = Image.open(file.stream)
    except IOError:
        return jsonify({'error': 'Invalid image file'}), 400

    output = remove(img)
    img_io = io.BytesIO()
    output.save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='processed_image.png')

if __name__ == '__main__':
    app.run(debug=True)