from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator

@login_required(login_url="login")
def index(req):
    all_items = Blog.objects.all().order_by('-id')
    paginator = Paginator(all_items, 5)
    page_number = req.GET.get('page')
    all_blogs = paginator.get_page(page_number)
    
    context = {
        "all_blogs": all_blogs,
    }

    return render(req, 'pages/index.html', context)

@login_required(login_url="login")
def blog_details(req, pk):
    blog = get_object_or_404(Blog, id=pk)
    tags = Tag.objects.all()
    comments = Comment.objects.filter(blog=blog)
    is_in_user_blogs = False
    try:
        blog = get_object_or_404(Blog, id=pk, created_by=req.user)
        is_in_user_blogs = True
    except Http404:
        is_in_user_blogs = False
        
    return render(req, "pages/blog.html", context={
        "blog": blog,
        "tags": tags,
        "comments": comments,
        "is_in_user_blogs": is_in_user_blogs
    })

@login_required(login_url="login")
def cat_blog(req, slug):
    all_blogs = Blog.objects.all().order_by('-id')
    tag = Tag.objects.get(slug=slug)
    if tag:
        blogs = all_blogs.filter(tags__in=[tag])
        return render(req, "pages/cat_blog.html", {'all_blogs': blogs})

@login_required(login_url="login")
def create_comment(req, id):
    if req.method == "POST":
        text = req.POST['comment']
        comment = Comment.objects.create(
            text=text,
            user=req.user,
            blog=get_object_or_404(Blog, id=id)
        )
        comment.save()
    return redirect('blog_details', id)

@login_required(login_url="login")
def delete_comment(req):
    if req.method == "POST":
        comment_id = req.POST.get('comment')
        comment = Comment.objects.get(id=comment_id)
        blog = comment.blog.id
        comment.delete()
    return redirect("blog_details", blog)

@login_required(login_url="login")
def edit_blog(req, id=None):
    blog_data = {
        "id": id,
        "title": "",
        "img": "",
        "content": "",
        "tags": ""  
    }
    tagsname = ''
    if id:
        blog = get_object_or_404(Blog, id=id)
        blog_data["title"] = blog.title
        blog_data["content"] = blog.content
        blog_data["img"] = blog.blog_img

        for tag in blog.tags.all():
            tagsname += f"{tag.name}, "
        
        tagsname = tagsname.rstrip(', ')
        blog_data["tags"] = tagsname
    if req.method == "POST":
        title = req.POST.get('title')
        content = req.POST.get('content')
        img = req.FILES.get('img')
        tags = req.POST.get('tags')

        if id:
            blog.title = title
            blog.content = content
            if img:
                blog.blog_img = img
            blog.tags.set(tags.split(','))  # Ensure tags are split correctly and passed as a list
            blog.save()
        else:
            blog = Blog.objects.create(
                title=title,
                content=content,
                blog_img=img,
                created_by=req.user
            )
            blog.tags.set(tags.split(','))  # Ensure tags are split correctly and passed as a list
            blog.save()
        return redirect("blog_details", pk=blog.id)

    return render(req, "pages/edit.html", blog_data)

def delete_blog(req, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect("index")

def search(req):
    search_for = req.GET.get('search_for')
    all_blogs = Blog.objects.filter(title__icontains=search_for)
    return render(req, 'pages/index.html', {'all_blogs': all_blogs})