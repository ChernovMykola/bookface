from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (TemplateView, ListView, DeleteView, CreateView, UpdateView, DetailView)
from myblog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from myblog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required



from django.urls import reverse_lazy
# Create your views here.



class AboutView(TemplateView):
    template_name = 'about.html'


def get_queryset(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user, published_date__isnull = True).order_by('create_date')
        return render(request, 'myblog/post_list.html', {'posts': posts})
    else:
        return redirect('accounts/login')


def list_post(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user, published_date__isnull = False)
        return render(request, 'myblog/post_list.html', {'posts': posts})
    else:
        return redirect('accounts/login')





    # def get_queryset(self,):
    #     return Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date'), 


class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'myblog/post_detail.html'
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
        return redirect('post_list')
    else:
        return redirect('accounts/login')

    
    
    
# model = Post
# success_url = reverse_lazy('post_list')

# class DraftListView(LoginRequiredMixin, ListView):
#     login_url = '/login/'
#     redirect_field_name = 'myblog/post/list.html'
#     model = Post



    

    
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk )

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()
        return render(request,'myblog/comment_form.html',{'form':form}) 
    
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)