from django.urls import path 
from .views import *

app_name = 'home'

urlpatterns = [
    path("" , IndexView.as_view() , name='index'),
    path('like/<int:pk>/', IndexView.as_view(), name='like_content'),  # مسیر لایک  
    path('download/<int:pk>/', IndexView.as_view(), name='download_content'),
    path("podcast/<int:id>/", PodcastDetailView.as_view(), name='podcast_detail'),
    path("memory/<int:id>/", EpisodeDetailView.as_view(), name='episode_detail'),
    path("podcastgrid/", PodcastGridView.as_view(), name='podcastgrid'),
    path("about/", AboutView.as_view(), name='about'),
    path("contact/", ContactView.as_view(), name='contact'),
    path("team/", TeamView.as_view(), name='team'),
    path("gallery/", GalleryView.as_view(), name='gallery'),
    path("faq/", FaqView.as_view(), name='faq'),
    path("sponsor/", SponsorView.as_view(), name='sponsor'),
    path("host/", HostView.as_view(), name='host'),
    path("hostsingle/", HostSingleView.as_view(), name='host-single'),
]