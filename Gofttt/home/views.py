from django.shortcuts import render
from django.views import View


# Index View
class IndexView(View):
    def get(self, request):
        return render(request, 'home/index.html')
    
    def post(self, request):
        return render(request, 'home/index.html')


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
