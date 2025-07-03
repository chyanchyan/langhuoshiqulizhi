from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime as dt
import os
from werkzeug.utils import secure_filename
from services.curd import get_player_cumsum_scores
import configparser


app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = True

# 添加数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'mysql+pymysql://username:password@localhost/langhuo_db'
)

# 添加上传文件夹配置
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', './uploads')

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    """首页路由"""
    return jsonify({
        'message': 'langhuo 后端服务',
        'status': 'success',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'flask-backend',
        'timestamp': dt.now().isoformat()
    })


@app.route('/api/enterAuth')
def enter_auth():
    token = request.args.get('password')
    parser = configparser.ConfigParser()
    parser.read('admin.ini')
    compare = parser.get('password', 'password')
    if token == compare:
        return jsonify({
            'data': 0,
            'status': 'success',
            'message': 'password 验证成功'
        })
    else:
        return jsonify({
            'data': 1,
            'status': 'error',
            'message': 'password 验证失败'
        })

@app.route('/api/uploadRecordPic')
def upload_record_pic():
    """上传记录图片接口"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            'status': 'success',
            'message': '图片上传成功',
            'filename': filename
        })
    else:
        return jsonify({'error': 'Failed to upload file'}), 500


@app.route('/api/getPlayerRecord')
def get_player_record():
    """获取玩家记录接口"""
    data = get_player_cumsum_scores()
    return jsonify({
        'data': data,
        'status': 'success',
        'message': '获取玩家记录成功'
    })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 