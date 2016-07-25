from django.contrib import admin
from photo.models import Album, Photo


# inline 방식은 1:N 관계로 연결된 객체를 함께 보여주는 방식 (총 2가지)
# StackedInline : 세로로 나열되어 보여주는 형식
# Tabularinline : 테이블 형태로 보여주는 형식
class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2                                   # 이미 입력된 객체 외 추가로 입력할 수 있는 객체 수


class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]                     # 객체를 보여줄 때, 미리 정의한 클래스로 보여줌
    list_display = ('name', 'description', )


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
