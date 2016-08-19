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

    ~ $ genius_lyrics.py eden sex --search --print_lyrics
    [1] EDEN - Sex
    [2] De Jeugd van Tegenwoordig - Op Een Sexuele Wijze
    [3] Seventh Seal - Eden
    [4] Nicki Minaj - Freaky Girl (Wanna Minaj?)
    [5] Trey Songz - Playin' Hard
    [6] Frank Ocean - Static
    [7] Home Brew Crew - Datura/White Flowers
    [8] SFB - Tanken
    [9] Cam'ron - Glory
    [10] Da Lench Mob - All on My Nutsac

    Please select a song number: 1

    EDEN - Sex
    -------------

    [Verse 1]
    And I said, "what's up?
    What you been thinking?"
    Cause you've been staring at that roof so long I'd swear it's come alive
    And she spoke nine words
    And now we're sinking
    But I can't find it in myself to want to lie to keep this thing from going down
    ...

A silly little project of mine, that I take way too seriously. 

Best Enjoyed with Wordy Songs.
