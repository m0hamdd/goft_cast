from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from unicodedata import category
from django.contrib.auth.mixins import LoginRequiredMixin
from memory.forms import MemoryForm,DelCastForm
from django.contrib import messages
from .models import Memory, Podcast,Like,DelCast
from django.contrib.contenttypes.models import ContentType


# Memory View.
class MemoriesView(LoginRequiredMixin,View):
    form_class = MemoryForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'memory/makestory.html',{'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            memory = Memory.objects.create(title=cd['title'], body = cd['body'],category=cd['category'],user = request.user)
            if not cd.get('title') or not cd.get('category') or not cd.get('body'):
                messages.error(request, 'فیلد های ضروری نباید خالی باشد ' , 'danger')
                return render(request, 'memory/makestory.html')
            memory.save()
            if memory.category == 'unnamed_memory':
                return redirect(reverse('BnameView'))
            elif memory.category == 'documentary_memory':
                return redirect(reverse('StenadiView'))
            elif  memory.category == 'OralTradition':
                return redirect(reverse(' SonatView'))
            elif memory.category == 'oral_memory':
                return redirect(reverse('TarikhView'))
            else:
                return redirect('memory/makestory.html', {'form': form})
        messages.info(request,"لطفا از به درستی شدن فید ها اطمینان حاصل کنید " , 'error' )
        return render(request, 'memory/makestory.html' ,{'form':form })

class EpiListView(View):
    def get(self, request):
        return render(request, 'memory/episodelist.html')

class ListCategory(View):
    template_name = ''
    def get(self, request):
        memories = Memory.objects.filter(category = self.category)
        return render(request, self.template_name, {'memories':memories})

# Stenadi View.
class StenadiView(ListCategory):
    def get(self, request):
        return render(request, 'memory/stenadi.html')

    
# Bname View.
class BnameView(ListCategory):
    def get(self, request ):
        return render(request, 'memory/bname.html')

    
# Sonat View.
class SonatView(ListCategory):
    def get(self, request,):
        return render(request, 'memory/sonat.html')
    
# Tarikh View.
class TarikhView(ListCategory):
    def get(self, request):
        return render(request, 'memory/tarikh.html')

# EpisodeList View.


# Episode-Grid View.
class EpiGridView(View):
    def get(self, request):
        podcasts  = Podcast.objects.all().order_by('created')
        return render(request, 'memory/episode-grid.html', {'podcasts ': podcasts})
    
# Episode-Single View.
class EpiSingleView(View):
    def get(self, request):
        return render(request, 'memory/episode-single.html')
    
    def post(self, request):
        return render(request, 'memory/episode-single.html')


# DelCast View.
class DelCastView(View):
    class_form=DelCastForm
    def get(self, request):
        form = self.DelCastForm()
        return render(request, 'memory/del-cast.html')
    
    def post(self, request):
        form = self.DelCastForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            DelCast_created= DelCast.objects.create(title=cd['title'],Occasion=cd['Occasion'],Recipients_name_surname=cd['Recipients_name_surname'],caption=cd['caption'],time=['time'])
            messages.success(request,'دل کست شما ایحاد شد ', 'successful')
            form.save()
            return render(request, 'memory/delcast_complate')
        return render(request, 'memory/del-cast.html')


class LikeToglleView(LoginRequiredMixin,View):
    def post(self, request, modelName,object_id):
        model_class= Podcast if modelName == 'podcast' else Memory
        content_type = ContentType.objects.get_for_model(model_class)
        content_object= get_object_or_404(model_class,id = object_id)
        like,created= Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
        )

        if not created:
            like.delete()
        next_url = request.POST.get('next')or request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)