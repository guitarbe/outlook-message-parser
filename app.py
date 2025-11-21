import os
import logging
from flask import Flask, request, jsonify
import extract_msg

# 初始化 Flask 應用
app = Flask(__name__)

# --- 設定與配置 ---
# 設定最大上傳限制為 100MB (以 Bytes 為單位)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# 設定日誌 (Logging)
logging.basicConfig(level=logging.INFO)
logger = app.getLogger(__name__)

@app.route('/parse', methods=['POST'])
def parse_msg():
    """
    接收 .msg 檔案並回傳解析後的 JSON 資料。
    不進行硬碟存取，全記憶體處理。
    """
    try:
        # 1. 檢查是否有檔案部分
        if 'file' not in request.files:
            logger.warning("Request missing 'file' part")
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        # 2. 檢查檔名是否為空
        if file.filename == '':
            logger.warning("No selected file")
            return jsonify({'error': 'No selected file'}), 400

        # 3. 使用 extract-msg 進行記憶體內解析
        # file.stream 是 Werkzeug 的 FileStorage 物件，extract-msg 可直接讀取
        try:
            msg = extract_msg.openMsg(file.stream)
        except Exception as e:
            logger.error(f"Failed to open/parse msg file: {str(e)}")
            return jsonify({'error': 'Invalid .msg file format or corrupted file'}), 400

        # 4. 提取所需欄位
        # 使用 getattr 或預設值以防欄位缺失
        parsed_data = {
            'subject': getattr(msg, 'subject', '') or '(No Subject)',
            'sender': getattr(msg, 'sender', '') or '(Unknown Sender)',
            'to': getattr(msg, 'to', '') or '(No Receivers)',
            'body': getattr(msg, 'body', '') or ''
        }

        # 5. 資源清理 (雖然 Python 有 GC，但明確關閉是好習慣)
        msg.close()

        logger.info(f"Successfully parsed: {file.filename}")
        return jsonify(parsed_data), 200

    except Exception as e:
        # 捕捉所有未預期的伺服器錯誤
        logger.error(f"Unexpected server error: {str(e)}", exc_info=True)
        return jsonify({'error': f"Internal Server Error: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def health_check():
    """
    簡單的健康檢查端點，確保服務活著
    """
    return jsonify({'status': 'ok', 'service': 'outlook-msg-parser'}), 200

if __name__ == '__main__':
    # 本地開發測試用，Zeabur 會使用 Gunicorn 啟動
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
