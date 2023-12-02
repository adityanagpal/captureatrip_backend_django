from rest_framework import serializers
from common_app.models import SliderMaster, HeaderMenu, HighlightedTrips, TestimonialMaster, ReviewMaster, BlogMaster

class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SliderMaster
        fields = ('slider_id', 'position', 'slider_title', 'slider_sub_title')

class HeaderMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeaderMenu
        fields = ('menu_id', 'menu_name', 'target_uri', 'position')

class HighlightedTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = HighlightedTrips
        fields = ('highlighted_trip_id', 'highlighted_trip_name', 'target_uri', 'position', 'image', 'image_alt_tag')

class TestimonialSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestimonialMaster
        fields = ("video_title", "video_url", "thumbnail_image")

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewMaster
        fields = ("reviewer_name", "designation", "review_image", "review_image_alt_tag", "title", "description", "rating")

class BlogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogMaster
        fields = ("blog_name", "blog_slug", "cover_image", "cover_image_alt_tag", "blog_description")

class BlogDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogMaster
        fields = (
            "blog_name", "cover_image", "cover_image_alt_tag", "banner_image", "banner_image_alt_tag",
            "blog_description", "meta_title", "meta_keywords", "meta_description"
        )

class RecentBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogMaster
        fields = ("blog_name", "blog_slug", "cover_image", "cover_image_alt_tag", "last_updated_date")