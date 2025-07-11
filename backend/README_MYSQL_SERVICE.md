# MySQL服务管理功能说明

## 概述

本系统集成了自动MySQL服务管理功能，可以在系统启动时自动检查并启动MySQL服务，确保数据库连接正常。

## 功能特性

- ✅ **自动检测MySQL服务状态**
- ✅ **自动启动MySQL服务**（如果未运行）
- ✅ **跨平台支持**（Windows、Linux、macOS）
- ✅ **服务就绪等待**
- ✅ **详细的日志记录**
- ✅ **错误处理和重试机制**

## 支持的操作系统

### Windows
- 使用 `sc query` 和 `net start/stop` 命令
- 支持的服务名：`MySQL80`、`MySQL`、`mysql`、`MYSQL80`、`MYSQL57`、`MYSQL56`

### Linux
- 使用 `systemctl` 和 `service` 命令
- 支持的服务名：`mysql`、`mysqld`、`mariadb`、`mysql-server`

### macOS
- 使用 `brew services` 和 `launchctl` 命令
- 支持Homebrew安装的MySQL

## 使用方法

### 1. 自动启动（推荐）

系统启动时会自动检查并启动MySQL服务：

```bash
cd backend
python app.py
```

### 2. 手动测试

运行测试脚本检查MySQL服务状态：

```bash
# 基本测试
python test_mysql_service.py

# 交互式测试
python test_mysql_service.py --interactive
```

### 3. 编程接口

```python
from services.mysql_service import MySQLServiceManager

# 创建服务管理器
mysql_manager = MySQLServiceManager()

# 检查服务状态
is_running = mysql_manager.check_mysql_service()

# 启动服务
success, message = mysql_manager.start_mysql_service()

# 停止服务
success, message = mysql_manager.stop_mysql_service()

# 重启服务
success, message = mysql_manager.restart_mysql_service()

# 等待服务就绪
is_ready = mysql_manager.wait_for_mysql_ready(timeout=60)
```

## 环境变量配置

确保在 `.env` 文件中配置正确的数据库连接信息：

```env
# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=langhuo_db
DATABASE_USER=root
DATABASE_PASSWORD=123456
DATABASE_CHARSET=utf8mb4

# 或者使用完整的DATABASE_URL
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/langhuo_db?charset=utf8mb4
```

## 故障排除

### 1. MySQL服务启动失败

**可能原因：**
- MySQL未安装
- 服务名不正确
- 权限不足
- 端口被占用

**解决方案：**
```bash
# Windows - 以管理员身份运行
net start MySQL80

# Linux - 使用sudo
sudo systemctl start mysql

# macOS - 使用brew
brew services start mysql
```

### 2. 数据库连接失败

**可能原因：**
- 数据库不存在
- 用户名或密码错误
- 数据库权限不足

**解决方案：**
```sql
-- 创建数据库
CREATE DATABASE langhuo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户并授权
CREATE USER 'langhuo_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON langhuo_db.* TO 'langhuo_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 权限问题

**Windows：**
- 以管理员身份运行命令提示符
- 确保用户有启动服务的权限

**Linux/macOS：**
- 使用 `sudo` 运行命令
- 确保用户有相应的系统权限

## 日志输出示例

```
🚀 启动系统初始化...
🔍 检查MySQL服务状态...
📋 操作系统: windows
🔍 检测到的系统类型:
   - Windows: True
   - Linux: False
   - macOS: False

1️⃣ 检查MySQL服务状态...
   服务状态: 🔴 未运行

2️⃣ 尝试启动MySQL服务...
   启动结果: ✅ 成功
   消息: MySQL服务(MySQL80)启动成功

3️⃣ 等待服务就绪...
   ✅ 服务已就绪

4️⃣ 再次检查服务状态...
   服务状态: 🟢 运行中

✅ MySQL服务运行正常
📦 初始化数据库表...
✅ 数据库初始化完成
🚀 启动服务器: http://0.0.0.0:5000
```

## 注意事项

1. **权限要求**：启动MySQL服务需要管理员/root权限
2. **服务名差异**：不同版本的MySQL可能有不同的服务名
3. **超时设置**：服务启动可能需要较长时间，默认超时为60秒
4. **错误处理**：系统会自动重试并记录详细的错误信息
5. **环境变量**：确保所有必要的环境变量都已正确配置

## 扩展功能

如需添加更多功能，可以：

1. 修改 `mysql_service.py` 添加新的服务管理方法
2. 在 `db_manager.py` 中集成更多数据库管理功能
3. 添加配置文件支持，允许自定义服务名和超时时间
4. 实现服务健康检查和自动恢复功能 