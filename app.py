import io
import json
from flask import Flask, request, jsonify
import extract_msg
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return jsonify({"error": "檔案過大，最大支援 100MB"}), 413

@app.route('/parse', methods=['POST'])
def parse_msg():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "請附上 'file' 欄位"}), 400
        
        file = request.files['file']
        if not file.filename.lower().endswith('.msg'):
            return jsonify({"error": "檔案格式錯誤，僅支援 .msg"}), 400
        
        msg_bytes = file.read()
        msg_stream = io.BytesIO(msg_bytes)
        
        try:
            msg = extract_msg.Message(msg_stream)
            subject = msg.subject or ""
            sender = msg.sender or ""
            to = msg.to or ""
            body = msg.body or ""
        except Exception as ex:
            return jsonify({"error": f"解析失敗: {str(ex)}"}), 400
        
        result = {
            "subject": subject,
            "sender": sender,
            "to": to,
            "body": body
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"內部錯誤: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
