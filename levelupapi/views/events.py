from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models import Gamer
from levelupapi.models import Game

class EventView(ViewSet):

    def retrieve(self, request, pk):

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):

        events = Event.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
                events = events.filter(game_id=game)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):

        organizer = Gamer.objects.get(uid=request.data["user_id"])
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
        description=request.data["description"],
        date=request.data["date"],
        time=request.data["time"],
        organizer=organizer,
        game=game
    )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):

        event = Event.objects.get(pk=pk)
        event.description=request.data["description"],
        event.date=request.data["date"],
        event.time=request.data["time"],
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
