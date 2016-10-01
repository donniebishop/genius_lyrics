#!/usr/bin/env python

import sys
import six
import lxml
import requests
from bs4 import BeautifulSoup

# Header uses Client Authorization Token from api.genius.com. As such,
# it is only allowed to request read-only endpoints from the API,
# With that explained, I'm including it here. Mostly because I don't know
# a better way of doing it.

API = 'https://api.genius.com'
HEADERS = {'Authorization': 'Bearer rDyWJrXXwACCg-otwQKmomcYSYFv2oQAN3vlTCV_507CW_pEQTQfQ98HtUYXq3W8'}


class HitResult():
    ''' Class for representing metadata of search results. '''
    def __init__(self, artist, title, song_id, url, api_call):
        self.artist = artist
        self.title = title
        self.song_id = song_id
        self.url = url
        self.api_call = api_call
        self.lyrics = None

        # for use at a later date
        self.referents = []
        self.annotations = []

    def get_lyrics(self):
        '''Looks up song_url, parses page for lyrics and returns the lyrics.'''

        if self.lyrics == None:
            get_url = requests.get(self.url)
            song_soup = BeautifulSoup(get_url.text, 'lxml')

            # Used to extract that stupid google tags thing. I'm a genius.
            [s.extract() for s in song_soup('div', attrs={'class':'dfp_unit'})]

            self.lyrics = song_soup.lyrics
            self.highlighted = [a.text for a in song_soup.lyrics.find_all('a')]
        else:
            return self.lyrics

    def form_output(self):
        '''Forms lyric sheet output for either paging or printing directly to a terminal.'''

        self.get_lyrics()
        header = '{} - {}'.format(self.artist, self.title)
        divider = '-'*(len(header) + 3)
        lyrics = self.lyrics.text

        output = header + '\n' + divider + lyrics + '\n'
        return output

    def get_referents_annotations(self, force=False):
        ''' Use song_id to pull referents for any annotations for the song. '''

        if self.referents == [] or force is True:
            referents_endpoint = API + '/referents'
            payload = {'song_id': self.song_id,
                      'text_format': 'plain', 'per_page': '50'}
            referents_request_object = requests.get(referents_endpoint,
                                                    params=payload,
                                                    headers=HEADERS)

            if referents_request_object.status_code == 200:
                r_json_response = referents_request_object.json()

                for r in r_json_response['response']['referents']:
                    r_class = r['classification']
                    r_frag = r['fragment'].replace('\n ', '\n')
                    r_id = r['id']
                    r_url = r['url']
                    r_api_call = referents_request_object.url

                    self.referents.append(Referent(r_class,
                                                   r_frag,
                                                   r_id,
                                                   r_url,
                                                   r_api_call
                                                   ))

                    for a in r['annotations']:
                        a_id = a['id']
                        a_text = a['body']['plain']
                        a_share = a['share_url']
                        a_url = a['url']
                        a_votes = a['votes_total']
                        a_api_call = API + '/annotations/' + str(a_id)

                        self.annotations.append(Annotation(a_id,
                                                           a_text,
                                                           a_share,
                                                           a_url,
                                                           a_votes,
                                                           a_api_call
                                                           ))

            elif referents_request_object.status_code >= 500:
                pass

        elif self.referents != []:
            return self.referents

    def mark_lyrics(self):
        ''' Mark lyrics for later use with highlighting referents and clicking and
        calling up the related annotation. '''

        marked_lyrics = self.lyrics

        for r in self.referents:
            current = r.fragment
            already_marked = '[% {} %]'.format(current) in marked_lyrics
            if current in marked_lyrics and not already_marked:
                marked_lyrics = marked_lyrics.replace(current, '[% {} %]'.format(current))

        self.lyrics = marked_lyrics


class Referent():
    """ Class for representing referents and their respective annotation. """
    def __init__(self, classification, fragment, annotation_id, url, api_call):
        self.classification = classification
        self.fragment = fragment
        self.annotation_id = annotation_id
        self.url = url
        self.api_call = api_call


class Annotation():
    """ Class for reprsentation of annotation metadata. """
    def __init__(self, annotation_id, text, share_url, url, votes, api_call):
        self.annotation_id = annotation_id
        self.text = text
        self.share_url = share_url
        self.url = url
        self.votes = votes
        self.api_call = api_call


def genius_search(query):
    ''' Uses the genius.com search API to return a list of HitResult instances,
    formed by JSON responses from the search. '''

    results = []

    search_endpoint = API + '/search?'
    payload = {'q': query}
    search_request_object = requests.get(search_endpoint, params=payload, headers=HEADERS)

    if search_request_object.status_code == 200:
        s_json_response = search_request_object.json()
        api_call = search_request_object.url

        # Get search entry information from JSON response
        for hit in s_json_response['response']['hits']:
            artist = hit['result']['primary_artist']['name']
            title = hit['result']['title']
            song_id = hit['result']['id']
            url = hit['result']['url']

            results.append(HitResult(artist, title, song_id, url, api_call))

    elif 400 <= search_request_object.status_code < 500:
        six.print_('[!] Uh-oh, something seems wrong...')
        six.print_('[!] Please submit an issue at https://github.com/donniebishop/genius_lyrics/issues')
        sys.exit(1)

    elif search_request_object.status_code >= 500:
        six.print_('[*] Hmm... Genius.com seems to be having some issues right now.')
        six.print_('[*] Please try your search again in a little bit!')
        sys.exit(1)

    return results


def pick_from_search(results_array):
    ''' If -s/--search is called, return a list of top results, and prompt
    choice from list. Will continue to prompt until it receives a valid choice.
    Returns HitResult instance of the appropriate JSON response. '''

    # Print search result lines
    six.print_()
    for n in range(len(results_array)):
        Current = results_array[n]
        result_line = '[{}] {} - {}'.format(n+1, Current.artist, Current.title)
        six.print_(result_line)

    # Determine user choice
    six.print_('\n[*] Blank line quits genius_lyrics')
    choice = -1
    while choice <= 0 or choice > len(results_array):
        try:
            choice = input('Please select a song number: ')

            if choice == '':
                six.print_()
                sys.exit(0)
            else:
                choice = int(choice)

        except ValueError:
            six.print_('[!] Please enter a number.\n')
            choice = -1

    # Return HitResult instance of chosen song
    actual_choice = choice - 1
    return results_array[actual_choice]

