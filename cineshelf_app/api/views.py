from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

# from rest_framework import mixins
from rest_framework import viewsets
from cineshelf_app.api.serializers import (
    MediaStreamSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)
from cineshelf_app.models import MediaStream, StreamPlatform, Review


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        media_stream = MediaStream.objects.get(pk=pk)

        serializer.save(media_stream=media_stream)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(media_stream=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# class ReviewList(
#     mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
# ):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ReviewDetail(
#     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
# ):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#


# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(
#             queryset, many=True, context={"request": request}
#         )
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         media_stream = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(
#             media_stream, context={"request": request}
#         )
#         return Response(serializer.data)


class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
    serializer_class = StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()


# class StreamPlatformListAV(APIView):
#     def get(self, request):
#         stream_platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(
#             stream_platforms, many=True, context={"request": request}
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class StreamPlatformDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             stream_platform = StreamPlatform.objects.get(pk=pk)
#         except ObjectDoesNotExist:
#             return Response(
#                 {"error": "stream platform not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = StreamPlatformSerializer(
#             stream_platform, context={"request": request}
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream_platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#         stream_platform.delete()
#         return Response(
#             {"msg": "stream platform is deleted"}, status=status.HTTP_204_NO_CONTENT
#         )


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
