import random

from AbstractPlayer import Player


class RandomPlayer(Player):

    def placepoints(self):
        for _ in range(self.gamestate['m'] if self.playernr == 1 else self.gamestate['n']):
            self.gamestate['points'].append(
                {
                    'x': random.uniform(0, self.gamestate['width']),
                    'y': random.uniform(0, self.gamestate['height']),
                    'player': self.playernr
                })
