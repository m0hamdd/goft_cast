from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models import User
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField


#add voice actor
class VoiceActor(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)


#creat podcast
class Podcast(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255 , unique=True )
    image = models.ImageField(upload_to='templates/memory/podcast_image/')
    # یک دایرکتوری برای ذخیره عکس در نظر گرفته شود
    caption = RichTextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='templates/memory/voice_podcast',validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])])
    # یک دایرکتوری برای ذخیره صداها در نظر گرفته شود
    actor= models.ForeignKey(VoiceActor, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
 
    def str(self):
        return f"{self.title}of {self.actor} in {self.category}"

#creating memories by all user and groups
class Memory(models.Model):
 
    CATEGORY_CHOICES = [
        ('unnamed_memory', 'خاطرات بی نام'),
        ('documentary_memory', 'خاطرات استنادی'),
        ('OralTradition', 'خاطرات سنت شفاهی'),
        ('oral_memory', 'خاطرات شفاهی'),
    ]
 
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255,choices=CATEGORY_CHOICES,default='unnamed_memory')
    slug = models.SlugField(max_length=255, unique=True)
    body = RichTextField(blank=True, null=True)
    image = models.ImageField(
        upload_to= 'templates/memory/Memory_image/',
        blank=True,
        null=True ,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
 
    audio_file = models.FileField(upload_to='templates/memory/voice_memory/'  ,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
 
    def str(self):
        return f"memories of {self.user.username} --- {self.title} ---"
 
    class Meta:
        ordering = ['-created']

#the like & cm class will support any modle
class Comment(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object= GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
 
    def str(self):
        return f"{self.user.username}--- comment of {self.content_type}---{self.object_id} "
 
    class Meta:
        ordering = ('created',)

class Like(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object= GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
 
    def str(self):
        return f"{self.user.username}--- like of {self.content_object}"

#report class will only support the Memory model
class Report(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memory = models.ForeignKey('Memory', on_delete=models.CASCADE,related_name='reports')
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_cheked = models.BooleanField(default=False)
 
    class Meta:
        unique_together = ('user', 'memory')
 
    def str(self):
        return f"{self.user.username}--- report of {self.memory.title}"



class DelCast(models.Model):
    title = models.CharField(max_length=255)
    CATEGORY_CHOICES1 = [
        ('WOMEN_DAY','روز زن'),
        ('MOTHERS_DAY', 'روز مادر'),
        ('STUDENT_DAY','روز دانش اموز'),
        ('LABOR_DAY','روز کارگر'),
        ('CUSTOM','سفارشی'),
    ]
    Occasion = models.CharField(max_length=255,choices=CATEGORY_CHOICES1,default='WOMEN_DAY')
    Recipients_name_surname = models.CharField(max_length=300)
    caption = RichTextField(blank=True, null=True)
    CATEGORY_CHOICES2=[
        ('2min','2دقیقه'),
        ('5min', '5دقیقه'),
        ('10min', '10دقیقه'),
        ('15min', '15دقیقه'),
    ]
    time = models.CharField(max_length=255,choices=CATEGORY_CHOICES2,default='2min' )
    image = models.ImageField(
        upload_to='templates/memory/delcast/',
        blank=True,
        null =True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
