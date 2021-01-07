from django.views import generic
from .models import Post

class PostList(generic.ListView):
    queryset = Post.objects.order_by('-date_created')[:15]
    template_name = 'announcements.html'

