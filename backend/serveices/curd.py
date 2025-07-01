from PIL import Image
import pytesseract
import json
from serveices.db_manager import DbManager


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




def get_player_record_data(days=30):
    sql = 'select * from langhuo_db.game_records where created_at > %s'
    conn = DbManager().get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, (days,))
    data = cursor.fetchall()

    return data