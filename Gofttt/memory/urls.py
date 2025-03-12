from django.urls import path
from .views import *
from django.conf import settings  
from django.conf.urls.static import static  
 
app_name = 'memory'
 
urlpatterns = [
    path("", MemoriesView.as_view(), name='makestory'),
    path("stenadi/", StenadiView.as_view(), name='stenadi'),
    path("bname/", BnameView.as_view(), name='bname'),
    path("sonat/", SonatView.as_view(), name='sonat'),
    path("tarikh/", TarikhView.as_view(), name='tarikh'),
    path("episodelist/", EpiListView.as_view(), name='episodelist'),
    # path("episodegrid/", EpiGridView.as_view(), name='episode-grid'),
    # path("episodesingle/<int:id>/", EpiSingleView.as_view(), name='episode-single'),

    path('Like/<str:modelname>/<int:object_id>/', LikeToglleView.as_view(), name='like_Toggle'),
    path("delcast/", DelCastView.as_view(), name="delcast"),
    path('podcast/download/<slug:slug>/', PodcastDownloadView.as_view(), name='download_podcast'),

 
]