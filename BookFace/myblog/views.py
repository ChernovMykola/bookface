from django.shortcuts import (
    render, 
    get_object_or_404, 
    redirect
)
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError
from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView, 
    CreateView, 
    UpdateView, 
    DetailView
)
from myblog.models import (
    Post, 
    Comment, 
    UserProfileInfo, 
    User
)
from django.contrib.auth.mixins import LoginRequiredMixin
from myblog.forms import (
    PostForm, 
    CommentForm, 
    UserForm
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate, 
    login
)
from django.http import (
    HttpResponseRedirect, 
    HttpResponse
)
from django.contrib.auth.models import User
from django.db.utils import IntegrityError






from django.urls import reverse_lazy




class AboutView(TemplateView):
    template_name = 'about.html'

class PostDraftList(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'post'
    template_name = 'myblog/post_draft_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(author=self.request.user, published_date__isnull=True).order_by('create_date')
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

# def wall(request):
#     if request.user.is_authenticated:
#         posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#         context = {'posts': posts}
#         return render(request, 'myblog/wall.html', context)
#     else:
#         return render(request, 'myblog/login.html')


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
    





def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

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


@login_required
def deletepost(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:
            post.delete()
        else:
            return redirect('accounts/login')
        return redirect('myblog:post_list')
    else:
        return redirect('accounts/login')

    
    
    


# class DraftListView(LoginRequiredMixin, ListView):
#     login_url = '/login/'
#     redirect_field_name = 'myblog/post/list.html'
#     model = Post


    

    
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('myblog:post_detail', pk=pk )

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Change commit argument to True
            comment.post = post
            comment.author = request.user
            comment.save()
            previous_page_url = request.session.get('previous_page_url', '/')
            return redirect(previous_page_url)
    else:
        form = CommentForm() 
    request.session['previous_page_url'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'myblog/comment_form.html',{'form':form})
    
# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('post_detail', pk=comment.post.pk)

# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     post_pk = comment.post.pk
#     comment.delete()
#     return redirect('post_detail', pk=post_pk)


def registration(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST,  files=request.FILES)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            confirm_password = user_form.cleaned_data.get('confirm_password')
            email_exists = User.objects.filter(email=email).exists()
            if password != confirm_password:
                user_form.add_error('username', f'Check your password please!')
            elif email_exists:
                user_form.add_error('email', f'This email is already registered.')
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.set_password(password)  # Hash the password for UserProfileInfo
                    user.save()
                    registered = True
                except IntegrityError as e:
                    user_form.add_error('username', f'Username {username} already exists. Please choose another username.')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'myblog/registration.html', {'user_form': user_form, 'registered': registered})





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
            return render(request, 'myblog/user_login.html',{})
            
        # HttpResponse("Invalid login details! supplied!")
    else:
        return render(request, 'myblog/user_login.html',{})