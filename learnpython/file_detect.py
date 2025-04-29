import os


def count_files_by_extension(folder_path):
    file_count = {}
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 {folder_path} 不存在。")
        return file_count

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension:
                if extension in file_count:
                    file_count[extension] += 1
                else:
                    file_count[extension] = 1
    return file_count


if __name__ == "__main__":
    folder_path = '/Users/suyuxuan/Documents'  # 可修改为你要遍历的文件夹路径
    result = count_files_by_extension(folder_path)
    for ext, count in result.items():
        print(f"后缀为 {ext} 的文件数量：{count}")
    