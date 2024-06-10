import numpy as np
import cv2
from sklearn.model_selection import train_test_split
import os

# Khai báo 2 list X và y
X = []
Y = []

# Lặp qua các folder trong thư mục data
data_folder = "data"

for folder in os.listdir(data_folder):
    # Lặp các file trong thư mục con
    curr_path = os.path.join(data_folder, folder)
    for file in os.listdir(curr_path):
        curr_file = os.path.join(curr_path, file)
        
        image = cv2.imread(curr_file)
        X.append(image)
        Y.append(folder)
        
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print(f"Số lượng ảnh trong tập train: {len(X_train)}")
print(f"Số lượng ảnh trong tập test: {len(X_test)}")