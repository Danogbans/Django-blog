from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm, EmailPostForm, SearchForm 
from django.db.models import Count
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector




# post_list: Retrieves and displays all posts..
def post_list(request):
    posts = Post.objects.all()
    latest_posts = Post.objects.order_by('-created_at')[:4] # Retrieves the latest 5 posts to be displayed in the sidebar.
    paginator = Paginator(posts, 3) # Shows 3 posts per page

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_object': page_object, 'latest_posts': latest_posts})


# post_detail: Displays a single post and handles comment submission.
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    latest_posts = Post.objects.order_by('-created_at')[:4]
    post_tags_ids = post.tags.values_list('id', flat=True)  # Retrieve all tags for the current post
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id) # Get all posts that are tagged with any of those tags, excluding the current post
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created_at')  # Annotate the count of shared tags
    similar_posts = similar_posts[:2] # Limit the query to the number of posts you want to recommend
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts,  'latest_posts': latest_posts})


# post_share view: handles the form submission and email sending.
@login_required
def post_share(request, post_id):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you reading \"{post.title}\""
            message = f"Read \"{post.title}\" at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_email@example.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post_share.html', {'post': post, 'form': form, 'sent': sent, 'latest_posts': latest_posts})
                

# post_create: Handles the creation of new posts. Requires user login.
@login_required
def post_create(request):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save tags
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'latest_posts': latest_posts})


# post_edit: Allows editing of existing posts. Requires user login.
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


# This retrieves all the posts associated with a specific tag and passes them to a template for rendering.
def post_list_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    latest_posts = Post.objects.order_by('-created_at')[:4]
    posts = Post.objects.filter(tags__in=[tag])
    return render(request, 'blog/post_list_by_tag.html', {'tag': tag, 'posts': posts, 'latest_posts': latest_posts})


# post_confirm_delete: Handles deletion of posts. Requires user login.
@login_required
def post_confirm_delete(request, slug):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post, 'latest_posts': latest_posts})


#like_post: Toggles the like status of a post. Requires user login.
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', slug=slug)



# A view that will handle the search functionality.
def search(request):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'content')
            results = Post.objects.annotate(search=search_vector).filter(search=query)
    return render(request, 'blog/search_results.html', {'form': form, 'query': query, 'results': results, 'latest_posts': latest_posts})