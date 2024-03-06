import os


def count_files_in_subfolders(folder_path):
    # Kiểm tra xem đường dẫn tới thư mục có tồn tại không
    if not os.path.exists(folder_path):
        print(f"Thư mục '{folder_path}' không tồn tại.")
        return

    # Dùng os.walk để duyệt qua tất cả các thư mục và tập tin trong thư mục cha
    for root, dirs, files in os.walk(folder_path):
        # In ra số lượng tập tin cho mỗi thư mục con
        if len(files) > 0:
            print(
                f"Thư mục '{os.path.relpath(root, folder_path)}' có {len(files)} tập tin.")


# Thay đổi đường dẫn folder_path thành đường dẫn thư mục chứa subfolder và tập tin của bạn
folder_path = "clean"
count_files_in_subfolders(folder_path)
