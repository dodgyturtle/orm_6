from django.shortcuts import get_object_or_404, render

from blog.models import Comment, Post, Tag


def serialize_post(post):
    return {
        "title": post.title,
        "teaser_text": post.text[:200],
        "author": post.author.username,
        "comments_amount": post.number_comments,
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": [serialize_tag(tag) for tag in post.tags.all()],
        "first_tag_title": post.tags.all()[0].title,
    }


def serialize_tag(tag):
    return {
        "title": tag.title,
        "posts_with_tag": tag.number_tags,
    }


def serialize_comments(comment):
    return {
        "text": comment.text,
        "published_at": comment.published_at,
        "author": comment.author.username,
    }


def index(request):
    most_popular_posts = (
        Post.objects.popular()
        .select_related("author")
        .fetch_with_tags_count()[:5]
        .fetch_with_comments_count()
    )
    most_fresh_posts = (
        Post.objects.order_by("published_at")
        .select_related("author")
        .fetch_with_tags_count()[:5]
        .fetch_with_comments_count()
    )

    most_popular_tags = Tag.objects.popular().fetch_with_tags_count()[:5]

    context = {
        "most_popular_posts": [serialize_post(post) for post in most_popular_posts],
        "page_posts": [serialize_post(post) for post in most_fresh_posts],
        "popular_tags": [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, "index.html", context)


def post_detail(request, slug):
    post_queryset = (
        Post.objects.popular().select_related("author").fetch_with_tags_count()
    )
    post = get_object_or_404(post_queryset, slug=slug)

    related_comments = post.comments.select_related("author").all()

    comments = [serialize_comments(comment) for comment in related_comments]

    related_tags = post.tags.all()

    serialized_post = {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments": comments,
        "likes_amount": post.number_likes,
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_tags = Tag.objects.popular().fetch_with_tags_count()[:5]

    most_popular_posts = (
        Post.objects.popular()
        .select_related("author")
        .fetch_with_tags_count()[:5]
        .fetch_with_comments_count()
    )

    context = {
        "post": serialized_post,
        "popular_tags": [serialize_tag(tag) for tag in most_popular_tags],
        "most_popular_posts": [serialize_post(post) for post in most_popular_posts],
    }
    return render(request, "post-details.html", context)


def tag_filter(request, tag_title):
    tag_queryset = Tag.objects
    tag = get_object_or_404(tag_queryset, title=tag_title)

    most_popular_tags = Tag.objects.popular().fetch_with_tags_count()[:5]

    most_popular_posts = (
        Post.objects.popular()
        .select_related("author")
        .fetch_with_tags_count()[:5]
        .fetch_with_comments_count()
    )

    related_posts = (
        tag.posts.all()
        .select_related("author")
        .fetch_with_tags_count()
        .fetch_with_comments_count()[:20]
    )

    context = {
        "tag": tag.title,
        "popular_tags": [serialize_tag(tag) for tag in most_popular_tags],
        "posts": [serialize_post(post) for post in related_posts],
        "most_popular_posts": [serialize_post(post) for post in most_popular_posts],
    }
    return render(request, "posts-list.html", context)


def contacts(request):
    # ?????????? ?????????? ?????????? ?????? ?????? ???????????????????? ?????????????? ???? ?????? ????????????????
    # ?? ?????? ???????????? ??????????????
    return render(request, "contacts.html", {})
