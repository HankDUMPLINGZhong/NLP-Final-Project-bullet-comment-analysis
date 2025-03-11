from utils import *
import os
import pandas as pd
from pathlib import Path
import json

'''
Meme collector:
collect, merge, and clean language features of bullet comments
'''

def call_chat_completion(system_message: str, user_message: str, model = "gpt-4o-mini", temperature = 0.5) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

def analyze_language_feature():
    current_dir = Path(__file__).parent
    csv_path = current_dir.parent / "data" / "combined_danmaku.csv"
    with open(csv_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    print(len(file_content))
    file_content=file_content[:900000]
    for i in range(len(file_content)//10000):
        content = file_content[0+10000*i:10000+10000*i]
        system_message = "you are a linguist studying modern online Internet slang"
        user_message = f'''I am providing you with a file, which includes collections of danmaku from the platform Bilibili
                    Your task is to analyze the language features of the comments and capture memes that you have identified
                    Do not show the process of analysis.
                    Instead, just show the memes you have collected, together with: 
                    1. an example sentence where this meme is contained; 
                    2. meaning of the meme; 
                    3. possible source of the meme
                    Sometimes, the memes are not expressed semantically. 
                    They might be expressied via syntactic structure. 
                    For instance, repetition of a phrase, special usage of punctuations, etc..
                    Please include these special usage as well. Try collect as many memes as possible.
                    Formate your response in a JSON format that can be readily saved as a JSON file, example:
                    [
                        {{
                            "meme": "This is fine",
                            "example_sentence": "When my project deadline is tomorrow, but I haven't started yet: 'This is fine.'",
                            "meaning": "Used sarcastically to describe a situation that is clearly not fine but is being accepted passively.",
                            "source": "KC Green's webcomic 'Gunshow' (2013)"
                        }},
                        {{
                            "meme": "No thoughts, head empty",
                            "example_sentence": "Me staring at my screen for 10 minutes without doing anything: 'No thoughts, head empty.'",
                            "meaning": "Used humorously to describe a state of having no meaningful or intelligent thoughts.",
                            "source": "Originates from an edited drawing of a simplistic cartoon face, spread on Tumblr."
                        }},
                        {{
                            "meme": "It's over 9000!",
                            "example_sentence": "My workload this week? 'It's over 9000!'",
                            "meaning": "Used to exaggerate a large number or overwhelming situation.",
                            "source": "Dragon Ball Z (Vegeta's famous line, 1997 English dub)"
                        }}
                    ]
                    File to be analyzed: {content}
                    '''
        response = call_chat_completion(system_message, user_message)
        save_analysis_as_json(response, str(i))

def save_analysis_as_json(input, segment):
    cleaned_input = input.strip().replace("json\n", "").replace("```", "").strip()
    json_content = json.loads(cleaned_input)
    current_dir = Path(__file__).parent
    filename = "meme_collection_"+str(segment)+".json"
    json_path = current_dir.parent / "data" / filename

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(json_content, file, indent=4, ensure_ascii=False)

    print(f"JSON saved to {json_path}")

def merge_meme_json():
    current_dir = Path(__file__).parent
    json_dir = current_dir.parent / "data"
    file_paths = []
    merged_json = []
    for i in range(90):
        filename = "meme_collection_"+str(i)+".json"
        file_paths.append(json_dir / filename)
    for file_path in file_paths:
        with open(file_path, "r", encoding ="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                merged_json.extend(data)
    merged_filename = "meme_collection_merged.json"
    merged_dir = json_dir / merged_filename
    with open(merged_dir, "w", encoding="utf-8") as output:
        json.dump(merged_json, output, indent=4, ensure_ascii=False)

    print("Merge success. File saved at merged_data.json。")

def open_merged_file():
    merged_dir = Path(__file__).parent.parent / "data" / "meme_collection_merged.json"
    with open(merged_dir, "r", encoding ="utf-8") as file:
        data = json.load(file)
    return data

def generate_comment_with_meme(zone, video_name=""):
    meme_data = open_merged_file()
    json_text = json.dumps(meme_data, indent=4, ensure_ascii=False)
    system_message = "you are a specialist in online meme culture and bullet comment (danmaku) generation"
    user_message = f'''
    Imagine you are a virtual user on Bilibili.
    You will receive a JSON file {json_text} containing various memes, their meanings, and common usage scenarios.
    You will also be given a category: {zone}, which indicates the type of video you are commenting on.
    Additionally, you may receive a video title: {video_name}. Based on the category and title, try to infer the video's content.
    If the title is empty, assume you're commenting on a variety of videos within the given category.
    Your task is to generate 100 bullet comments (danmaku) that viewers might post on Bilibili under the specified video or category.
    Ensure that the provided memes are incorporated while fitting into the zone and inferred video content.
    Output only the generated comments without extra explanations.
    Do not number the comments.
    Avoid repetitive comments.
    Do not end every comment with exclamation mark '!' - end some comments with no punctuations
    Be sure to include some short comments with 2 or 3 characters.
    Format your output so that each comment appears on a new line.
    '''
    response = call_chat_completion(system_message, user_message)
    print(response)
    return response

def get_merged_length(data):
    print(len(data))
    return len(data)

if __name__ == "__main__":
    zone = "鬼畜" # keyword: category
    generate_comment_with_meme(zone,"电棍：Ave Mujica")





