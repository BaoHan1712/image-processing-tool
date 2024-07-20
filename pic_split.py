import os
import cv2
import numpy as np

#old folder
DATA_DIR = 'data_test'

# new folder
DATA2_DIR = 'data2'

if not os.path.exists(DATA2_DIR):
    os.makedirs(DATA2_DIR)

for img_path in os.listdir(DATA_DIR):
    
    img_full_path = os.path.join(DATA_DIR, img_path)

    img_save_path = os.path.join(DATA2_DIR, img_path)

    img = cv2.imread(img_full_path)
    img = cv2.resize(img, (1280,720))
    
    hsv =  cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([42, 55, 46])
    upper_green = np.array([75, 245, 245])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    hsv[:, :, 1] = cv2.add(hsv[:, :, 1], mask // 5)
    # hsv[:, :, 2] = cv2.add(hsv[:, :, 2], mask // 5)

    enhanced_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # save new picture in new folder 
    cv2.imwrite(img_save_path, enhanced_image)
    
    print(f"Đã lưu {img_save_path}")
