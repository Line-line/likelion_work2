from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Blog, Comment
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required # 이거 설정한 def는 로그인 꼭 해야함.

# Create your views here.

def home(request):
    blogs = Blog.objects    #admin에 써져있는 목록들
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page') # get방식으로 페이지 번호를 알아왔다.
    posts = paginator.get_page(page) # 그 페이지 번호가 뭔지 넣어버림
    return render(request, 'home.html', {'blogs' : blogs, 'posts':posts}) # key랑 value값 리턴

def detail(request, blog_id):
    details = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'detail' : details})
    # 우리가 앞에서 처음에 했을 때 blogobject로 받아온것들을 얻어올려고 하는것
    # 갖고오면 내용 보여주고 실패하면 404에러 띄워줌

def new(request):
    form = BlogForm()
    return render(request, 'new.html', {'form':form})

def create(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('/blog' + str(blog.id))
    else:
        form = BlogForm()
    return redirect(request, 'new.html', {'form' : form})

def edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('/blog' + str(blog.id))
    else:
        form = BlogForm(instance = blog)
    return render(request,'edit.html',{'form':form})

def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()       # 삭제 함수
    return redirect('/')    # 새로고침 그런느낌

@login_required   # 로그인 한채로만 접속 가능 
def comment_add(request, blog_id):
    if request.method == "POST":
        post = Blog.objects.get(pk = blog_id)

        comment = Comment()
        comment.user = request.user
        comment.body = request.POST['body']
        comment.post = post
        comment.save() 
        return redirect('/blog/' + str(blog_id))
    else:
        return HttpResponse('잘못된 접근입니다.')

@login_required   # 로그인 한채로만 접속 가능 
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)
    if request.user == comment.user:        # 접속한 유저가 댓글 작성자인지?
        if request.method == "POST":
            comment.body = request.POST['body']
            post_id = comment.post.id
            comment.save()
            return redirect('/blog/'  + str(post_id))

        elif request.method == "GET":
            context = {
                'comment' : comment
            }
            return render(request, 'comment_edit.html', context)

@login_required   # 로그인 한채로만 접속 가능 
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user:
        if request.method == "POST":
            post_id = comment.post.id
            comment.delete()
            return redirect('/blog/' + str(post_id))
    return HttpResponse('잘못된 접근입니다.')