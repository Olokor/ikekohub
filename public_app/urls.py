from django.urls import include, path

from django.contrib import admin

from public_app.views import CreateSchoolView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-school/', CreateSchoolView.as_view(), name='create-school'),
]