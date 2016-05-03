#!/usr/bin/env python

import sys
import lxml
import json
import requests
import argparse
import tempfile
import subprocess
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='The Python genius.com commandline lyric searcher.')

parser.add_argument('query', nargs='+',
                    help='Query to search genius.com for. Will automatically select the best result.')
parser.add_argument('-s', '--search',
                    action='store_true', default=False,
                    help='Display list of top results found. Suppresses automatic selection.')
parser.add_argument('-p', '--print_lyrics',
                    action='store_true', default=False,
                    help='Print lyrics to console; do not send to pager.')

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

API = 'https://api.genius.com'
ACCESS_TOKEN = 'Za979SFA7_pwCdjDaAsBhnPb3A5jSgcCMixyiDeJv7U415u3ko6Qd14HIJzqrXFj'


def genius_search(query):
    '''Uses the genius.com search API to return a dictionary of results found by the search engine.'''

    results = []

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


def make_soup(url):
    '''Takes URL and returns a BeautifulSoup object for parsing.'''

    get_url = requests.get(url)
    soup = BeautifulSoup(get_url.text, 'lxml')
    return soup


def get_lyrics_from_url(song_url):
    '''Uses url key from search result dictionary and parses the lyrics.'''

    song_soup = make_soup(song_url)
    soup_lyrics = song_soup.lyrics.text
    return soup_lyrics


def pick_from_search():
    '''
    If -s/--search is called, return a list of top results, and prompt choice from list.
    Will continue to prompt until it receives a valid choice.
    '''

    for n in range(len(search_results)):
        current = search_results[n]
        result_line = '[{}] {} - {}'.format(n+1, current['artist'], current['title'])
        print(result_line)

    choice = -1
    while choice <= 0 or choice > len(search_results):
        choice = int(input('\nPlease select a song: '))
    actual_choice = choice - 1

    return search_results[actual_choice]


def form_output(search_result):
    '''Forms lyric sheet output for either paging or printing directly to a terminal.'''

    header = '{} - {}'.format(search_result['artist'], search_result['title'])
    divider = '-'*(len(header) + 3)
    lyrics = get_lyrics_from_url(search_result['url'])
    output = header + '\n' + divider + '\n' + lyrics + '\n'
    return output


# Here's where the magic happens
if __name__ == '__main__':
    search_query = ' '.join(args.query)
    search_results = genius_search(search_query)

    if args.search is True:
        user_choice = pick_from_search()
        all_together_now = form_output(user_choice)
    else:
        top_result = search_results[0]
        all_together_now = form_output(top_result)

    if args.print_lyrics is True:
        print('\n' + all_together_now,)
    else:
        with tempfile.NamedTemporaryFile(dir='/tmp') as t:
            t.write(bytes(all_together_now, 'UTF-8'))
            t.seek(0)
            command_list = ['/bin/less', t.name]
            subprocess.call(command_list)
    print()
