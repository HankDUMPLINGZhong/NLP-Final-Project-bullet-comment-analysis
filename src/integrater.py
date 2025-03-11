import os
import csv
from pathlib import Path

'''
Integrater:
merge bullet comments from all files into combined_danmaku.csv, to be used for both experiments
NOTICE - run this before running both experiments
'''

def read_danmaku_from_files():
    """
    read all bullet comment files from output folder
    """
    current_dir = Path(__file__).parent
    output_dir = current_dir.parent / "output"
    danmaku_set = set()
    for filename in os.listdir(output_dir):
        if filename.endswith(".txt"): 
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    danmaku_set.add(line.strip()) 
    return list(danmaku_set) 

def save_to_csv(danmaku_list, output_file="combined_danmaku.csv"):
    """
    save to csv file
    """
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["弹幕内容"])  # head for csv file
        for danmaku in danmaku_list:
            writer.writerow([danmaku])
    print(f"Unique danmaku saved at: {output_file}")

if __name__ == "__main__":
    danmaku_list = read_danmaku_from_files()
    print(f"Get {len(danmaku_list)} unique bullet comments")
    save_to_csv(danmaku_list)