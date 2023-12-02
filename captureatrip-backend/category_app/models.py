from django.db import models
from common_app.models import CommonModel

# Create your models here.
class CategoryMaster(CommonModel):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)
    category_slug = models.SlugField(max_length=255, unique=True)
    category_description_heading = models.CharField(max_length=255, null=True, blank=True)
    category_description = models.TextField(null=True, blank=True)
    curated_category_position = models.PositiveIntegerField(default=0, null=True, blank=True)
    customized_category_position = models.PositiveIntegerField(default=0, null=True, blank=True)
    cover_image = models.ImageField(upload_to='uploads/category/images/cover')
    cover_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    banner_image = models.ImageField(upload_to='uploads/category/images/banner')
    banner_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    icon_image = models.ImageField(upload_to='uploads/category/images/icon')
    icon_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['category_slug'])
        ]

class TripCategory(CommonModel):
    trip_category_id = models.AutoField(primary_key=True)
    trip_id = models.ForeignKey('trip_app.TripMaster', on_delete=models.CASCADE, related_name='trip_category')
    category_id = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE, related_name='category_in_trip')
    is_primary_category = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0, null=True, blank=True) # 0 means no position defined

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip_id', 'category_id'], name="unique_trip_category"),
        ]