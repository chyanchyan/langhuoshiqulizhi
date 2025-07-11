# 数据库连接问题修复说明

## 问题描述
错误信息：`Not an executable object: 'SELECT 1'`

这个错误是由于 SQLAlchemy 版本更新导致的。在较新版本的 SQLAlchemy 中，`execute()` 方法返回的是一个 `Result` 对象，需要调用 `.fetchone()` 或其他方法来获取结果。

## 修复内容

### 1. 修复 `db_manager.py` 中的 `test_connection` 方法

**修复前：**
```python
def test_connection(self):
    """测试数据库连接"""
    with self.engine.connect() as conn:
        result = conn.execute("SELECT 1")
```

**修复后：**
```python
def test_connection(self):
    """测试数据库连接"""
    try:
        with self.engine.connect() as conn:
            result = conn.execute("SELECT 1")
            result.fetchone()  # 获取结果
            return True
    except Exception as e:
        logger.error(f"数据库连接测试失败: {e}")
        return False
```

### 2. 修复 `init_db` 方法

**修复前：**
```python
def init_db(self):
    """初始化数据库表"""
    # 创建数据库
    with self.engine.connect() as conn:
        conn.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

    # 创建表
    Base.metadata.create_all(self.engine)
    print("数据库表初始化完成")
```

**修复后：**
```python
def init_db(self):
    """初始化数据库表"""
    try:
        # 获取数据库名称
        database = os.getenv('DB_SCHEMA', 'langhuo_db')
        
        # 创建数据库
        with self.engine.connect() as conn:
            conn.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            conn.commit()

        # 创建表
        Base.metadata.create_all(self.engine)
        print("数据库表初始化完成")
    except Exception as e:
        logger.error(f"初始化数据库失败: {e}")
        raise
```

### 3. 修复数据库 URL 构建

**修复前：**
```python
host = os.getenv('DATABASE_HOST', 'localhost')
port = os.getenv('DATABASE_PORT', '3306')
username = os.getenv('DATABASE_USER', 'root')
password = os.getenv('DATABASE_PASSWORD', '123456')
charset = os.getenv('DATABASE_CHARSET', 'utf8mb4')

return f"mysql+pymysql://{username}:{password}@{host}:{port}?charset={charset}"
```

**修复后：**
```python
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '3306')
username = os.getenv('DB_USERNAME', 'root')
password = os.getenv('DB_PASSWORD', '123456')
charset = os.getenv('DB_CHARSET', 'utf8mb4')
database = os.getenv('DB_SCHEMA', 'langhuo_db')

return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset={charset}"
```

### 4. 增强错误处理

在 `crud.py` 和 `app.py` 中添加了更好的错误处理机制，确保在数据库连接失败时不会导致程序崩溃。

## 环境配置

请确保创建 `.env` 文件并配置以下环境变量：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_SCHEMA=langhuo_db
DB_USERNAME=root
DB_PASSWORD=your-password-here
DB_CHARSET=utf8mb4

# 数据库连接池配置
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

## 测试

运行测试脚本来验证修复是否有效：

```bash
cd backend
python test_db.py
```

## 注意事项

1. 确保 MySQL 服务已安装并运行
2. 确保数据库用户有足够权限
3. 确保防火墙设置允许数据库连接
4. 如果使用 Docker，确保容器间网络配置正确

## 相关文件

- `backend/services/db_manager.py` - 数据库管理器
- `backend/services/crud.py` - 数据库操作
- `backend/app.py` - 主应用文件
- `backend/test_db.py` - 测试脚本
- `backend/.env.example` - 环境变量示例 