from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
)
from cineshelf_app.api.pagination import (
    MediaStreamCursorPagination,
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
    serializer_class = ReviewSerializer

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
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
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


class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()


class MediaStreamList(generics.ListAPIView):
    queryset = MediaStream.objects.all()
    serializer_class = MediaStreamSerializer
    pagination_class = MediaStreamCursorPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "platform__name"]


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
