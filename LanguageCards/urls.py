from django.conf import settings
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
    path('word/<str:date>/', cards_v.word, name='word'),
    path('add/', cards_v.add, name='add'),
    path('learn/', cards_v.learn, name='learn'),
    path('learn/one/', cards_v.one, name='one'),
    path('learn/type/', cards_v.type, name='type'),
    path('translate/', cards_v.translate, name='translate'),
    path('vocabulary/', cards_v.vocab, name='vocab')
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
