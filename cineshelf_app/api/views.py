from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from cineshelf_app.api.serializers import (
    MediaStreamSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)
from cineshelf_app.models import MediaStream, StreamPlatform, Review


class ReviewList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReviewDetail(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class StreamPlatformListAV(APIView):
    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(
            stream_platforms, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "stream platform not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StreamPlatformSerializer(
            stream_platform, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream_platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        stream_platform.delete()
        return Response(
            {"msg": "stream platform is deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class MediaStreamListAV(APIView):

    def get(self, request):
        movies = MediaStream.objects.all()
        serializer = MediaStreamSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MediaStreamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaStreamDetailAV(APIView):

    def get(self, request, pk):
        try:
            movie = MediaStream.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "movie not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = MediaStreamSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = MediaStream.objects.get(pk=pk)
        serializer = MediaStreamSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = MediaStream.objects.get(pk=pk)
        movie.delete()
        return Response({"msg": "movie is deleted"}, status=status.HTTP_204_NO_CONTENT)
