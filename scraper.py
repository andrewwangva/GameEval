import os
import pandas as pd
import numpy as np
import requests
from concurrent.futures import ThreadPoolExecutor
import pickle
from tqdm import tqdm
tqdm.pandas()


#ex_urls = ['https://lichess.org/yyznGmXs/black#34', 'https://lichess.org/gyFeQsOE#35']

#put in function to paralleize on pandas


def get_png(ex_url):
    game_id = ex_url.split('/')[3]
    hash_ix = game_id.find('#')
    if hash_ix > 0:
        game_id = game_id[:hash_ix]
    
    download_url = f'https://lichess.org/game/export/{game_id}?evals=0&clocks=0'
    response = requests.get(download_url)
    text_str = str(response.content, 'utf-8')
    new_line_split = text_str.split('\n')
    date = new_line_split[2]
    if '2022' in date or '2023' in date:
        return text_str.split('\n')[-4]
    else:
        return np.nan
nrows = 50000

batch_size = 1000
for i in range(12, nrows//batch_size):
    try:
        puzzles = pd.read_csv('lichess_db_puzzle.csv', skiprows= i* batch_size+1, nrows = batch_size, names = ["PuzzleId","FEN","Moves","Rating","RatingDeviation","Popularity","NbPlays","Themes","GameUrl","OpeningTags"])
        puzzles['pgn'] = puzzles['GameUrl'].progress_apply(get_png)

        puzzles = puzzles[puzzles['pgn'].notna()]
        puzzles.to_json(f'puzzles_annot_{i}.json', orient = 'records', lines=True)
    except Exception as e:
        print(f'{i}', 'didn\'t work')











  