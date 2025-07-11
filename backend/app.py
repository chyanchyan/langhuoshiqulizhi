from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime as dt
import os
from werkzeug.utils import secure_filename
from services.crud import get_player_cumsum_scores
from services.db_manager import DbManager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# CORS配置
cors_origins = os.getenv('CORS_ORIGINS', '*')
if cors_origins == '*':
    CORS(app)
else:
    CORS(app, origins=cors_origins.split(','))

# 应用配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

# 数据库连接池配置
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
    'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
    'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
    'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
}

# 文件上传配置
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_sys():
    try:
        db_manager = DbManager(app)

        # 检查mysql服务是否启动，如果未启动，则启动
        print("🔍 检查MySQL服务状态...")
        if not db_manager.check_and_start_mysql():
            print("❌ MySQL服务启动失败，请检查MySQL是否已安装并配置正确")
            print("💡 提示：")
            print("   1. 确保MySQL已正确安装")
            print("   2. 检查环境变量中的数据库配置")
            print("   3. 确保数据库用户有足够权限")
            return False
        
        print("✅ MySQL服务运行正常")
        
        return True
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        return False

@app.route('/')
def home():
    """首页路由"""
    return jsonify({
        'message': 'langhuo 后端服务',
        'status': 'success',
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'development')
    })

@app.route('/api/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'flask-backend',
        'timestamp': dt.now().isoformat(),
        'environment': os.getenv('FLASK_ENV', 'development')
    })

@app.route('/api/enterAuth')
def enter_auth():
    token = request.args.get('password')
    admin_password = os.getenv('ADMIN_PASSWORD', '34jinbulai')
    
    if token == admin_password:
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
    print("🚀 启动系统初始化...")
    if not init_sys():
        print("❌ 系统初始化失败，程序退出")
        exit(1)
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 启动服务器: http://{host}:{port}")
    print(f"🔧 调试模式: {debug}")
    print(f"环境: {os.getenv('FLASK_ENV', 'development')}")
    
    app.run(host=host, port=port, debug=debug) 