#!/usr/bin/env python

import sys
import argparse
from g_lyrics_funcs import *

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

# Here's where the magic happens
if __name__ == '__main__':
    search_query = ' '.join(args.query)
    search_results = genius_search(search_query)

    if args.search is True:
        user_choice = pick_from_search(search_results)
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
