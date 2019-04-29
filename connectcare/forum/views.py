from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question
from django.db.models import Q
from .forms import QuestionForm,CommentForm
from django.shortcuts import redirect
from profiledet.models import USERMODEL
from rolepermissions.decorators import has_permission_decorator,has_role_decorator

# Create your views here.
@login_required()
@has_permission_decorator('view_forum')
@has_permission_decorator('add_question')
def question_create(request):
       form = QuestionForm(request.POST or None)
       if form.is_valid():
           instance = form.save(commit=False)
           instance.save()
           return redirect('questions')
       return render(request, 'forum/create.html', {"form":form})


@login_required()
@has_permission_decorator('view_forum')
def question_list(request):
        queryset_list=Question.objects.all()
        query = request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
        page_request_var = "page"
        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        return render(request, 'forum/index.html', {"object_list":queryset,"title":"Question and Answer Forum","page_request_var":page_request_var})

@login_required()
@has_permission_decorator('view_forum')
def question_detail(request,id=None):
    instance=get_object_or_404(Question,id=id)
    return render(request,'forum/detail.html',{"title":instance.title,"instance":instance})

@login_required()
@has_permission_decorator('view_forum')
@has_permission_decorator('add_comment')
def add_comment_to_post(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            p = USERMODEL.objects.get(name = request.user.username)
            comment.author = p.aname
            comment.question = question
            comment.save()
            return redirect('detail', id=question.id)
    else:
        form = CommentForm()
    return render(request, 'forum/add_comment_to_post.html',{"question" : question ,'form': form})
