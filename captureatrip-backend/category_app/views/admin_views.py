from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from category_app.serializers import AdminCategorySerializer
from category_app.models import CategoryMaster
from django.contrib.sitemaps import Sitemap

# Create your views here.
class AdminCategoryListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CategoryMaster.objects.all().prefetch_related('category_in_trip').order_by('-category_id')
    serializer_class = AdminCategorySerializer

class AdminCategoryViewUpdate(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CategoryMaster.objects.all()
    serializer_class = AdminCategorySerializer

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return CategoryMaster.objects.all().order_by('-category_id')

    def lastmod(self, obj):
        return obj.last_updated_date
        
    def location(self,obj):
        return '/%s' % (obj.category_slug)