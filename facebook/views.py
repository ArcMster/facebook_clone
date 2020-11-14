from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Post, Liked, Comment, Messages
from rest_framework.response import Response
from rest_framework.views import APIView
#from rest_framework.decorators import api_view, renderer_classes
#from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import login

#@api_view(('GET',))
#@renderer_classes((TemplateHTMLRenderer, JSONRenderer))

# Create your views here.


def comment(request):
    comment = Comment()
    comment.comment = request.POST['value']
    print('comment val',request.POST['id'])
    post = Post.objects.get(id = request.POST['id'])
    comment.post = Post.objects.get(id = request.POST['id'])
    comment.postid = str(comment.post)
    comment.user = request.user
    comment.save()
    print('comment function invoked')
    
    return JsonResponse({'value': 'Comment has been added', 'user': str(comment.user)})

def signin(request):
    user = User.objects.all()
    
    usernames = []
    for i in user:
        usernames.append(i.username)
        
    
    if str(request.user) in usernames :
        return redirect('home')
    return render(request,'login.html')

def login(request):
    user_name = request.POST['userid']
    print("user name is: ",user_name)
    user_password = request.POST['password']
    user = auth.authenticate(username = user_name,password= user_password)
    if user is not None:
        
        auth.login(request,user)
        return redirect('home')
        

    return redirect('signin')

def logintest(request):
    user_name = request.POST['userid']
    print("user name is: ",user_name)
    user_password = request.POST['password']
    user = auth.authenticate(username = user_name,password= user_password)
    if user is not None:
        
        auth.login(request,user)
        #return redirect('home')
        return JsonResponse({'value': 'valid'})
    else: 
        return JsonResponse({'value': 'invalid'})

def post(request): 
    print('post function invoked')
    caption = request.POST['caption']
    image = request.FILES['image']
    print(image)
    new_post = Post()
    new_post.caption = caption
    new_post.image = image
    new_post.username = request.user
    new_post.save()
    return JsonResponse({'value': 'post has been added successfully'})

def logout(request):
    auth.logout(request)
    return redirect('signin')

def home(request):

    #auto complete section
    if 'term' in request.GET:
        qs = User.objects.filter(username__istartswith = request.GET['term'])
        users = []
        for i in qs:
            users.append(i.username)
        return JsonResponse(users, safe=False)
    
    all_post = Post.objects.all().order_by('id').reverse()

    paginator = Paginator(all_post,5)
    page = request.GET.get('page')
    all_post = paginator.get_page(page)
    for i in all_post:
        i.id = str(i.id)
    comment = Comment.objects.all()


    return render(request,'home.html',{'posts':all_post, 'comment': comment})

"""def btntest(APIView):
    print('button clicked')
    data = {
        'value': 'this is a test value'
    }

    return Response(data)"""



    
#class created for test purpose
class Btntest(APIView):
   

    def get(self, request, format=None):
        
        data = {
        'value':'this is a test value'
    }
        #usernames = [user.username for user in User.objects.all()]
        return Response(data)

#Class created for test purpose
class Like(APIView):
    def get(self, request, format = None):
        print(self.data)
        return Response({'value':'liked'})

def like(request):
    
    
    
    print('like function invoked')
    post = request.POST['value']
    
    print(post)
    currentpost = Post.objects.get(id = post)
    print(request.user)
    users = User.objects.all()
    if request.user in users:
        currentpost.likedby.append(str(request.user))
    else: 
        print('not logged in')
    if 'no likes' in currentpost.likedby:
        currentpost.likedby.remove('no likes')
    """
    if str(request.user) in currentpost.likedby:
        print("user already liked")
    else:
        currentpost.likedby.append(request.user)
        if 'no likes' in currentpost.likedby:
            currentpost.likedby.remove('no likes')"""

    currentpost.save()
    
    
   
    
    return JsonResponse({'value': 'Post has been liked successfully'})
    #return Response({'value':'liked'},template_name='home.html' )


def unlike(request):
    id = request.POST['value']
    currentpost = Post.objects.get(id = id)
    print(currentpost.likedby)
    currentpost.likedby.remove(str(request.user))
    if len(currentpost.likedby) == 0:
        currentpost.likedby.append('no likes')
    currentpost.save()
    return JsonResponse({'value': 'Post has been unliked successfully'})



def searchtrial(request):
    if 'term' in request.GET:
        qs = User.objects.filter(username__istartswith = request.GET['term'])
        users = []
        for i in qs:
            users.append(i.username)
        return JsonResponse(users, safe=False)
    return render(request,'searchtrial.html')



def signup(request):
    return render(request,'signup.html')


def user_registration(request):
    print('Registration invoked')
    uname = request.POST['uname']
    f_name = request.POST['f_name']
    l_name = request.POST['l_name']
    email = request.POST['email']
    passwd = request.POST['passwd']
    if User.objects.filter(username = uname).exists():
        return JsonResponse({'value':'username_exists'})
    elif User.objects.filter(email = email).exists():
        return JsonResponse({'value': 'email_exists'})
    else:
        user = User.objects.create_user(username = uname, first_name = f_name, last_name = l_name, email = email, password = passwd)
        user.save()
        return JsonResponse({'value': 'user_created'})
    


def testpage(request,id):
    id = id
    user = request.user
    messages = Messages.objects.all()
    u_messages = []
    print('current user: ', user)
    for i in messages:
        print('sender: :',i.sender)
        print('receiver :', i.receiver)
        if str(i.sender) == user.username or i.receiver == user.username:
            u_messages.append(i)
    print(u_messages)
    c_messages = []
    for i in u_messages:
        if i.sender == User.objects.get(id = id) or i.receiver == str(User.objects.get(id = id)) :
            c_messages.append(i)
    print(c_messages)


    users = User.objects.all()
    return render(request,'test.html',{'users':users, 'messages': c_messages,'c_user': str(user)})


def messages(request,id):
    if request.user not in User.objects.all():
        return redirect('signin')
    id = id
    user = request.user
    messages = Messages.objects.all()
    u_messages = []
    
    for i in messages:
        
        if str(i.sender) == user.username or i.receiver == user.username:
            u_messages.append(i)
    print(u_messages)
    c_messages = []
    for i in u_messages:
        if i.sender == User.objects.get(id = id) or i.receiver == str(User.objects.get(id = id)) :
            c_messages.append(i)
    print(c_messages)


    users = User.objects.all()
    return render(request,'chat.html',{'users':users, 'messages': c_messages,'c_user': User.objects.get(id = id)})

def chat(request):
    if request.user not in User.objects.all():
        return redirect('signin')
    all_users = User.objects.all()
    users = []
    for i in all_users:
        if i!= request.user:
            users.append(i)
    
    return render(request,'chatlist.html',{'all_users': users})


def send_message(request, receiver):
    user = receiver
    c_user = User.objects.get(username = user)
    new_message = Messages()
    new_message.receiver = str(c_user)
    new_message.sender = request.user
    new_message.message = request.POST['message']
    new_message.save()
    url = "/messages/" + str(c_user.id)
    return redirect(url)
#    return HttpResponse(receiver)