import cv2 
import time
import numpy as np
from io import BytesIO

def match(background_bytef, icons_order):

	image_bytes = BytesIO(background_bytef)

	byte_image = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
	image = cv2.imdecode(byte_image, cv2.IMREAD_COLOR)

	coords = []
	trail_x = []
	trail_y = []

	for icon in icons_order:
		template = cv2.imread("src/{}.png".format(icon))

		result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

		template_height, template_width, _ = template.shape

		top_left = max_loc
		bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

		center_x = (top_left[0] + bottom_right[0]) // 2
		center_y = (top_left[1] + bottom_right[1]) // 2

		coords.append({"x":center_x, "y":center_y})
		timestamp = int(time.time() * 1000)
		trail_x.append({"timestamp":timestamp,"coord":center_x})
		trail_y.append({"timestamp":timestamp,"coord":center_y})

	timestamp = int(time.time() * 1000) + 15
	trail_x.append({"timestamp":timestamp,"coord":163})
	trail_y.append({"timestamp":timestamp,"coord":298})

	return coords, trail_x, trail_y
