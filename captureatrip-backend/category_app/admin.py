# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class CategoryMasterAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'category_id',
        'category_name',
        'category_slug',
        'curated_category_position',
        'customized_category_position',
        'cover_image',
        'banner_image',
        'icon_image',
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
        'category_id',
        'category_name',
        'category_slug',
        'curated_category_position',
        'customized_category_position',
        'cover_image',
        'banner_image',
        'icon_image',
        'meta_title',
        'meta_keywords',
        'meta_description',
    )


class TripCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_category_id',
        'trip_id',
        'category_id',
        'is_primary_category',
        'position',
    )
    list_filter = (
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_id',
        'category_id',
        'is_primary_category',
        'created_date',
        'last_updated_date',
        'is_active',
        'is_deleted',
        'trip_category_id',
        'trip_id',
        'category_id',
        'is_primary_category',
        'position',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.CategoryMaster, CategoryMasterAdmin)
_register(models.TripCategory, TripCategoryAdmin)
