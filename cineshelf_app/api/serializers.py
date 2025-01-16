from rest_framework import serializers
from cineshelf_app.models import MediaStream, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ["media_stream"]
        read_only_fields = ("created_at", "updated_at")


class MediaStreamSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source="platform.name")

    class Meta:
        model = MediaStream
        fields = "__all__"
        read_only_fields = ("created_at",)


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    media_streams = MediaStreamSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="stream-platform-detail",
    )

    class Meta:
        model = StreamPlatform
        fields = "__all__"
