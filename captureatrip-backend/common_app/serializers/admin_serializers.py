from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from common_app.models import SliderMaster, HeaderMenu, HighlightedTrips, TestimonialMaster, ReviewMaster, BlogMaster

class AdminSliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SliderMaster
        fields = ("slider_title", "slider_sub_title")

class AdminHeaderMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeaderMenu
        fields = ("menu_id", "menu_name", "target_uri", "position", "is_active")

class AdminHighlightedTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = HighlightedTrips
        fields = (
                "highlighted_trip_id", "highlighted_trip_name", "target_uri", "position", "image", 
                "image_alt_tag", "is_active"
            )

class AdminTestimonialSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestimonialMaster
        fields = ("testimonial_id", "video_title", "video_url", "thumbnail_image", "is_active")

class AdminReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewMaster
        fields = (
            "review_id", "reviewer_name", "designation", "review_image", "review_image_alt_tag", "title",
            "description", "rating", "is_active"
        )

class AdminBlogSerializer(serializers.ModelSerializer):
    blog_slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=BlogMaster.objects.all(), message='This slug already exists')]
    )

    class Meta:
        model = BlogMaster
        fields = (
            "blog_id", "blog_name", "blog_slug", "cover_image", "cover_image_alt_tag", "banner_image", 
            "banner_image_alt_tag", "blog_description", "meta_title", "meta_keywords", "meta_description"
        )

class AdminBlogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogMaster
        fields = ("blog_id", "blog_name", "cover_image")