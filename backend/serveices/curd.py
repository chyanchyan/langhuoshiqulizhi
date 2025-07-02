from PIL import Image
import pytesseract
import json
from serveices.db_manager import DbManager
import pandas as pd

def booking_record_pic(image_path):
    # 打开图片
    image_path = "/path/to/image.png"
    image = Image.open(image_path)

    # 设置语言
    tess_lang = "chi_sim+eng"


    mock = {
    "title": "浪",
    "time": "6-28 13:30 ~ 6-29 1:30",
    'creator': '看君醉',
    'total_hands': 1000,
    "players": [
        {"name": "看君醉", "hands": 311, "buyin": 3000, "profit": 33980},
    ]
    }


    # 手动标注的区域坐标（示例）——你需要把这些换成你的坐标
    title_box = (150, 120, 200, 160)
    time_box = (240, 250, 700, 290)

    # 玩家数据区域，每行一个字典（手动标注坐标）
    player_boxes = [
        {
            "name_box": (100, 560, 300, 590),
            "hands_box": (320, 560, 400, 590),
            "buyin_box": (420, 560, 500, 590),
            "profit_box": (520, 560, 700, 590)
        },
        {
            "name_box": (100, 630, 300, 660),
            "hands_box": (320, 630, 400, 660),
            "buyin_box": (420, 630, 500, 660),
            "profit_box": (520, 630, 700, 660)
        },
        # ... 继续添加更多玩家
    ]

    # 提取比赛名称与时间
    title = pytesseract.image_to_string(image.crop(title_box), lang=tess_lang).strip()
    time = pytesseract.image_to_string(image.crop(time_box), lang=tess_lang).strip()

    # 提取玩家信息
    players = []
    for box in player_boxes:
        name = pytesseract.image_to_string(image.crop(box["name_box"]), lang=tess_lang).strip()
        hands = pytesseract.image_to_string(image.crop(box["hands_box"]), lang=tess_lang).strip()
        buyin = pytesseract.image_to_string(image.crop(box["buyin_box"]), lang=tess_lang).strip()
        profit = pytesseract.image_to_string(image.crop(box["profit_box"]), lang=tess_lang).strip().replace(",", "")
        
        # 尝试将数字字段转为 int
        def to_int(s):
            try:
                return int(s.replace("+", "").replace("−", "-").replace("–", "-"))
            except:
                return s

        players.append({
            "name": name,
            "hands": to_int(hands),
            "buyin": to_int(buyin),
            "profit": to_int(profit)
        })

    # 最终 JSON 数据
    result = {
        "title": title,
        "time": time,
        "players": players
    }

    # 输出 JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))




def get_player_record_data():
    sql1 = 'select * from langhuo_db.game_records'
    sql2 = 'select * from langhuo_db.players'
    sql3 = 'select * from langhuo_db.games'
    conn = DbManager().get_conn()
    game_record_data = pd.read_sql(sql1, conn)
    players_data = pd.read_sql(sql2, conn)
    games_data = pd.read_sql(sql3, conn)
    data = pd.merge(
        game_record_data,
        players_data,
        left_on='player_id',
        right_on='id',
        how='left'
    )
    data = pd.merge(
        data,
        games_data,
        left_on='game_id',
        right_on='id',
        how='left'
    )
    return data


def get_player_cumsum_scores():
    data = get_player_record_data()
    
    # 获取所有玩家ID
    all_player_ids = data['player_id'].unique()
    
    # 获取所有游戏ID和对应的开始时间
    games_info = data[['game_id', 'start_time']].drop_duplicates()
    
    # 创建完整的数据框，包含所有玩家在所有游戏中的记录
    complete_data = []
    
    for _, game_row in games_info.iterrows():
        game_id = game_row['game_id']
        start_time = game_row['start_time']
        
        # 获取该局游戏的实际参与者
        game_participants = data[data['game_id'] == game_id]
        
        # 为每个玩家创建记录
        for player_id in all_player_ids:
            # 检查该玩家是否参与了这局游戏
            player_in_game = game_participants[game_participants['player_id'] == player_id]
            
            if len(player_in_game) > 0:
                # 玩家参与了游戏，使用原始数据
                complete_data.append(player_in_game.iloc[0].to_dict())
            else:
                # 玩家没有参与游戏，创建默认记录
                default_record = {
                    'game_id': game_id,
                    'player_id': player_id,
                    'start_time': start_time,
                    'score': 0,  # 没有参与，score设为0
                    # 其他字段设为空或默认值
                    'profit': 0,
                    'buyin': 0,
                    'hands': 0
                }
                complete_data.append(default_record)
    
    # 转换为DataFrame
    complete_df = pd.DataFrame(complete_data)
    
    # 按照player_id和start_time排序
    complete_df = complete_df.sort_values(['player_id', 'start_time'])
    
    # 计算每个玩家的累计score
    complete_df['cumulative_score'] = complete_df.groupby('player_id')['score'].cumsum()
    
    return complete_df.to_dict(orient='records')


