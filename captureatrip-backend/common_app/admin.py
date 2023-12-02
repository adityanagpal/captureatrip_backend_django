# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class AdminUserAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'user',
        'admin_uuid',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'user',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'user',
        'admin_uuid',
    )


class HeaderMenuAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'menu_id',
        'menu_name',
        'target_uri',
        'position',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'menu_id',
        'menu_name',
        'target_uri',
        'position',
    )


class HighlightedTripsAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'highlighted_trip_id',
        'highlighted_trip_name',
        'position',
        'target_uri',
        'image',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'highlighted_trip_id',
        'highlighted_trip_name',
        'position',
        'target_uri',
        'image',
    )


class SliderMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'slider_id',
        'position',
        'slider_title',
        'slider_sub_title',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'slider_id',
        'position',
        'slider_title',
        'slider_sub_title',
    )


class BlogMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'blog_id',
        'blog_name',
        'blog_slug',
        'cover_image',
        'banner_image',
        'meta_title',
        'meta_keywords',
        'meta_description',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'blog_id',
        'blog_name',
        'blog_slug',
    )


class TestimonialMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'testimonial_id',
        'video_title',
        'video_url',
        'thumbnail_image',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'testimonial_id',
        'video_title',
        'video_url',
        'thumbnail_image',
    )


class ReviewMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'review_id',
        'reviewer_name',
        'designation',
        'review_image',
        'title',
        'description',
        'rating',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'review_id',
        'reviewer_name',
        'designation',
        'review_image',
        'title',
        'description',
        'rating',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.AdminUser, AdminUserAdmin)
_register(models.HeaderMenu, HeaderMenuAdmin)
_register(models.HighlightedTrips, HighlightedTripsAdmin)
_register(models.SliderMaster, SliderMasterAdmin)
_register(models.BlogMaster, BlogMasterAdmin)
_register(models.TestimonialMaster, TestimonialMasterAdmin)
_register(models.ReviewMaster, ReviewMasterAdmin)
