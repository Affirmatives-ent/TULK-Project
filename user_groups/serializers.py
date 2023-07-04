from rest_framework import serializers
from .models import ConversationGroup


from rest_framework import serializers


class ConversationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationGroup
        fields = '__all__'
