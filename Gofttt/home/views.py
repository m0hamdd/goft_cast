from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from accounts.models import User

from django.views.generic import ListView  
from django.db.models import Q    
from django.views import View  
from django.shortcuts import redirect, get_object_or_404  
from django.contrib import messages  
from django.contrib.contenttypes.models import ContentType  
from memory.models import Podcast, Memory, Like, PodcastDownload  


class BaseContentView(View):  
    # این متد برای لایک و دانلود استفاده می‌شود  
    def handle_like(self, request, pk, content_type):  
        if request.method == 'POST':  
            if content_type == 'podcast':  
                podcast = get_object_or_404(Podcast, pk=pk)  
                Like.objects.get_or_create(user=request.user, object_id=podcast.id,  
                                           content_type=ContentType.objects.get_for_model(Podcast))  
                messages.success(request, 'لایک شما با موفقیت ثبت شد!')  
            elif content_type == 'memory':  
                memory = get_object_or_404(Memory, pk=pk)  
                Like.objects.get_or_create(user=request.user, object_id=memory.id,  
                                           content_type=ContentType.objects.get_for_model(Memory))  
                messages.success(request, 'لایک شما با موفقیت ثبت شد!')  
    
    def handle_download(self, request, pk, content_type):  
        if request.method == 'POST':  
            if content_type == 'podcast':  
                podcast = get_object_or_404(Podcast, pk=pk)  
                PodcastDownload.objects.create(podcast=podcast, user=request.user)  
                messages.success(request, 'دانلود شما با موفقیت ثبت شد!')  
            elif content_type == 'memory':  
                memory = get_object_or_404(Memory, pk=pk)  
                # منطق دانلود برای memory  
                messages.success(request, 'دانلود شما با موفقیت ثبت شد!')  

class IndexView(BaseContentView):  
    template_name = 'home/index.html'  
    
    def get(self, request, *args, **kwargs):  
        query = request.GET.get('q', '')  
        podcasts = Podcast.objects.all()  
        memories = Memory.objects.all()  
        
        if query:  
            podcasts = podcasts.filter(title__icontains=query)  
            memories = memories.filter(title__icontains=query)  

        context = {  
            'podcasts': podcasts,  
            'memories': memories,  
            'query': query,  
        }  
        return render(request, self.template_name, context)  

    def post(self, request, *args, **kwargs):  
        content_type = request.POST.get('content_type')  
        pk = request.POST.get('pk')  
        
        # مدیریت لایک یا دانلود  
        if request.POST.get('action') == 'like':  
            self.handle_like(request, pk, content_type)  
        elif request.POST.get('action') == 'download':  
            self.handle_download(request, pk, content_type)  

        return redirect('home:index')  


# Episode-Grid View.
class PodcastGridView(ListView):
    mode = Podcast
    template_name = 'home/podcastgrid.html' 
    context_object_name = 'podcasts'

    def get_queryset(self):
        return Podcast.objects.all()
        

class PodcastDetailView(View):  
    def get(self, request, id):  
        podcast = get_object_or_404(Podcast, id=id)  # پیدا کردن پادکست با ID مشخص  
        return render(request, 'home/podcast_detail.html', {'podcast': podcast})


class EpisodeDetailView(View):  
    def get(self, request, id):  
        memories = get_object_or_404(Memory, id=id)  # پیدا کردن پادکست با ID مشخص  
        return render(request, 'home/episode_detail.html', {'memories': memories})
    

# About Us View
class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html')
    
    def post(self, request):
        return render(request, 'home/about.html')


# Contact Us View
class ContactView(View):
    def get(self, request):
        return render(request, 'home/contact.html')
    
    def post(self, request):
        return render(request, 'home/contact.html')


# Team View.
class TeamView(View):
    def get(self, request):
        return render(request, 'home/team.html')
    
    def post(self, request):
        return render(request, 'home/team.html')


# Gallery View.
class GalleryView(View):
    def get(self, request):
        return render(request, 'home/gallery.html')
    
    def post(self, request):
        return render(request, 'home/gallery.html')
    
# Faq View.
class FaqView(View):
    def get(self, request):
        return render(request, 'home/faq.html')
    
    def post(self, request):
        return render(request, 'home/faq.html')
    
# Sponsor View.
class SponsorView(View):
    def get(self, request):
        return render(request, 'home/sponsor.html')
    
    def post(self, request):
        return render(request, 'home/sponsor.html')

# Host View.
class HostView(View):
    def get(self, request):
        return render(request, 'home/host.html')
    
    def post(self, request):
        return render(request, 'home/host.html')

# Host-Single View.
class HostSingleView(View):
    def get(self, request):
        return render(request, 'home/host-single.html')
    
    def post(self, request):
        return render(request, 'home/host-single.html')
