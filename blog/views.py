from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from blog.models import Blog, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras

# Create your views here.
def bloghome(request): 
    allPosts= Blog.objects.all()
    context={'allPosts': allPosts}
    return render(request, "blog/bloghome.html", context)

def blogPost(request, slug): 
    post=Blog.objects.filter(slug=slug).first()
    post.views= post.views +1
    post.save()
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno=request.POST.get('postSno')
        post = Blog.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return render(request, f"blog/{post.slug}")
        
