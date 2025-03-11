from meme_detecter import *
from danmaku_finder import *
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu
import textstat
import spacy
import numpy as np
import torch

# attempts for evaluation metrics on similarity for experiment 2

def save_ai_comment(data, filename):
    current_dir = Path(__file__).parent
    output_dir = current_dir.parent / "generated_bullet_comments" / filename
    comments = [line.strip() for line in data.split(" ") if line.strip()]
    with open(output_dir, "w", encoding="utf-8") as output:
        for comment in comments:
            output.write(comment + "\n") 

# Readability Score
def calculate_readability(text):
    scores = {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade Level": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text)
    }
    return scores

# Syntactic Similarity
nlp = spacy.load("en_core_web_sm")
def syntactic_similarity(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    dep_sim = sum([1 for token1, token2 in zip(doc1, doc2) if token1.dep_ == token2.dep_]) / max(len(doc1), len(doc2))
    pos_sim = sum([1 for token1, token2 in zip(doc1, doc2) if token1.pos_ == token2.pos_]) / max(len(doc1), len(doc2))
    syntax_score = (dep_sim + pos_sim) / 2

    return {
        "Dependency Similarity": dep_sim,
        "POS Similarity": pos_sim,
        "Overall Syntactic Similarity": syntax_score
    }

def read_two_files(bvid):
    cid = get_cid(bvid)
    home_dir = Path(__file__).parent.parent
    original_filename = str(cid)+".txt"
    ai_filename = str(cid)+"_ai_generated.txt"
    original_dir = home_dir / "individual_bullet_comments" / original_filename
    ai_dir = home_dir / "generated_bullet_comments" / ai_filename
    with open(original_dir, "r", encoding ="utf-8") as file:
        original_content = file.read()
    with open(ai_dir, "r", encoding ="utf-8") as file:
        ai_content = file.read()
    return original_content, ai_content

def cosine_sim_strings(str1, str2):
    """
    cosine similarity
    """
    vectorizer = CountVectorizer()
    corpus = [str1, str2]
    X = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(X[0], X[1])
    print("Cosine similarity:", similarity[0][0])
    return similarity[0][0]

def cosine_sim_strings_tfidf(str1, str2):
    """
    cosine similarity using tf_dif
    """
    vectorizer = TfidfVectorizer()
    corpus = [str1, str2]
    X = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(X[0], X[1])
    print("Cosine similarity (tf_idf):", similarity[0][0])
    return similarity[0][0]

def jaccard_similarity(str1, str2):
    """
    jaccard_similarity
    """
    set1 = set(str1.split())
    set2 = set(str2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    print("Jaccard Similarity:", len(intersection) / len(union))
    return len(intersection) / len(union)

def bleu_score(str1, str2):
    """
    calculate bleu score
    """
    reference = [str1.split()]
    candidate = str2.split()
    print(f"BLEU score:{sentence_bleu(reference, candidate)}")
    return sentence_bleu(reference, candidate)

def create_ai_comment_for_video(bvid):
    cid = get_cid(bvid)
    title = get_video_title(bvid)
    category = get_video_category(bvid)
    print(f"视频名称：{title}")
    print(f"视频的cid为: {cid}")
    print(f"视频分区：{category}")
    comments = generate_comment_with_meme(category,title)
    cleaned_comments = comments.replace("- ", "").replace("\n"," ")
    filename = str(cid)+"_ai_generated.txt"
    save_ai_comment(cleaned_comments, filename)
    print(f"video {cid}: ai comments generated.")

if __name__ == "__main__":
    bvid_list = read_bvid_from_file()
    '''
    if bvid_list:
        for bvid in bvid_list:
            original, ai = read_two_files(bvid)
            sim_info = syntactic_similarity(original, ai)
            print(f"video {bvid}: {sim_info}")
            #original_readability_score = calculate_readability(original)
            #i_readability_score = calculate_readability(ai)
            #print (f"Readability - original:{original_readability_score},ai:{ai_readability_score}")
    #original, ai = read_two_files(bvid)
    #print(type(original))
    #print(type(ai))
    #bleu_score(original, ai)
    '''
    a = "折木奉太郎＆秋山澪。结婚去啊！！"
    b = "秋山澪和折木奉太郎的故事真甜"
    sim_info = syntactic_similarity(a, b)
    print(sim_info)