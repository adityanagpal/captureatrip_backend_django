# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class TripLocationMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_location_id',
        'trip_location_name',
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
        'trip_location_id',
        'trip_location_name',
    )


class TripDurationMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_duration_id',
        'trip_duration_name',
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
        'trip_duration_id',
        'trip_duration_name',
    )


class PerkMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'perk_id',
        'perk_name',
        'perk_icon',
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
        'perk_id',
        'perk_name',
        'perk_icon',
    )


class TripMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_id',
        'trip_name',
        'trip_slug',
        'cover_image',
        'banner_image',
        'review_video_url',
        'perk1',
        'perk2',
        'pickup_location',
        'drop_location',
        'starting_cost',
        'duration',
        'trip_description',
        'trip_itinerary',
        'trip_itinerary_pdf',
        'trip_exclusion',
        'trip_inclusion',
        'multiple_costing',
        'note',
        'meta_title',
        'meta_keywords',
        'meta_description',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'perk1',
        'perk2',
        'pickup_location',
        'drop_location',
        'duration',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_id',
        'trip_name',
        'trip_slug',
        'cover_image',
        'banner_image',
        'review_video_url',
        'perk1',
        'perk2',
        'pickup_location',
        'drop_location',
        'starting_cost',
        'duration',
        'trip_description',
        'trip_itinerary',
        'trip_itinerary_pdf',
        'trip_exclusion',
        'trip_inclusion',
        'multiple_costing',
        'note',
        'meta_title',
        'meta_keywords',
        'meta_description',
    )


class SliderTripsAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'slider_trip_id',
        'slider_trip_position',
        'slider_id',
        'trip_id',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'slider_id',
        'trip_id',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'slider_trip_id',
        'slider_id',
        'trip_id',
    )


class TripRelatedImagesAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_related_image_id',
        'trip_id',
        'related_image',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_id',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_related_image_id',
        'trip_id',
        'related_image',
    )


class TripRelatedVideosAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_related_video_id',
        'trip_id',
        'trip_related_video_url',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_id',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_related_video_id',
        'trip_id',
        'trip_related_video_url',
    )


class TripDatesAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_date_id',
        'trip_id',
        'date_value',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_id',
        'date_value',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_date_id',
        'trip_id',
        'date_value',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.TripLocationMaster, TripLocationMasterAdmin)
_register(models.TripDurationMaster, TripDurationMasterAdmin)
_register(models.PerkMaster, PerkMasterAdmin)
_register(models.TripMaster, TripMasterAdmin)
_register(models.SliderTrips, SliderTripsAdmin)
_register(models.TripRelatedImages, TripRelatedImagesAdmin)
_register(models.TripRelatedVideos, TripRelatedVideosAdmin)
_register(models.TripDates, TripDatesAdmin)
