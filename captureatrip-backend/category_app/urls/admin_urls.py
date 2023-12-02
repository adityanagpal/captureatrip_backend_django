from django.urls import path
from category_app.views import admin_views

urlpatterns = [
    path('', admin_views.AdminCategoryListCreate.as_view()),
    path('<int:pk>/', admin_views.AdminCategoryViewUpdate.as_view()),
]