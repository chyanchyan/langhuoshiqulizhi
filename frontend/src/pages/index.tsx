import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Container,
  Paper,
  Alert,
  Fade,
  InputAdornment,
  IconButton
} from '@mui/material';
import { Visibility, VisibilityOff, Lock } from '@mui/icons-material';
import axios from 'axios';
import { AccProfitChart } from '../components/accProfitchart';
import API_CONFIG, { getApiUrl } from '../config/api';

export default function HomePage() {
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [networkStatus, setNetworkStatus] = useState('online');

  return <div><AccProfitChart /></div>
  // 定义一个异步函数auth，用于验证用户身份
  const auth = async () => {
    try {
      // 获取API地址
      const apiUrl = getApiUrl(API_CONFIG.ENDPOINTS.AUTH);
      console.log('发送验证请求到:', apiUrl);
      
      // 发送GET请求，获取响应
      const res = await axios.get(apiUrl, {
        params: { password },
        timeout: 10000 // 10秒超时
      });
      
      console.log('收到响应:', res.data);
      
      // 判断响应状态
      if (res.data.status === 'success') {
        // 验证成功，设置认证状态为true，并将认证状态存储到localStorage中
        setIsAuthenticated(true);
        localStorage.setItem('isAuthenticated', 'true');
        setError(''); // 清空错误信息
      } else {
        // 验证失败，设置认证状态为false，并设置错误信息
        setIsAuthenticated(false);
        setError('验证失败,请检查口令是否正确');
      }
    } catch (err: any) {
      console.error('验证请求失败:', err);
      // 判断错误类型，设置相应的错误信息
      if (err.code === 'ECONNABORTED') {
        setError('请求超时，请检查网络连接');
      } else if (err.response) {
        setError(`服务器错误: ${err.response.status}`);
      } else if (err.request) {
        setError('无法连接到服务器，请检查网络连接');
      } else {
        setError('验证失败,请检查口令是否正确');
      }
    }
  }

  // 检查网络状态
  useEffect(() => {
    const checkNetwork = () => {
      setNetworkStatus(navigator.onLine ? 'online' : 'offline');
    };
    
    window.addEventListener('online', checkNetwork);
    window.addEventListener('offline', checkNetwork);
    checkNetwork();
    
    return () => {
      window.removeEventListener('online', checkNetwork);
      window.removeEventListener('offline', checkNetwork);
    };
  }, []);

  // 检查是否已经通过验证（从 localStorage 读取）
  useEffect(() => {
    const authStatus = localStorage.getItem('isAuthenticated');
    if (authStatus === 'true') {
      setIsAuthenticated(true);
    }
  }, []);

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
    setError(''); // 清除错误信息
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    console.log('表单提交事件触发');
    setIsLoading(true);
    setError('');

    try {
      await auth();
    } catch (err) {
      console.error('验证过程出错:', err);
    }
    setIsLoading(false);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('isAuthenticated');
    setPassword('');
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  // 如果已认证，显示站点内容
  if (isAuthenticated) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            失去理智
          </Typography>
          <Button
            variant="outlined"
            color="secondary"
            onClick={handleLogout}
            sx={{ minWidth: 100 }}
          >
            退出登录
          </Button>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <AccProfitChart />
        </Box>
        
      </Container>
    );
  }

  // 登录界面
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        p: 2
      }}
    >
      <Container maxWidth="sm">
        <Fade in={true} timeout={1000}>
          <Paper
            elevation={8}
            sx={{
              p: 4,
              borderRadius: 3,
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)'
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Box sx={{ 
                display: 'inline-flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                width: 80,
                height: 80,
                borderRadius: '50%',
                bgcolor: 'primary.main',
                mb: 2
              }}>
                <Lock sx={{ fontSize: 40, color: 'white' }} />
              </Box>
              
              <Typography variant="h4" component="h1" sx={{ 
                fontWeight: 'bold', 
                mb: 1,
                background: 'linear-gradient(45deg, #667eea, #764ba2)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                淳朴的记录
              </Typography>
              
              <Typography variant="body1" color="text.secondary">
                请输入访问口令以继续
              </Typography>
            </Box>

            {/* 网络状态提示 */}
            {networkStatus === 'offline' && (
              <Alert severity="warning" sx={{ mb: 2 }}>
                网络连接已断开，请检查网络设置
              </Alert>
            )}

            {/* API地址显示（开发环境） */}
            {process.env.NODE_ENV === 'development' && (
              <Alert severity="info" sx={{ mb: 2 }}>
                后端地址: {API_CONFIG.BASE_URL}
              </Alert>
            )}

            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                type={showPassword ? 'text' : 'password'}
                label="访问口令"
                value={password}
                onChange={handlePasswordChange}
                variant="outlined"
                size="medium"
                sx={{ mb: 3 }}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={togglePasswordVisibility}
                        edge="end"
                        size="large"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                error={!!error}
                helperText={error}
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading || !password.trim() || networkStatus === 'offline'}
                onClick={handleSubmit}
                onTouchEnd={handleSubmit}
                sx={{
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  borderRadius: 2,
                  background: 'linear-gradient(45deg, #667eea, #764ba2)',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #5a6fd8, #6a4190)',
                  }
                }}
              >
                {isLoading ? '验证中...' : '失去理智'}
              </Button>
            </form>

            {error && (
              <Fade in={!!error}>
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              </Fade>
            )}
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
}
