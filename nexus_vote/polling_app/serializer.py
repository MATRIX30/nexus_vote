from rest_framework import serializers
from polling_app.models import User, Poll, Registration, Vote, VoteOption


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
