from django.shortcuts import render
from django.views import View

# Blog View.
class BlogView(View):
    def get(self, request):
        return render(request, 'blog/blog.html')
    
    def post(self, request):
        return render(request, 'blog/blog.html')
