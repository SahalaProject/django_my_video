from django.contrib import admin
from myapp.models import Video, Photo, Path


# Register your models here.


class PathAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'type', 'status', 'create_time')


admin.site.register(Path, PathAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_name', 'video_path', 'create_time')


admin.site.register(Video, VideoAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_name', 'image_path', 'video', 'create_time')


admin.site.register(Photo, PhotoAdmin)
