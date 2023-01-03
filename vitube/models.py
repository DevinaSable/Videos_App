from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.contrib.auth.models import AbstractUser


User = settings.AUTH_USER_MODEL


class VideoQuerySet(models.QuerySet):

    def search(self, query, user = None):
        lookup = (Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(tags__icontains=query))
        qs =  self.filter(lookup)
        if user is not None:
            qs2 = self.filter(user = user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class VideoManager(models.Manager):
    def get_queryset(self, *agrs, **kwargs):
        return VideoQuerySet(self.model, using=self.db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

#
# class User(AbstractUser):
#     liked_video = models.ManyToManyField('Video', through='Like')
#     pass


class Video(models.Model):
    BOLLYWOOD = 'BW'
    CARTOONS = 'CT'
    SONG = 'SG'
    LYRICAL = 'LC'
    MUSIC = 'MC'
    INTERVIEW = 'IN'
    EDUCATIONAL = 'ED'
    INSPIRATIONAL = 'IP'
    categories = [
        (BOLLYWOOD, 'Bollywood'),
        (CARTOONS, 'Cartoons'),
        (SONG, 'Song'),
        (LYRICAL, 'Lyrical'),
        (MUSIC, 'Music'),
        (INTERVIEW, 'Interview'),
        (EDUCATIONAL, 'Educational'),
        (INSPIRATIONAL, 'Inspirational')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank=True)
    video = models.FileField("Upload your video",
                             blank=False,
                             null=False,
                             validators=[FileExtensionValidator(allowed_extensions=["mp4", "mov", "wmv"])])
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=categories, default='Song')
    tags = models.CharField(max_length=400, null=True, blank=True, help_text='Use commas to separate text')
    upload_date = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    likes_count = models.IntegerField(default=0)
    #liked_by = models.ManyToManyField('User', through= 'Like')

    objects = VideoManager()


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'My Video'
        verbose_name_plural = 'My Videos'


    def get_absolute_url(self, *args, **kwargs):
        return f"api/videos/{self.user}/{self.pk}/"

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})
    #

class Like(models.Model):
    user = models.ForeignKey(User, related_name='Like', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='Like', on_delete=models.CASCADE)

