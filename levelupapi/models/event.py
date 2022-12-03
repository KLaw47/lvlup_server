from django.db import models
from .game import Game
from .gamer import Gamer

class Event(models.Model):
    description = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
