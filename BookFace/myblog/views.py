from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.utils import IntegrityError
from django.http import (
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import (
    get_object_or_404, 
    redirect, 
    render
)
from django.urls import (
    reverse, 
    reverse_lazy
)
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from myblog.forms import (
    CommentForm,
    PostForm, 
    UserForm
)
from myblog.models import (
    Comment, 
    Post, 
    User, 
    UserProfileInfo
)


class AboutView(TemplateView):
    template_name = 'about.html'


class PostDraftList(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'post'
    template_name = 'myblog/post_draft_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(
                author=self.request.user, published_date__isnull=True
            ).order_by('create_date')
            return posts
        else:
            posts = Post.objects.none()
            return posts


class AllPost(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'post'
    template_name = 'myblog/post_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(author=self.request.user)
        else:
            posts = Post.objects.none()
        return posts


class Wall(ListView):
    model = Post
    template_name = 'myblog/wall.html'
    context_object_name = 'post'
    paginate_by = 5

    def get_queryset(self):
        post = Post.objects.all()
        if not self.request.user.is_authenticated:
            return redirect('accounts/login')
        return post


class PostDetail(DetailView):
    model = Post
    template_name = 'myblog/post_detail.html'
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'myblog/post_detail'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        picture = form.cleaned_data['picture']
        if picture:
            form.instance.picture = picture
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'myblog/post_detail.html'
    model = Post
    form_class = PostForm


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('myblog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('myblog:post_detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'myblog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        previous_page_url = self.request.session.get('previous_page_url', '/')
        return redirect(previous_page_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_page_url'] = self.request.META.get('HTTP_REFERER', '/')
        return context


def registration(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            confirm_password = user_form.cleaned_data.get('confirm_password')
            email_exists = User.objects.filter(email=email).exists()
            if password != confirm_password:
                user_form.add_error('username', f'Check your password please!')
            elif email_exists:
                user_form.add_error(
                    'email', f'This email is already registered.'
                )
            else:
                try:
                    user = User.objects.create_user(
                        username=username, email=email, password=password
                    )
                    user.set_password(
                        password
                    )  # Hash the password for UserProfileInfo
                    user.save()
                    registered = True
                except IntegrityError as e:
                    user_form.add_error(
                        'username',
                        f'Username {username} already exists. Please choose another username.',
                    )
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(
        request,
        'myblog/registration.html',
        {'user_form': user_form, 'registered': registered},
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myblog:post_list'))

            else:
                return HttpResponse("ACCOUNT IS NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password: {}".format(username, password))
            return render(request, 'myblog/user_login.html', {})
    else:
        return render(request, 'myblog/user_login.html', {})
