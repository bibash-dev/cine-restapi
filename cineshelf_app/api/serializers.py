from rest_framework import serializers
from cineshelf_app.models import MediaStream, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class MediaStreamSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = MediaStream
        fields = "__all__"


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    media_streams = MediaStreamSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="platform-detail",
    )

    class Meta:
        model = StreamPlatform
        fields = "__all__"
