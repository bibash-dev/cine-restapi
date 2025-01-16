from django.core.checks import register
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters

# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.throttling import (
    UserRateThrottle,
    AnonRateThrottle,
    ScopedRateThrottle,
)
from cineshelf_app.api.serializers import (
    MediaStreamSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)
from cineshelf_app.models import MediaStream, StreamPlatform, Review
from cineshelf_app.api.permissions import (
    IsReviewerOrReadOnly,
    IsAdminOrReadOnly,
)
from cineshelf_app.api.throttling import CreateReviewThrottle, ReviewListThrottle


class UserReview(generics.ListAPIView):
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs["username"]
    #     return Review.objects.filter(reviewer__username=username)

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        return Review.objects.filter(reviewer__username=username)


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [CreateReviewThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        media_stream = MediaStream.objects.get(pk=pk)

        reviewer = self.request.user
        review = Review.objects.filter(media_stream=media_stream, reviewer=reviewer)
        if review.exists():
            raise ValidationError("You have already submitted a review for this media!")

        if media_stream.total_ratings == 0:
            media_stream.average_rating = serializer.validated_data.get("rating")
        else:
            media_stream.average_rating = (
                media_stream.average_rating + serializer.validated_data.get("rating")
            ) / 2
        media_stream.total_ratings += 1
        media_stream.save()
        serializer.save(media_stream=media_stream, reviewer=reviewer)


class ReviewList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active", "reviewer__username"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(media_stream=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_scope = "review-detail"


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


class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
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


class MediaStreamList(generics.ListAPIView):
    queryset = MediaStream.objects.all()
    serializer_class = MediaStreamSerializer
    # filter_backends = [DjangoFilterBackend]
    # search_fields = ["title", "platform__name"]

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "platform__name"]

    # filter_backends = [filters.OrderingFilter]
    # search_fields = ["average_rating"]


class MediaStreamListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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
