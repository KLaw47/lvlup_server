from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models import Game_Type
from levelupapi.models import Gamer

class GameView(ViewSet):

    def retrieve(self, request, pk):

        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):

        games = Game.objects.all()
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(uid=request.data["user_id"])
        game_type = Game_Type.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
        title=request.data["title"],
        maker=request.data["maker"],
        number_of_players=request.data["number_of_players"],
        skill_level=request.data["skill_level"],
        gamer=gamer,
        game_type=game_type
    )
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
        Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = Game_Type.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 1
