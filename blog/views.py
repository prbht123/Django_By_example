
# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from .forms import EmailPostForm, CommentForm

from django.core.mail import send_mail

from taggit.models import Tag
import operator
from django.db.models import Count

#def post_list(request):
 #   posts = Post.published.all()
  #  print(posts)
   # return render(request,'blog/post/list.html',{'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='draft',publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blog/post/detail.html',{'post': post})


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request,'blog/post/list_new.html',{'page': page,'posts': posts})



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'




def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
        # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,'form': form})




def post_share_template(request, post_id):
    # Retrieve post by id
    print(request.method)
    post = get_object_or_404(Post, id=post_id, status='draft')
    sent = False
    
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            url_p = str(post.publish.year)+'/'+str(post.publish.month)+'/'+str(post.publish.day)+'/'+post.slug
            post_url = request.build_absolute_uri(post.get_absolute_url)
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, settings.EMAIL_HOST_USER,[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,'form': form,'sent': sent})





def post_detail_template(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='draft',publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blog/post/detail1.html',{'post': post})





def post_detail_comment(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='draft',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            print("99999999999999")
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,'blog/post/blog_detail.html',{'post': post,'comments': comments,'comment_form': comment_form})


#--------------------------

def post_list_tag(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list_tags.html',{'page': page,'posts': posts})



def post_list_tag_slug(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    print("00000")
    print(tag_slug)
    if tag_slug:
        print("66666666")
        tag = get_object_or_404(Tag, slug=tag_slug)
        print(tag)
        object_list = object_list.filter(tags__in=[tag])
        print(object_list)
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    print(tag)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
   # return render(request,'blog/post/listtagslug.html',{'page': page,'posts': posts,'tag': tag})
    return render(request,'blog/post/list_new.html',{'page': page,'posts': posts,'tag': tag})





def post_retrived(request,pk):
    print("0000000000000000")
    object_list = Post.published.get(id=pk)
    print(object_list)
    post_tags_name = object_list.tags.all().order_by('taggit_taggeditem_items')
    
    post_tags_ids = object_list.tags.values_list('id', flat=True)
    print(post_tags_ids)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=object_list.id)
    print(similar_posts)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    print(similar_posts)
    return render(request,'blog/post/detail_tag_filter.html',{'post': object_list,'post_tags_name':post_tags_name,'similar_posts': similar_posts})

