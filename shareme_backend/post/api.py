from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend
from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer, TrendsSerializer

@api_view(["GET"])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    
    trend = request.GET.get('trend', '') 

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)
    
    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)

    return JsonResponse({'post': PostDetailSerializer(post).data})

@api_view(["GET"])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)    
    posts = Post.objects.filter(created_by_id=id)
   

    if request.user.id == user.id:
        posts = posts.filter(created_by_id=id)
    elif request.user not in user.friends.all():
        posts = posts.filter(is_private=False)
    



    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)


    if  check1 or  check2:
        can_send_friendship_request = False

    
    return JsonResponse({
        'posts' : posts_serializer.data,
        'user': user_serializer.data, 
        'can_send_friendship_request': can_send_friendship_request,   
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    user = User.objects.get(pk=request.user.id)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()


    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        user.posts_count = user.posts_count + 1
        user.save()
        post.save()
        
        if attachment:
            post.attachments.add(attachment)

        serializer = PostSerializer(post)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({ 'error' :'add something later!...'})
    

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    found_like = post.likes.filter(created_by=request.user).first()  # Check for existing like

    if found_like:
        # Unlike the post
        found_like.delete()
        post.likes_count -= 1
        post.save()
       
        notification = create_notification(request, 'post_unlike', post_id=post.id)
        return JsonResponse({'like': 'unliked'})
    else:
        # Like the post
        like = Like.objects.create(created_by=request.user)
        post.likes_count += 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, 'post_like', post_id=post.id)
        return JsonResponse({'like': 'liked'})

@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, 'post_comment', post_id=post.id)


    serializer = CommentSerializer(comment)
 
    return JsonResponse(serializer.data, safe=False)

@api_view(["DELETE"])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    user = User.objects.get(pk=request.user.id)
    user.posts_count = user.posts_count - 1
    user.save()
    post.delete()

    return JsonResponse({'message': 'post deleted'})

@api_view(["POST"])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()

    return JsonResponse({'message': 'post reported'})


@api_view(["GET"])
def get_trends(request):
    serializer = TrendsSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)
