from rest_framework import serializers
from .models import ConversationGroup, GroupInvitation, GroupPost, GroupMedia, Like, Comment


from rest_framework import serializers


class ConversationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationGroup
        fields = '__all__'


class GroupInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvitation
        fields = '__all__'


class ConversationGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('members')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class GroupMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMedia
        fields = '__all__'


class GroupPostSerializer(serializers.ModelSerializer):
    files = GroupMediaSerializer(many=True, required=False)

    class Meta:
        model = GroupPost
        fields = ['id', 'author', 'group', 'content', 'files', 'created_at']
