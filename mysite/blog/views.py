from blog.forms import PostSearchForm
from blog.models import Post
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView
from django.views.generic.edit import FormView
from tagging.models import Tag, TaggedItem
from tagging.views import TaggedObjectList


class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostDV(DetailView):
    model = Post


class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'


class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_date'
    make_object_list = True


class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_date'


class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_date'


class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_date'


class TagTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'


class PostTOL(TaggedObjectList):
    model = Post
    template_name = 'tagging/tagging_post_list.html'


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        schWord = '{}'.format(self.request.POST['search_word'])
        post_list = Post.objects.filter(
            Q(title__icontains=schWord) |
            Q(content__icontains=schWord) |
            Q(description__icontains=schWord)
        ).distinct()

        context = dict()
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)