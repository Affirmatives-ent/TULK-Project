from rest_framework import serializers
from .models import ConversationGroup, GroupChat


from rest_framework import serializers


class ConversationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationGroup
        fields = '__all__'


class ConversationGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('members')


class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'
