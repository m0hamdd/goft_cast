from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.views.generic import ListView  
from django.utils.timezone import now

from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from memory.forms import MemoryForm,DelCastForm
from django.contrib import messages
from .models import *
from django.contrib.contenttypes.models import ContentType
from .models import Podcast, PodcastDownload

 
 
 # Memory View.
class MemoriesView(LoginRequiredMixin, View):
    form_class = MemoryForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'memory/makestory.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            # بررسی خالی بودن فیلدها
            if not cd.get('title') or not cd.get('category') or not cd.get('body'):
                messages.error(request, 'فیلدهای ضروری نباید خالی باشند', 'danger')
                return render(request, 'memory/makestory.html', {'form': form})

            # ذخیره‌ی فرم
            memory = form.save(commit=False)
            memory.user = request.user  # در صورتی که مدل دارای فیلد user است
            memory.save()
            messages.success(request, 'خاطره با موفقیت ذخیره شد!', 'success')

            # بعد از ثبت، رندر گرفتن صفحه‌ی story_complate.html
            return render(request, 'memory/story_complete.html', {'memory': memory})
        return render(request, 'memory/makestory.html', {'form': form})
class EpiListView(View):
    def get(self, request):
        return render(request, 'memory/episodelist.html')



# Stenadi View.
class StenadiView(ListView):  
    model = Memory  
    template_name = 'memory/stenadi.html'  # نام تمپلیت  
    context_object_name = 'memories'  # نام متغیر در تمپلیت  

    def get_queryset(self):  
        return Memory.objects.filter(category='documentary_memory')  # می‌توانید اینجا فیلترهای خاصی اضافه کنید


# Episode-Single View.
# class EpiSingleView(View):  
#     def get(self, request, id):  
#         episodes = get_object_or_404(Podcast, id=id)  # پیدا کردن پادکست با ID مشخص  
#         return render(request, 'home/podcast_detail.html', {'episodes': episodes})


# Bname View.
class BnameView(View):
    model = Memory
    template_name = 'memory/bname.html'
    context_object_name = 'memories'


    def get_queryset(self, request ):
        return Memory.objects.filter(category='unnamed_memory')

    
# Sonat View.
class SonatView(View):
    def get(self, request,):
        return render(request, 'memory/sonat.html')
    
# Tarikh View.
class TarikhView(View):
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