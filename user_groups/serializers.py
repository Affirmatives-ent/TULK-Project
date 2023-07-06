from rest_framework import serializers
from .models import ConversationGroup, GroupChat


from rest_framework import serializers


class ConversationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationGroup
        fields = '__all__'


class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'
