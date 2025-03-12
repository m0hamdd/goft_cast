from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.views.generic import ListView  
from django.utils.timezone import now
from django.urls import reverse
from django.views import View
from unicodedata import category
from django.contrib.auth.mixins import LoginRequiredMixin
from memory.forms import MemoryForm,DelCastForm
from django.contrib import messages
from .models import Memory, Podcast,Like,DelCast
from django.contrib.contenttypes.models import ContentType
from .models import Podcast, PodcastDownload

 
 
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
        messages.info(request,"با موفقیت ارسال شد." , 'error' )
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
class StenadiView(ListView):  
    model = Memory  
    template_name = 'memory/stenadi.html'  # نام تمپلیت  
    context_object_name = 'memories'  # نام متغیر در تمپلیت  

    def get_queryset(self):  
        return Memory.objects.all()  # می‌توانید اینجا فیلترهای خاصی اضافه کنید 


# Episode-Single View.
# class EpiSingleView(View):  
#     def get(self, request, id):  
#         episodes = get_object_or_404(Podcast, id=id)  # پیدا کردن پادکست با ID مشخص  
#         return render(request, 'home/podcast_detail.html', {'episodes': episodes})


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
 

class DelCastView(LoginRequiredMixin, View):  
    form_class = DelCastForm  

    def get(self, request):  
        form = self.form_class()  # استفاده از form_class به جای DelCastForm  
        return render(request, 'memory/del-cast.html', {'form': form})  # فرستادن فرم به تمپلیت  

    def post(self, request):  
        form = self.form_class(request.POST, request.FILES)  # دریافت فایل‌ها برای بارگذاری  
        if form.is_valid():  
            cd = form.cleaned_data  
            DelCast.objects.create(  
                title=cd['title'],  
                Occasion=cd['Occasion'],  
                Recipients_name_surname=cd['Recipients_name_surname'],  
                caption=cd['caption'],  
                time=cd['time'],  
                image=cd.get('image'),
                audio_file=cd.get('audio_file'),  
            )  
            messages.success(request, 'دل کست شما ایجاد شد.', 'successful')  
            return render(request, "memory/delcast_complete.html")  # هدایت به صفحه تکمیل  
        # اگر فرم معتبر نبود، دوباره فرم را با ارور نشان می‌دهیم  
        return render(request, 'memory/del-cast.html', {'form': form})  


class PodcastDownloadView(LoginRequiredMixin, View):
    redirect_field_name = 'next'  # هدایت به صفحه دانلود بعد از لاگین

    def get(self, request, slug):
        podcast = get_object_or_404(Podcast, slug=slug)

        # ثبت اطلاعات دانلود در دیتابیس
        PodcastDownload.objects.create(
            podcast=podcast,
            user=request.user,
            downloaded_at=now(),
            ip_address=self.get_client_ip(request)
        )

        # نمایش پیام موفقیت‌آمیز به کاربر
        messages.success(request, f'پادکست "{podcast.title}" با موفقیت دانلود شد!')

        # ارسال فایل صوتی برای دانلود
        response = FileResponse(podcast.audio_file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{podcast.audio_file.name}"'
        return response

    def get_client_ip(self, request):
        """ دریافت آدرس IP کاربر """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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