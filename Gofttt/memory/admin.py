from django.contrib import admin
from .models import *
 
 
 # پنل مدیریت برای VoiceActor
@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
 
 # پنل مدیریت برای Podcast
@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'actor', 'category', 'created']
    list_filter = ['category', 'actor']
    search_fields = ['title', 'actor__name']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created']
 
 # پنل مدیریت برای Memory
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'created']
    list_filter = ['category', 'user']
    search_fields = ['title', 'user__username']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created']
 
 # پنل مدیریت برای Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created']
    search_fields = ['user__username']
    list_filter = ['content_type', 'created']
    ordering = ['-created']
 
 # پنل مدیریت برای Like
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created']
    search_fields = ['user__username']
    list_filter = ['content_type', 'created']
    ordering = ['-created']
 
 # پنل مدیریت برای Report
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'memory', 'reason', 'is_cheked', 'created']
    list_filter = ['is_cheked', 'created']
    search_fields = ['user__username', 'memory__title']
    ordering = ['-created']
    actions = ['mark_as_checked']

    # اکشن برای علامت‌گذاری گزارش‌ها به عنوان بررسی‌شده
    @admin.action(description="علامت‌گذاری گزارش‌های انتخاب شده به عنوان بررسی‌شده")
    def mark_as_checked(self, request, queryset):
        queryset.update(is_cheked=True)

@admin.register(DelCast)
class DelCastAdmin(admin.ModelAdmin):
    list_display = ('title', 'Occasion', 'Recipients_name_surname', 'time')  # نمایش در لیست
    search_fields = ('title', 'Recipients_name_surname')  # امکان جستجو بر اساس عنوان و نام گیرنده
    list_filter = ('Occasion', 'time')  # فیلتر بر اساس مناسبت و مدت زمان


@admin.register(PodcastDownload)
class PodcastDownloadAdmin(admin.ModelAdmin):
    list_display = ('podcast', 'user', 'downloaded_at', 'ip_address')  # نمایش در لیست
    search_fields = ('podcast_title', 'user_username', 'ip_address')  # امکان جستجو
    list_filter = ('downloaded_at',)  # فیلتر بر اساس زمان دانلود