from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class CommonModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class AdminUser(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    admin_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

'''
Note: Below table contains trips as well as categories, defined by target URI
'''
class HeaderMenu(CommonModel):
    menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=255)
    target_uri = models.CharField(max_length=128)
    position = models.PositiveIntegerField(default=0, null=True, blank=True)

'''
Note: Below table contains trips as well as categories, defined by target URI
'''
class HighlightedTrips(CommonModel):
    highlighted_trip_id = models.AutoField(primary_key=True)
    highlighted_trip_name = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=0, null=True, blank=True)
    target_uri = models.CharField(max_length=128)
    image = models.ImageField(upload_to='uploads/menu/highlighted/images', null=True, blank=True)
    image_alt_tag = models.CharField(max_length=128, null=True, blank=True)

class SliderMaster(CommonModel):
    slider_id = models.AutoField(primary_key=True)
    position = models.PositiveIntegerField(default=0, null=True, blank=True)
    slider_title = models.CharField(max_length=128)
    slider_sub_title = models.CharField(max_length=128, blank=True, null=True)

class BlogMaster(CommonModel):
    blog_id = models.AutoField(primary_key=True)
    blog_name = models.CharField(max_length=255)
    blog_slug = models.SlugField(max_length=255, unique=True)
    cover_image = models.ImageField(upload_to='uploads/blog/images/cover')
    cover_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    banner_image = models.ImageField(upload_to='uploads/blog/images/banner')
    banner_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    blog_description = models.TextField()
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['blog_slug'])
        ]

class TestimonialMaster(CommonModel):
    testimonial_id = models.AutoField(primary_key=True)
    video_title	= models.CharField(max_length=255, null=True, blank=True)
    video_url = models.URLField(max_length=1024)
    thumbnail_image = models.ImageField(upload_to='uploads/testimonial/images/thumb')

class ReviewMaster(CommonModel):
    review_id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=255, null=True, blank=True)
    designation	= models.CharField(max_length=255, null=True, blank=True)
    review_image = models.ImageField(upload_to='uploads/review/images')
    review_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    rating = models.PositiveIntegerField(default=0)