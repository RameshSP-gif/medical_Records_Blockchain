import os
from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from blockchain import Blockchain

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secretkey'

blockchain = Blockchain()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files, chain=blockchain.to_dict())

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        blockchain.add_block({
            "action": "create",
            "filename": filename
        })
        flash(f"{filename} uploaded successfully.")
    return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)
        blockchain.add_block({
            "action": "delete",
            "filename": filename
        })
        flash(f"{filename} deleted successfully.")
    return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/blockchain')
def view_blockchain():
    return jsonify(blockchain.to_dict())

# 🔥 Railway-compatible startup
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Railway's PORT or fallback to 5000
    app.run(host='0.0.0.0', port=port)
