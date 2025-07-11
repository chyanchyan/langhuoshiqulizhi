import React, { useState, useEffect, useRef } from "react";

import * as echarts from "echarts";
import ReactECharts from "echarts-for-react";

interface Record {
  player_name: string;
  hands: number;
  buyin: number;
  profit: number;
}

interface Data {
  title: string;
  creator: string;
  start_time: string;
  end_time: string;
  boss: string;
  mvp: string;
  model_worker: string;
  records: Record[];
}

export function AccProfitChart() {
  const chartRef = useRef<HTMLDivElement>(null);
  const mockData: Data[] = require("../mockdata.json");
  const [data, setData] = useState<Data[]>(mockData);
  const [chart, setChart] = useState<echarts.ECharts | null>(null);
  const minTickInterval = 15;

  // 获取所有玩家名称
  const allPlayers = Array.from(
    new Set(
      data.flatMap((item) => 
        item.records
          .filter((record) => record && record.player_name) // 过滤掉空记录和没有player_name的记录
          .map((record) => record.player_name)
      )
    )
  );

  // 为每个玩家创建数据系列
  const series = allPlayers.map((playerName) => {
    let acc = 0

    const playerData = data.map((item) => {
      
      const record = item.records.find((r) => r && r.player_name && r.player_name === playerName);
      if (record) {
        acc += record.profit;
        return acc
      }
      return acc
    });
    let paddedPlayerData = [0, ...playerData];
    if (paddedPlayerData.length < minTickInterval) {
      paddedPlayerData = [
        ...paddedPlayerData,
        ...Array(minTickInterval - paddedPlayerData.length).fill(null),
      ];
    }

    return {
      name: playerName,
      type: "line",
      data: paddedPlayerData,
      smooth: false,
      showSymbol: true,
      symbolSize: 8,
      lineStyle: {
        width: 3,
      },
      emphasis: {
        focus: "series",
      },
    };
  });
  let paddedEndTime = ["", ...data.map((item) => item.end_time)];
  if (paddedEndTime.length < minTickInterval) {
    paddedEndTime = [
      ...paddedEndTime,
      ...Array(minTickInterval - paddedEndTime.length).fill(""),
    ];
  }
  const option = {
    title: {
      text: "淳朴的记录",
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
    },
    legend: {
      data: allPlayers,
      top: 30,
      left: "center",
      itemWidth: 25,
      itemHeight: 14,
      itemGap: 10,
      textStyle: {
        fontSize: 12,
      },
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      top: "20%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: paddedEndTime,
      axisLabel: {
        rotate: 45,
      },
      boundaryGap: false,
      axisTick: {
        alignWithLabel: true,
        align: "right",
      },
      axisPointer: {
        value: 0,
      },
      minInterval: 15,
      maxInterval: Math.max(1, Math.floor(data.length / 15)),
    },
    yAxis: {
      type: "value",
      scale: true,
    },
    series: series,
  };

  useEffect(() => {
    if (chartRef.current) {
      const chart = echarts.init(chartRef.current);
      setChart(chart);
      chart.setOption(option);
      return () => {
        chart.dispose();
      };
    }
  }, [option]);

  useEffect(() => {
    function resizeChart() {
      if (chart) {
        chart.resize();
      }
    }
    window.addEventListener("resize", resizeChart);
    return () => {
      window.removeEventListener("resize", resizeChart);
    };
  }, [chart]);

  return (
    <div>
      <ReactECharts
        option={option}
        style={{ width: "100vw", height: "80vh" }}
      />
    </div>
  );
}
