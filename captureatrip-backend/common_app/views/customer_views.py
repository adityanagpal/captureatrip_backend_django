from  rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models.functions import Substr

from common_app.models import SliderMaster, HeaderMenu, HighlightedTrips, TestimonialMaster, ReviewMaster, BlogMaster
from common_app.serializers import SliderSerializer, HeaderMenuSerializer, HighlightedTripSerializer, TestimonialSerializer,\
    ReviewSerializer, BlogListSerializer, BlogDetailSerializer, RecentBlogSerializer

# Create your views here.
class SliderList(ListAPIView):
    serializer_class = SliderSerializer
    queryset = SliderMaster.objects.all().order_by('position')

class SliderView(RetrieveAPIView):
    serializer_class = SliderSerializer
    queryset = SliderMaster.objects.all()

class HeaderMenuList(ListAPIView):
    serializer_class = HeaderMenuSerializer
    queryset = HeaderMenu.objects.filter(is_active=True).order_by('position')

class HighlightedTripList(ListAPIView):
    serializer_class = HighlightedTripSerializer
    queryset = HighlightedTrips.objects.filter(is_active=True).order_by('position')

class TestimonialList(ListAPIView):
    queryset = TestimonialMaster.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

class ReviewList(ListAPIView):
    queryset = ReviewMaster.objects.filter(is_active=True)
    serializer_class = ReviewSerializer

class BlogList(ListAPIView):
    queryset = BlogMaster.objects.all()
    serializer_class = BlogListSerializer

class BlogView(RetrieveAPIView):
    queryset = BlogMaster.objects.all()
    serializer_class = BlogDetailSerializer
    lookup_field = 'blog_slug'

class RecentBlogsList(ListAPIView):
    queryset = BlogMaster.objects.all().order_by('last_updated_date')[:8]
    serializer_class = RecentBlogSerializer