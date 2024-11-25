import os
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
from imagehash import average_hash

def get_image_hash(image_path):
    """Tính toán hash của ảnh sử dụng average hash"""
    try:
        return str(average_hash(Image.open(image_path)))
    except Exception as e:
        print(f"Lỗi khi xử lý ảnh {image_path}: {e}")
        return None

def find_duplicate_images(folder_path):
    """Tìm các ảnh giống nhau trong thư mục"""
    hash_dict = {}
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    print("Đang quét tất cả ảnh...")
    for img_path in Path(folder_path).glob('*'):
        if img_path.suffix.lower() in image_extensions:
            img_hash = get_image_hash(img_path)
            if img_hash:
                if img_hash in hash_dict:
                    hash_dict[img_hash].append(img_path)
                else:
                    hash_dict[img_hash] = [img_path]
    
    return {h: paths for h, paths in hash_dict.items() if len(paths) > 1}

def show_sample_duplicates(duplicates):
    """Hiển thị một cặp ảnh mẫu từ nhóm ảnh trùng lặp đầu tiên"""
    # Lấy nhóm ảnh đầu tiên
    first_group = next(iter(duplicates.values()))
    img_path1 = first_group[0]  # Ảnh gốc
    img_path2 = first_group[1]  # Ảnh trùng đầu tiên
    
    img1 = cv2.imread(str(img_path1))
    img2 = cv2.imread(str(img_path2))
    
    if img1 is None or img2 is None:
        return None
    
    # Đảm bảo ảnh có cùng kích thước để hiển thị
    height = 400
    width1 = int(img1.shape[1] * height / img1.shape[0])
    width2 = int(img2.shape[1] * height / img2.shape[0])
    
    img1 = cv2.resize(img1, (width1, height))
    img2 = cv2.resize(img2, (width2, height))
    
    # Hiển thị tên file trên ảnh
    cv2.putText(img1, img_path1.name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img2, img_path2.name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Ghép 2 ảnh ngang nhau
    combined = np.hstack((img1, img2))
    
    window_name = 'Ảnh mẫu - Nhấn c để xóa TẤT CẢ ảnh trùng lặp, phím khác để thoát'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, combined)
    return cv2.waitKey(0) & 0xFF

def delete_all_duplicates(duplicates):
    """Xóa tất cả ảnh trùng lặp từ mọi nhóm"""
    deleted_count = 0
    for hash_value, paths in duplicates.items():
        original = paths[0]  # Giữ lại ảnh đầu tiên
        duplicates_to_remove = paths[1:]  # Xóa các ảnh còn lại
        
        for img_path in duplicates_to_remove:
            try:
                os.remove(img_path)
                print(f"Đã xóa: {img_path.name}")
                deleted_count += 1
            except Exception as e:
                print(f"Lỗi khi xóa {img_path.name}: {e}")
    
    return deleted_count

def main():
    folder_path = Path("fire\den_train\images")
    
    if not folder_path.exists():
        print(f"Thư mục {folder_path} không tồn tại!")
        return
    
    print("Đang tìm ảnh giống nhau...")
    duplicates = find_duplicate_images(folder_path)
    
    if not duplicates:
        print("Không tìm thấy ảnh giống nhau!")
        return
    
    # Tính tổng số ảnh trùng lặp
    total_duplicates = sum(len(paths) - 1 for paths in duplicates.values())
    print(f"\nTìm thấy {total_duplicates} ảnh trùng lặp trong {len(duplicates)} nhóm")
    
    # Hiển thị một cặp ảnh mẫu và chờ xác nhận
    if show_sample_duplicates(duplicates) == ord('c'):
        print("\nĐang xóa tất cả ảnh trùng lặp...")
        deleted_count = delete_all_duplicates(duplicates)
        print(f"\nĐã xóa thành công {deleted_count} ảnh trùng lặp")
    else:
        print("\nĐã hủy thao tác xóa")
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()