import os

def delete_html_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
                except Exception as e:
                    print(f"删除失败: {file_path}，原因: {e}")

if __name__ == "__main__":
    delete_html_files("blogs")
