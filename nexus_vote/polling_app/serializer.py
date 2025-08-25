from rest_framework import serializers
from polling_app.models import User, Poll, Registration, Vote, VoteOption


class userSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"
        
class pollSerializer(serializers.Serializer):
    # created_by 
    id = serializers.IntegerField(read_only=True)
    creater_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    poll_name = serializers.CharField(max_length=255)
    question = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    expiring_date = serializers.DateField()
    is_active = serializers.BooleanField(default=True)
    
    
    def create(self, validated_data):
        new_poll = Poll.objects.create(**validated_data)
        new_poll.save()
        return new_poll

        
    
    
    def update(self, instance, validated_data):
        """Update an existing poll instance"""
        # Update all fields that are provided
        instance.creater_by = validated_data.get('creater_by', instance.creater_by)
        instance.poll_name = validated_data.get('poll_name', instance.poll_name)
        instance.question = validated_data.get('question', instance.question)
        instance.expiring_date = validated_data.get('expiring_date', instance.expiring_date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        
        instance.save()
        return instance
