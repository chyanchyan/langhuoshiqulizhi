import json
import pytesseract
from PIL import Image
import cv2
import numpy as np


default_anchor = (132, 502)
default_relative_boxes = {
    'game_name': (135, 250, 580, 40),
    'chip_level': (90, 360, 210, 30),
    'game_hands_count': (340, 360, 180, 30),
    'creator_player_name': (530, 360, 220, 30),
    'start_time': (300, 425, 135, 26),
    'end_time': (453, 425, 120, 26)
}
default_record_list_params = {
    'record_list_anchor': (150, 925),
    'record_row_height': 75,
    'player_name_width': 250,
    'hands_width': 100,
    'buy_in_width': 125,
    'score_width': 150,
}

def pic_to_json(pic_path):

    image = Image.open(pic_path)
    image_array = np.array(image)
    anchor_loc = get_anchor_loc(image_array)
    relative_boxes, record_list_params = get_relative_boxes(anchor_loc)
    
    game_name = crop_and_ocr(image, relative_boxes['game_name'])
    chip_level = crop_and_ocr(image, relative_boxes['chip_level'])
    game_hands_count = crop_and_ocr(image, relative_boxes['game_hands_count'])
    creator_player_name = crop_and_ocr(image, relative_boxes['creator_player_name'])
    start_time = crop_and_ocr(image, relative_boxes['start_time'])
    end_time = crop_and_ocr(image, relative_boxes['end_time'])

    rx, ry = record_list_params['record_list_anchor']
    rh = record_list_params['record_row_height']
    nw = record_list_params['player_name_width']
    hw = record_list_params['hands_width']
    biw = record_list_params['buy_in_width']
    sw = record_list_params['score_width']

    record_list = []
    while ry < image.height:
        player_name = crop_and_ocr(image, (rx, ry, nw, rh))
        hands = crop_and_ocr(image, (rx+nw, ry, hw, rh))
        buy_in = crop_and_ocr(image, (rx+nw+hw, ry, biw, rh))
        score = crop_and_ocr(image, (rx+nw+hw+biw, ry, sw, rh))
        record_list.append({
            'player_name': player_name,
            'hands_count': hands,
            'buy_in_count': buy_in,
            'score': score
        })
        ry += rh

    return {
        'game_name': game_name,
        'chip_level': chip_level,
        'game_hands_count': game_hands_count,
        'creator_player_name': creator_player_name,
        'start_time': start_time,
        'end_time': end_time,
        'record_list': record_list
    }

def get_anchor_loc(image):
    # 在image中寻找anchor_img的坐标，并返回坐标
    anchor_pic_path = r'anchor_img.jpg'
    anchor_img = Image.open(anchor_pic_path)
    anchor_img_array = np.array(anchor_img)
    result = cv2.matchTemplate(image, anchor_img_array, cv2.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc


def get_relative_boxes(anchor_loc):
    dx, dy = anchor_loc[0] - default_anchor[0], anchor_loc[1] - default_anchor[1]
    for key, value in default_relative_boxes.items():
        x0, y0, w, h = value
        default_relative_boxes[key] = (x0+dx, y0+dy, w, h)

    for key, value in default_record_list_params.items():
        if key == 'record_list_anchor':
            x0, y0 = value
            default_record_list_params[key] = (x0+dx, y0+dy)
        
    return default_relative_boxes, default_record_list_params


def crop_and_ocr(image, box):
    region = image.crop((box[0], box[1], box[0]+box[2], box[1]+box[3]))
    text = pytesseract.image_to_string(region, lang='chi_sim+eng').strip()
    return text


def show_relative_boxes(image_array, relative_boxes):
    for key, value in relative_boxes.items():
        x0, y0, w, h = value
        cv2.rectangle(image_array, (x0, y0), (x0+w, y0+h), (0, 0, 255), 2)
    cv2.imshow('relative_boxes', image_array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def t_show_relative_boxes():
    pic_path = r'mock_record_pic.jpg'
    image = Image.open(pic_path)
    image_array = np.array(image)
    anchor_loc = get_anchor_loc(image_array)
    relative_boxes, record_list_params = get_relative_boxes(anchor_loc)
    show_relative_boxes(image_array, relative_boxes)

def main():
    pic_path = r'../uploads/20250711024727.jpg'
    res = pic_to_json(pic_path)

    res = json.dumps(res, indent=4)
    print(res)

if __name__ == "__main__":
    main() 