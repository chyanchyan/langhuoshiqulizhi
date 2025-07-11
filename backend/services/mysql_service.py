import subprocess
import time
import platform
import os
import logging
from typing import Optional, Tuple

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MySQLServiceManager:
    """MySQL服务管理器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == 'windows'
        self.is_linux = self.system == 'linux'
        self.is_macos = self.system == 'darwin'
    
    def check_mysql_service(self) -> bool:
        """检查MySQL服务是否正在运行"""
        try:
            if self.is_windows:
                return self._check_mysql_windows()
            elif self.is_linux:
                return self._check_mysql_linux()
            elif self.is_macos:
                return self._check_mysql_macos()
            else:
                logger.warning(f"不支持的操作系统: {self.system}")
                return False
        except Exception as e:
            logger.error(f"检查MySQL服务时出错: {e}")
            return False
    
    def start_mysql_service(self) -> Tuple[bool, str]:
        """启动MySQL服务"""
        try:
            if self.is_windows:
                return self._start_mysql_windows()
            elif self.is_linux:
                return self._start_mysql_linux()
            elif self.is_macos:
                return self._start_mysql_macos()
            else:
                return False, f"不支持的操作系统: {self.system}"
        except Exception as e:
            logger.error(f"启动MySQL服务时出错: {e}")
            return False, str(e)
    
    def stop_mysql_service(self) -> Tuple[bool, str]:
        """停止MySQL服务"""
        try:
            if self.is_windows:
                return self._stop_mysql_windows()
            elif self.is_linux:
                return self._stop_mysql_linux()
            elif self.is_macos:
                return self._stop_mysql_macos()
            else:
                return False, f"不支持的操作系统: {self.system}"
        except Exception as e:
            logger.error(f"停止MySQL服务时出错: {e}")
            return False, str(e)
    
    def restart_mysql_service(self) -> Tuple[bool, str]:
        """重启MySQL服务"""
        try:
            # 先停止服务
            stop_success, stop_msg = self.stop_mysql_service()
            if not stop_success:
                logger.warning(f"停止MySQL服务失败: {stop_msg}")
            
            # 等待一段时间
            time.sleep(2)
            
            # 再启动服务
            start_success, start_msg = self.start_mysql_service()
            if not start_success:
                return False, f"重启失败: {start_msg}"
            
            return True, "MySQL服务重启成功"
        except Exception as e:
            logger.error(f"重启MySQL服务时出错: {e}")
            return False, str(e)
    
    def _check_mysql_windows(self) -> bool:
        """Windows系统检查MySQL服务"""
        try:
            # 使用sc命令检查服务状态
            result = subprocess.run(
                ['sc', 'query', 'MySQL80'],  # MySQL8.0默认服务名
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return 'RUNNING' in result.stdout
            else:
                # 尝试其他可能的服务名
                service_names = ['MySQL', 'mysql', 'MYSQL80', 'MYSQL57', 'MYSQL56']
                for service_name in service_names:
                    result = subprocess.run(
                        ['sc', 'query', service_name],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0 and 'RUNNING' in result.stdout:
                        return True
                
                return False
        except subprocess.TimeoutExpired:
            logger.error("检查MySQL服务超时")
            return False
        except Exception as e:
            logger.error(f"Windows检查MySQL服务出错: {e}")
            return False
    
    def _check_mysql_linux(self) -> bool:
        """Linux系统检查MySQL服务"""
        try:
            # 尝试使用systemctl
            result = subprocess.run(
                ['systemctl', 'is-active', 'mysql'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout.strip() == 'active'
            
            # 尝试其他可能的服务名
            service_names = ['mysqld', 'mariadb', 'mysql-server']
            for service_name in service_names:
                result = subprocess.run(
                    ['systemctl', 'is-active', service_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip() == 'active':
                    return True
            
            # 尝试使用service命令
            result = subprocess.run(
                ['service', 'mysql', 'status'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logger.error("检查MySQL服务超时")
            return False
        except Exception as e:
            logger.error(f"Linux检查MySQL服务出错: {e}")
            return False
    
    def _check_mysql_macos(self) -> bool:
        """macOS系统检查MySQL服务"""
        try:
            # 尝试使用brew services
            result = subprocess.run(
                ['brew', 'services', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return 'mysql' in result.stdout and 'started' in result.stdout
            
            # 尝试使用launchctl
            result = subprocess.run(
                ['launchctl', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return 'mysql' in result.stdout or 'com.mysql' in result.stdout
            
            return False
        except subprocess.TimeoutExpired:
            logger.error("检查MySQL服务超时")
            return False
        except Exception as e:
            logger.error(f"macOS检查MySQL服务出错: {e}")
            return False
    
    def _start_mysql_windows(self) -> Tuple[bool, str]:
        """Windows系统启动MySQL服务"""
        try:
            # 尝试启动MySQL80服务
            result = subprocess.run(
                ['net', 'start', 'MySQL80'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务启动成功"
            
            # 尝试其他可能的服务名
            service_names = ['MySQL', 'mysql', 'MYSQL80', 'MYSQL57', 'MYSQL56']
            for service_name in service_names:
                result = subprocess.run(
                    ['net', 'start', service_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return True, f"MySQL服务({service_name})启动成功"
            
            return False, "无法启动MySQL服务，请检查服务是否已安装"
        except subprocess.TimeoutExpired:
            return False, "启动MySQL服务超时"
        except Exception as e:
            return False, f"启动MySQL服务出错: {e}"
    
    def _start_mysql_linux(self) -> Tuple[bool, str]:
        """Linux系统启动MySQL服务"""
        try:
            # 尝试使用systemctl启动
            result = subprocess.run(
                ['sudo', 'systemctl', 'start', 'mysql'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务启动成功"
            
            # 尝试其他可能的服务名
            service_names = ['mysqld', 'mariadb', 'mysql-server']
            for service_name in service_names:
                result = subprocess.run(
                    ['sudo', 'systemctl', 'start', service_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return True, f"MySQL服务({service_name})启动成功"
            
            # 尝试使用service命令
            result = subprocess.run(
                ['sudo', 'service', 'mysql', 'start'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务启动成功"
            
            return False, "无法启动MySQL服务，请检查服务是否已安装"
        except subprocess.TimeoutExpired:
            return False, "启动MySQL服务超时"
        except Exception as e:
            return False, f"启动MySQL服务出错: {e}"
    
    def _start_mysql_macos(self) -> Tuple[bool, str]:
        """macOS系统启动MySQL服务"""
        try:
            # 尝试使用brew services启动
            result = subprocess.run(
                ['brew', 'services', 'start', 'mysql'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务启动成功"
            
            # 尝试使用launchctl启动
            result = subprocess.run(
                ['sudo', 'launchctl', 'load', '-w', '/Library/LaunchDaemons/com.mysql.mysql.plist'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务启动成功"
            
            return False, "无法启动MySQL服务，请检查服务是否已安装"
        except subprocess.TimeoutExpired:
            return False, "启动MySQL服务超时"
        except Exception as e:
            return False, f"启动MySQL服务出错: {e}"
    
    def _stop_mysql_windows(self) -> Tuple[bool, str]:
        """Windows系统停止MySQL服务"""
        try:
            result = subprocess.run(
                ['net', 'stop', 'MySQL80'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务停止成功"
            
            # 尝试其他可能的服务名
            service_names = ['MySQL', 'mysql', 'MYSQL80', 'MYSQL57', 'MYSQL56']
            for service_name in service_names:
                result = subprocess.run(
                    ['net', 'stop', service_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return True, f"MySQL服务({service_name})停止成功"
            
            return False, "无法停止MySQL服务"
        except subprocess.TimeoutExpired:
            return False, "停止MySQL服务超时"
        except Exception as e:
            return False, f"停止MySQL服务出错: {e}"
    
    def _stop_mysql_linux(self) -> Tuple[bool, str]:
        """Linux系统停止MySQL服务"""
        try:
            result = subprocess.run(
                ['sudo', 'systemctl', 'stop', 'mysql'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务停止成功"
            
            # 尝试其他可能的服务名
            service_names = ['mysqld', 'mariadb', 'mysql-server']
            for service_name in service_names:
                result = subprocess.run(
                    ['sudo', 'systemctl', 'stop', service_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return True, f"MySQL服务({service_name})停止成功"
            
            return False, "无法停止MySQL服务"
        except subprocess.TimeoutExpired:
            return False, "停止MySQL服务超时"
        except Exception as e:
            return False, f"停止MySQL服务出错: {e}"
    
    def _stop_mysql_macos(self) -> Tuple[bool, str]:
        """macOS系统停止MySQL服务"""
        try:
            result = subprocess.run(
                ['brew', 'services', 'stop', 'mysql'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "MySQL服务停止成功"
            
            return False, "无法停止MySQL服务"
        except subprocess.TimeoutExpired:
            return False, "停止MySQL服务超时"
        except Exception as e:
            return False, f"停止MySQL服务出错: {e}"
    
    def wait_for_mysql_ready(self, timeout: int = 60) -> bool:
        """等待MySQL服务就绪"""
        logger.info("等待MySQL服务就绪...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.check_mysql_service():
                logger.info("MySQL服务已就绪")
                return True
            time.sleep(2)
        
        logger.error(f"等待MySQL服务就绪超时({timeout}秒)")
        return False 