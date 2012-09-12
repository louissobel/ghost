ghost
=====

AI for Ghost word game

[Ghost](http://en.wikipedia.org/wiki/Ghost_%28game%29)

This is a project I worked on last year, I recently cleaned it up a little.

The interface need to be cleaned up, but the guts are all there.

I can't remember where the current word list, `ghost\_words` is from. Probably the scrabble dictionary.

Type `python ghost.py h c` to play against the computer. 'LLAMA' is your only hope.

Type `python ghost.py c c c` to watch three computers play

I need to work on it a little, the next step I'm thinking (to make it more fun)
is to make the computer non-omniscient by making the set of words that it knows
each game (or round or turn) stochastic. Ideally weighted by how likely it would be
that a human knows a given word. Right now, `ghost\_words` doesn't include a lot of common words because the common word
has an uncommon word as a prefix. So there would have to be logic to select words that the
computer knows from the whole universe of words, then recompute the possible words in ghost.


