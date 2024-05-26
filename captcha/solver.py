import cv2
import numpy as np

def _read_image(image_source):
    if isinstance(image_source, bytes):
        return cv2.imdecode(np.frombuffer(image_source, np.uint8), cv2.IMREAD_ANYCOLOR)
    elif hasattr(image_source, 'read'):
        return cv2.imdecode(np.frombuffer(image_source.read(), np.uint8), cv2.IMREAD_ANYCOLOR)
    else:
        raise TypeError("Invalid image source type. Must be bytes or a file-like object.")

def find_puzzle_piece_position(background, puzzle_piece):
    edge_puzzle_piece = cv2.Canny(puzzle_piece, 100, 200)
    edge_background = cv2.Canny(background, 100, 200)

    edge_puzzle_piece_rgb = cv2.cvtColor(edge_puzzle_piece, cv2.COLOR_GRAY2RGB)
    edge_background_rgb = cv2.cvtColor(edge_background, cv2.COLOR_GRAY2RGB)

    res = cv2.matchTemplate(edge_background_rgb, edge_puzzle_piece_rgb, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    h, w = edge_puzzle_piece.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    center_x = top_left[0] 
    center_y = top_left[1]
    position_from_left = center_x
    position_from_bottom = background.shape[0] - center_y

    return {
        "coordinates": [center_x, center_y]
    }


def find_position(background_bytef, puzzle_piece_bytef):
    _background = _read_image(background_bytef)
    _puzzle_piece = _read_image(puzzle_piece_bytef)
    return find_puzzle_piece_position(_background, _puzzle_piece)
