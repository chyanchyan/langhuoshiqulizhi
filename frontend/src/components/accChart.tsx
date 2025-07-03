import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Box, Typography, Paper, CircularProgress, Alert } from '@mui/material';
import axios from 'axios';
import API_CONFIG, { getApiUrl } from '../config/api';

interface PlayerRecord {
  player_id: string;
  game_id: string;
  start_time: string;
  score: number;
}

interface ChartData {
  timestamp: string;
  [key: string]: string | number;
}

const AccChart: React.FC = () => {
  const [data, setData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [players, setPlayers] = useState<string[]>([]);

  // 生成随机颜色
  const generateColors = (count: number) => {
    const colors = [
      '#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#ff0000',
      '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'
    ];
    return colors.slice(0, count);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const apiUrl = getApiUrl(API_CONFIG.ENDPOINTS.PLAYER_RECORD);
        const response = await axios.get(apiUrl);
        
        if (response.data.data && response.data.data.length > 0) {
          const playerRecords: PlayerRecord[] = response.data.data;
          
          // 提取所有时间戳并去重
          const allTimestamps = new Set<string>();
          playerRecords.forEach(record => {
            allTimestamps.add(record.start_time);
          });
          
          // 按时间戳排序
          const sortedTimestamps = Array.from(allTimestamps).sort();
          
          // 构建图表数据
          const chartData: ChartData[] = sortedTimestamps.map(timestamp => {
            const record = playerRecords.find(r => r.start_time === timestamp);
            return {
              timestamp,
              [record?.player_id || '']: record?.score || 0
            };
          });
          
          setData(chartData);
          
          // 设置玩家列表
          const playerNames = playerRecords.map(p => p.player_id);
          setPlayers(playerNames);
        } else {
          setError('暂无数据');
        }
      } catch (err) {
        console.error('获取数据失败:', err);
        setError('获取数据失败，请检查网络连接');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  const colors = generateColors(players.length);

  return (
    <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
      <Typography variant="h6" component="h2" sx={{ mb: 3, textAlign: 'center' }}>
        多玩家准确率趋势图
      </Typography>
      
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="start_time" />
          <YAxis />
          <Tooltip />
          <Legend />
          {players.map((player, index) => (
            <Line key={player} dataKey={player} stroke={colors[index]} />
          ))}
        </LineChart>
      </ResponsiveContainer>
      
      <Typography variant="body2" color="text.secondary" sx={{ mt: 2, textAlign: 'center' }}>
        显示所有玩家的准确率变化趋势
      </Typography>
    </Paper>
  );
};

export default AccChart;
