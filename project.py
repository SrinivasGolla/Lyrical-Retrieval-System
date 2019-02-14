import urllib.request
import urllib.error
from lxml import html
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import requests
import re
import csv
from collections import Counter
import numpy as np
import json
import sys
import time

song = {}
final_keys = set()
# final_keys.add("")
final_index = []
final_matrix = []


def starter():
    for i in range(97,98):
        url = 'https://www.lyricsfreak.com/'+chr(i)+'_top.html'
        print(url)
        try:
            # response = requests.get(url)
            response = urllib.request.Request(url)
            html=urllib.request.urlopen(response).read()        
        except urllib.error.HTTPError as e:
            print("error")
        
        soup=BeautifulSoup(html,'html.parser') 
        artist_names=soup.select('td.colfirst')
        one_song = {}
        j = 0
        for links in artist_names:
            y = links.find_all('a')
            one_artist = {}
            j = j + 1
            for tag in y:
                
                artist = tag.get_text()[1:-7]
                # print(artist)
                # print("****************")
                one_artist["name"] = artist.strip()
                one_artist["link"] = "https://www.lyricsfreak.com"+tag.get('href')
                # artist_links[artist.strip()] = "https://www.lyricsfreak.com"+tag.get('href')
            # one_song["artist_details"] = one_artist
            # print(one_artist)
            if(j == 2):
                break
            try:
                response = urllib.request.Request(one_artist["link"])
                html=urllib.request.urlopen(response).read()        
            except urllib.error.HTTPError as e:
                print("error")
            soup=BeautifulSoup(html,'html.parser')
            songs_links=soup.select('div.lf-list__cell--full')
            i = 0  # remove it later
            for songs in songs_links:
                i = i + 1
                # print(i)
                data = songs.find_all('a')
                song_store = {}
                namer = ""

                for name in data:
                    namer = name.get_text()[1:-7]
                    
                    # print(song_name)
                    song_store[namer.strip()] = "https://www.lyricsfreak.com"+name.get('href')
                    # print(store)
                one_song["song_link"] = "https://www.lyricsfreak.com"+name.get('href')
                # final_index.append(one_song["song_link"])
                # print(namer)
                final_index.append(namer)
                # print(final_index)
                one_song["artist_details"] = one_artist
                ch_song = tokenizer(one_song['song_link'])
                if(ch_song != None):
                    one_song["song_tokens"] = tokenizer(one_song['song_link'])
                else:
                    one_song["song_tokens"] = None
                
                song[namer] = one_song
                one_song = {}
                if(i == 2):
                    break

def tokenizer(url):
    # print(soup.find_all('p'))
    soup = BeautifulSoup(urlopen(url).read(),"lxml")
    asd=soup.find(class_='lyrictxt')
    if(asd != None):
        one = asd.get_text()
        tokens2 = []
        tokens2.extend(re.findall('\w+',one))
        tokens2 = [element.lower() for element in tokens2]
        doc_length = len(tokens2)
        word_count = Counter(tokens2)
        li = set()
        for k,v in word_count.items():
            word_count[k] = v/doc_length
            # final_keys.append(k)
            final_keys.add(k)
        # print(li)
        # final_keys = final_keys.union(li)
        # print(final_keys)
        return word_count
    else:
        return None

def load_from_file():
    with open('dataIR.json', 'r') as fp:
        songer = json.load(fp)    
    song = dict(songer)
    # print(song)
    for i in song:
        final_index.append(i)
        x = song[i]
        for j in x["song_tokens"]:
            # print(j)
            # time.sleep(0.5)
            final_keys.add(j)
    return song
    



def matrix_design():
    # print("entered")
    # print(final_keys)
    # print(final_index)
    # print(song)
    # token_index.remove("")
    token_index = list(final_keys)
    # token_index.remove("")
    song_index = list(final_index)
    
    # print(song_index)
    mat = []
    for i in song_index:
        # print(song[i])
        # current = Counter(song[i].get("song_tokens"))
        current = song[i].get("song_tokens")
        
    # print("current len " + str(len(current)))
        t = []
        # try:
        for j in token_index:
            # if j != "":
            if j in current:
                t.append(current[j])
            else:
                t.append(0)
            # else:
                # t.append(0)
    # except KeyError as e:
        # print("token missing" + j)
            # print(t)
        mat.append(t)
    return np.asarray(mat)
# starter()
# final_matrix = matrix_design()
# print(final_keys)

def search_query(query):
    
    song_index = list(final_index)
    token_index = list(final_keys)
    s = query.split(' ')
    # ts = []
    total_list = []
    # for i in s:
    #     if i not in token_index:
    #         ts.append(i.lower())
    for i in s:
        # print(i)
        if i in token_index:
            pl = token_index.index(i)
            # print(pl)
            total_list.append(final_matrix[:,pl])
        else:
            print(i +" is missing")
#     num_of_words = len(total_list)
    # print(total_list)
    user_songs = []
    for i in range(len(song_index)):
        sub_total = 0
        num_total = 0
        for j in range(len(total_list)):
            if(total_list[j][i] != 0):
                sub_total = sub_total + total_list[j][i]+1
                num_total = num_total + 1
        if(num_total > 0):
            user_songs.append([i,sub_total,num_total])
        # print(user_songs)
    user_songs = sorted(user_songs, key=lambda x: x[1],reverse=True)
    
    
    for i in user_songs:
        # print(song_index[i[0]])
        urlsong=song[song_index[i[0]]]['song_link']
        print(urlsong)

        
song = load_from_file()
# print(song)
final_matrix = matrix_design()
while(1):

    query = input("enter the search query")
    search_query(query)
    x = input("press 0 to exit or 1 to continues : ")
    if(x == 0):
        sys.exit()

# starter()
# final_matrix = matrix_design()
# with open('data.json', 'w') as fp:
#     json.dump(song, fp)

# print(song)
# print()