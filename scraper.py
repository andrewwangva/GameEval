import os
import pandas 
import numpy
import requests

ex_urls = ['https://lichess.org/yyznGmXs/black#34', 'https://lichess.org/gyFeQsOE#35']

#put in function to paralleize on pandas

def get_png(ex_url):
    game_id = ex_url.split('/')[3]
    hash_ix = game_id.find('#')
    if hash_ix > 0:
        game_id = game_id[:hash_ix]
    
    download_url = f'https://lichess.org/game/export/{game_id}?evals=0&clocks=0'
    response = requests.get(download_url)
    text_str = str(response.content, 'utf-8')
    pgn = text_str.split('\n')[-4]

    return pgn 
    

  