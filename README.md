# genius_lyrics
The Python genius.com command line lyric searcher.

    usage: genius_lyrics.py [-h] [-s] [-p] query [query ...]

    positional arguments:
      query               Query to search genius.com for. Will automatically
                          select the best result.
    
    optional arguments:
      -h, --help          show this help message and exit
      -s, --search        Display list of top results found. Suppresses automatic
                          selection.
      -p, --print_lyrics  Print lyrics to console; do not send to pager.

Intelligent automatic song selection for geniuses who want their lyrics served up as fast as possible.

Plus a pretty snazzy search selection thingy, if you're into that sort of thing.

Sample:

    ~ $ genius_lyrics.py nujabes --search --print
    [1] Nujabes - Feather
    [2] Nujabes - Luv Sic
    [3] Nujabes - Battlecry
    [4] Nujabes - Lady Brown
    [5] Nujabes - Luv Sic part 3
    [6] Nujabes - Luv(sic) Part 4
    [7] Nujabes - Eclipse
    [8] Nujabes - Think Different
    [9] Nujabes - Sky Is Tumbling
    [10] Nujabes - The Sign
    
    Please select a song number: 1
    
    Nujabes - Feather
    --------------------
    
    [Verse 1: Cise Starr]
    Light as a feather when I'm floating through
    Reading through the daily news
    Measuring the hurt within the golden rule
    Centimetres of ether, I'm heating the speaker
    Motivational teacher with words that burn people
    Seeing the headlines lined with discord
    It's either genocide or the planet in uproar
    Never good.  The rules of paradise are never nice
    The best laid plans of Mice and Men are never right
    ...

A silly little project of mine, that I take way too seriously. 

Best Enjoyed with Wordy Songs.
