
from django.contrib import admin
from django.urls import path,include
import myapp,users


from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("myapp/",include("myapp.urls")),
    path("users/",include("users.urls")),
   
]

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)