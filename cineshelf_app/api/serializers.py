from rest_framework import serializers

from cineshelf_app.models import Movie

def name_length(value):
    if len(value) < 3:
        raise serializers.ValidationError("Name must be at least 3 characters")

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and Description cannot be the same.")
        return data

    # def validate_name(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError("The name must be greater than 3 characters long")
    #     return value
