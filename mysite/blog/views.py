from blog.forms import PostSearchForm
from blog.models import Post
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from mysite.views import LoginRequiredMixin
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


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    initial = {'slug': 'auto-pilling-do-not-input', }       # 입력란의 초기문구
    # fields = ['title', 'description', 'content', 'tag']   # save method에서 slug 미입력시 auto로 설정되게 했으므로 제외 가능
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return super(PostChangeLV, self).get_queryset().filter(owner=self.request.user)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('blog:index')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
