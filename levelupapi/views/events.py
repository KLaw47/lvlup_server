from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models import Gamer
from levelupapi.models import Game
from levelupapi.models import Event_Gamer
from rest_framework.decorators import action



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
        uid = request.query_params.get('uid', None)
        gamer = Gamer.objects.get(uid=uid)

        for event in events:
            event.joined = None
            try:
                Event_Gamer.objects.get(event=event, gamer=gamer)
                event.joined = True
            except:
                if  Event_Gamer.DoesNotExist:
                    event.joined = False

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized event instance
        """
        game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(uid=request.data["organizer"])

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=organizer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):

        event = Event.objects.get(pk=pk)
        event.description=request.data["description"]
        event.date=request.data["date"]
        event.time=request.data["time"]
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.data["uid"])
        event = Event.objects.get(pk=pk)
        Event_Gamer.objects.create(
            gamer = gamer,
            event = event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """delete request for user to leave event"""

        gamer = Gamer.objects.get(uid=request.data["uid"])
        event = Event.objects.get(pk=pk)
        event_gamer = Event_Gamer.objects.filter(gamer = gamer, event = event)
        event_gamer.delete()

        return Response({'message': 'Gamer left event'}, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer', 'joined')
        depth = 1
