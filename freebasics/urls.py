import os

from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from . import views

# if settings.MICROSOFT_AUTH_LOGIN_ENABLED:
#     urlpatterns = [
#         path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),
#     ]
# else:

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.HomeView.as_view(), name='index'),
    path('<int:article_id>/', views.ArticleView.as_view(), name='article'),
    path('sections/<int:section_id>/', views.SectionView.as_view(), name='section'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
