import requests
import re
import os
import time
from bs4 import BeautifulSoup
from pathlib import Path
from utils import *

def get_cid(bvid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Cookie": MY_COOKIE
    }
    url = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}"
    response = requests.get(url, headers=headers)
    print(f"response status code: {response.status_code}")
    print(f"response content: {response.text[:200]}")
    try:
        data = response.json()
        if data["code"] == 0:
            return data["data"][0]["cid"]
        else:
            print(f"API error: {data['message']}")
            return None
    except requests.exceptions.JSONDecodeError:
        print("invalid JSON format")
        return None

def get_danmaku(cid):
    """
    get danmaku data based on cid
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Cookie": "buvid3=94F4CE13-30F1-42FC-2AB5-D7DD3B44D83323162infoc; b_nut=1717896923; _uuid=D28894D8-AAE6-59F3-859F-610DCDC952F9323251infoc; enable_web_push=DISABLE; buvid4=AA06F2DC-B0C7-B8E9-0586-CB3BFD342D9324242-024060901-sihQ5DQWPT8v0HKARBd0mg%3D%3D; DedeUserID=35233437; DedeUserID__ckMd5=b47233f1e3129f48; header_theme_version=CLOSE; rpdid=|(k|RllmkRmk0J'u~u~)mYml~; buvid_fp_plain=undefined; LIVE_BUVID=AUTO5517278895494483; is-2022-channel=1; CURRENT_QUALITY=116; PVID=2; enable_feed_channel=DISABLE; fingerprint=dd1d5f4e3e91ce99dab07ea9fe9e02f7; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg2ODgzMjIsImlhdCI6MTczODQyOTA2MiwicGx0IjotMX0.iRixb5dcFPevbmTmJVPJvbfNwU47xfp79kdsmZPIMeA; bili_ticket_expires=1738688262; home_feed_column=5; browser_resolution=1528-738; buvid_fp=dd1d5f4e3e91ce99dab07ea9fe9e02f7; SESSDATA=45d5ac72%2C1754098600%2C72414%2A21CjDgdOLZYxRyTlml0jbWJ1dkRkD3jd589nBdo2zMhMb3r553Do9yqnV5i_9dkdD8HrISVmp1NnVjR0JMZk5NdUFfamVGUV9Za2JUbU1WTlhzT1RMQ3pfbHI0MzBSMzJWN0dGYzdXSndmc3ktOE9ZWXlubmpYUmJWVF8wbnB1OXZ6aFF5b3JJMmR3IIEC; bili_jct=f976850fea3cd703e5426e19a4bd95e3; b_lsid=104FC257C_194CCA17D4E; bsource=search_google; sid=6j4ekz80; bp_t_offset_35233437=1029769338938195968; CURRENT_FNVAL=2000"
    }
    url = f"https://comment.bilibili.com/{cid}.xml"
    
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8" 
    
    soup = BeautifulSoup(response.text, "lxml-xml")
    danmaku_list = soup.find_all("d")
    
    pattern = re.compile(r'\["[^"]+","[^"]+","[^"]+","[^"]+","([^"]+)",[^\]]+\]')

    danmaku_contents = []
    for danmaku in danmaku_list:
        text = danmaku.text
        match = pattern.search(text)
        if match:
            danmaku_contents.append(match.group(1))
        else:
            danmaku_contents.append(danmaku.text)
    
    return danmaku_contents

def save_to_file(danmaku_list, cid, output_dir="output"):
    """
    save files in the output folder
    """
    current_dir = Path(__file__).parent
    output_dir = current_dir.parent / "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f"{cid}.txt"
    file_path = output_dir / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        for danmaku in danmaku_list:
            f.write(danmaku + "\n")
    print(f"Danmaku saved at: {file_path}")

def read_bvid_from_file():
    """
    Read bvid.txt from the input folder
    """
    current_dir = Path(__file__).parent
    input_dir = current_dir.parent / "input"
    file_path = input_dir / "bvid.txt"
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        bvid_list = [line.strip() for line in f if line.strip()]
        return bvid_list

def get_existing_cids():
    """
    Check and skip cids for videos that have already been converted
    """
    current_dir = Path(__file__).parent
    output_dir = current_dir.parent / "output"
    existing_cids = set()
    for filename in os.listdir(output_dir):
        if filename.endswith(".txt"):
            cid = filename[:-4] 
            existing_cids.add(cid)
    return existing_cids

def get_video_title(bvid):
    """
    Get video title
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Cookie": MY_COOKIE
    }

    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 0:
            return data["data"]["title"]
        else:
            raise ValueError(f"API error: {data['message']}")
    else:
        raise ValueError(f"Request failure, status code: {response.status_code}")

def get_video_category(bvid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Cookie": MY_COOKIE
    }
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    response = requests.get(api_url,headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0: 
            video_info = data['data']
            partition = video_info['tname']
            return partition
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    existing_cids = get_existing_cids()
    print(existing_cids)

    bvid_list = read_bvid_from_file()
    if bvid_list:
        for bvid in bvid_list:
            print(f"currently on bvid: {bvid}")
            cid = get_cid(bvid)
            if cid:
                if str(cid) in existing_cids:
                    print(f"cid {cid} is existent, skip the video")
                    continue 

                print(f"cid: {cid}")
                danmaku_data = get_danmaku(cid)
                save_to_file(danmaku_data, cid)
                print(f"EXtracted {len(danmaku_data)} bullet comments，saved at output/{cid}.txt")
            else:
                print(f"cannot get cid, please check if bvid: {bvid} is correct, or there's a failure in Internet connection")
            
            print("3 seconds before extracting from the next video ...")
            time.sleep(3) 
    else:
        print("Cannot read bvid, please check if bvid.txt is in the input folder")
