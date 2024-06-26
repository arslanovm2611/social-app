from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm, ProfileForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer
from notification.utils import create_notification
from post.serializers import PostSerializer
from post.models import Post

@api_view(['GET'])
def me(request): 
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email
    })



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'


    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save();
        
    
        # Send verification email later!
    else: 
        message = form.errors

    return JsonResponse({'message': message, 'requset': request.data,})


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data
        
    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests,
        'posts': PostSerializer(Post.objects.filter(created_by__in=friends), many=True).data
    }, safe=False)

@api_view(["POST"])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email is already exist'})
    
    else:
        print(request.FILES)
        print(request.POST)

        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        return JsonResponse({'message': 'changes updated'})


@api_view(['GET'])
def my_friendship_request(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)

    return JsonResponse(serializer.data, safe=False)    
    
@api_view(['POST'])
def editpassword(request):
    user = request.user

    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors}, safe=False)
 
    
@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    # print(request)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)


    if not check1 or not check2:
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)


        return JsonResponse({'message': 'request sent'})
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(["POST"])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()
    
    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

    return JsonResponse({'data': 'data'})