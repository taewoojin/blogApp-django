from bookmark.models import Bookmark
from django.shortcuts import render
from django.views.generic import DetailView, ListView


class BookmarkLV(ListView):
    model = Bookmark


class BookmarkDV(DetailView):
    model = Bookmark
