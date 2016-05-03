#!/usr/bin/env python

import lxml
import requests
import subprocess
from bs4 import BeautifulSoup

def genius_search(query):
    '''Uses the genius.com search API to return a dictionary of results found by the search engine.'''

    results = []
    API = 'https://api.genius.com'
    ACCESS_TOKEN = 'Za979SFA7_pwCdjDaAsBhnPb3A5jSgcCMixyiDeJv7U415u3ko6Qd14HIJzqrXFj'

    search_endpoint = API + '/search?'
    payload = {'q': query, 'access_token': ACCESS_TOKEN}
    search_request_object = requests.get(search_endpoint, params=payload)

    if search_request_object.status_code == 200:
        json_response = search_request_object.json()

        # Get search entry information from JSON response
        for hit in json_response['response']['hits']:
            artist = hit['result']['primary_artist']['name']
            title = hit['result']['title']
            song_id = hit['result']['id']
            url = hit['result']['url']

            hit_dict = {'artist': artist,
                        'title': title,
                        'song_id': song_id,
                        'url': url
                        }

            results.append(hit_dict)

    return results


def get_lyrics_from_url(song_url):
    '''Uses url key from search result dictionary and parses the lyrics.'''

    get_url = requests.get(song_url)
    song_soup = BeautifulSoup(get_url.text, 'lxml')
    soup_lyrics = song_soup.lyrics.text
    return soup_lyrics


def pick_from_search(results_array):
    '''
    If -s/--search is called, return a list of top results, and prompt choice from list.
    Will continue to prompt until it receives a valid choice. Returns dictionary of the
    appropriate JSON response.
    '''

    for n in range(len(results_array)):
        current = results_array[n]
        result_line = '[{}] {} - {}'.format(n+1, current['artist'], current['title'])
        print(result_line)

    choice = -1
    while choice <= 0 or choice > len(results_array):
        choice = int(input('\nPlease select a song: '))
    actual_choice = choice - 1

    return results_array[actual_choice]


def form_output(search_result):
    '''Forms lyric sheet output for either paging or printing directly to a terminal.'''

    header = '{} - {}'.format(search_result['artist'], search_result['title'])
    divider = '-'*(len(header) + 3)
    lyrics = get_lyrics_from_url(search_result['url'])
    output = header + '\n' + divider + '\n' + lyrics + '\n'
    return output
