from django.urls import path
from common_app.views import admin_views
from django.contrib.sitemaps.views import sitemap

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from category_app.views.admin_views import CategorySitemap
from trip_app.views.admin_views import TripSitemap, UpcomingTripSitemap

SITEMAPS = {
    'home': admin_views.HomeSitemap,
    'category': CategorySitemap,
    'trip': TripSitemap,
    'upcoming_trip': UpcomingTripSitemap,
    'blog': admin_views.BlogSitemap,
    'static': admin_views.StaticSitemap
}

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot_password/', admin_views.AdminForgotPassword.as_view()),
    path('reset_password/', admin_views.AdminResetPassword.as_view()),

    path('slider/<int:pk>/', admin_views.AdminSliderViewUpdate.as_view()),

    path('menu/header/', admin_views.AdminHeaderMenuList.as_view()),
    path('menu/header/<int:pk>/', admin_views.AdminHeaderMenuViewUpdate.as_view()),
    path('menu/highlighted_trips/', admin_views.AdminHighlightedTripList.as_view()),
    path('menu/highlighted_trips/<int:pk>/', admin_views.AdminHighlightedTripViewUpdate.as_view()),

    path('testimonial/video/', admin_views.AdminTestimonialListCreate.as_view()),
    path('testimonial/video/<int:pk>/', admin_views.AdminTestimonialViewUpdate.as_view()),
    path('testimonial/review/', admin_views.AdminReviewListCreate.as_view()),
    path('testimonial/review/<int:pk>/', admin_views.AdminReviewViewUpdate.as_view()),

    path('blog/', admin_views.AdminBlogListCreate.as_view()),
    path('blog/<int:pk>/', admin_views.AdminBlogViewUpdate.as_view()),

    path('sitemap/generate/', sitemap, {'sitemaps': SITEMAPS, 'template_name': 'common_app/sitemap/custom_sitemap.html'}),
    path('sitemap/upload/', admin_views.UploadSitemap.as_view()),

    path('ckeditor/upload/', admin_views.CKEditorFileUpload.as_view()),
]