import os
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description='工作目录中的文件后缀名修改')
    parser.add_argument('work_dir', metavar='WORK_DIR', type=str, nargs=1, help='修改文件名的后缀目录')
    parser.add_argument('old_ext', metavar='OLD_EXT', type=str, nargs=1, help='原来的后缀')
    parser.add_argument('new_ext', metavar='NEW_EXT', type=str, nargs=1, help='新的后缀')
    return parser
    

# 后缀批量重命名
def batch_rename(work_dir, old_ext, new_ext):
    """
    传递当前目录，原来后缀名，新的后缀名后，批量重命名后缀
    """
    for filename in os.listdir(work_dir):
        # 获取得到文件后缀
        split_file = os.path.splitext(filename)
        file_ext = split_file[1]
        # 定位后缀名为old_ext 的文件
        if old_ext == file_ext:
            # 修改后文件的完整名称
            newfile = split_file[0] + new_ext
            # 实现重命名操作
            os.rename(
                os.path.join(work_dir, filename),
                os.path.join(work_dir, newfile)
            )
    print("完成重命名")
    print(os.listdir(work_dir))

batch_rename('/Users/suyuxuan/Downloads/rename', '.ts', '.mp4')
