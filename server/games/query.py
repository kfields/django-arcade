from blogsley.django.graphql import query

from .models import Post
from .schema import PostConnection, PostEdge, PostNode

@query.field("allPosts")
def resolve_all_posts(root, info):
    # return Post.objects.all()
    posts = [p for p in Post.objects.all()]
    connection = PostConnection(posts)
    result = connection.wire()
    return result


@query.field("post")
def resolve_post(*_, id):
    return Post.objects.get(id=id)
