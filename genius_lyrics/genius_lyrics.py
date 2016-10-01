#!/usr/bin/env python

import argparse
import tempfile
import subprocess
from genius_lyrics.backend import *

# Here's where the magic happens
def main():
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
    search_query = ' '.join(args.query)
    search_results = genius_search(search_query)

    if args.search is True:
        UserChoice = pick_from_search(search_results)
        all_together_now = UserChoice.form_output()
    else:
        TopResult = search_results[0]
        all_together_now = TopResult.form_output()

    if args.print_lyrics is True:
        six.print_('\n' + all_together_now,)
    else:
        with tempfile.NamedTemporaryFile(prefix='glyrics_', dir='/tmp') as t:
            try:
                t.write(bytes(all_together_now, 'UTF-8'))
            except TypeError:
                t.write(bytes(all_together_now))
            t.seek(0)
            command_list = ['/bin/less', t.name]
            subprocess.call(command_list)
        six.print_()

if __name__ == '__main__':
    main()
