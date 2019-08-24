from django.contrib.auth.models import User

from rest_framework import serializers, views, response

from oauth2_provider.contrib.rest_framework import (
    IsAuthenticatedOrTokenHasScope
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProfileView(views.APIView):
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    serializer_class = UserSerializer
    required_scopes = ['read:user']

    def get(self, request, format=None):
        user = request.user
        return response.Response(UserSerializer(user).data)
