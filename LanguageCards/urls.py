from django.contrib import admin
from django.urls import path, include
from cards import views as cards_v
from reg import views as reg_v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cards_v.main),
    path('signup/', reg_v.register, name='signup'),
    path('', include('django.contrib.auth.urls'), name='login'),
    path('', include('django.contrib.auth.urls'), name='logout'),
    path('word/<str:date>/', cards_v.word, name='word')
]

