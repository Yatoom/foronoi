import random

from AbstractPlayer import Player

class RandomPlayer(Player):

    def _placepoints(self):
        for i in range(self._gamestate['m'] if self._playernr == 1 else self._gamestate['n']):
            self._gamestate['points'].append({'x': random.uniform(0,self._gamestate['width']), 'y': random.uniform(0,self._gamestate['height'])})
