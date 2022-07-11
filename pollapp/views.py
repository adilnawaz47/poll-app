from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from django.template import context
from pollapp.models import Question, Answers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate , login

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if not user_obj.exists():
            messages.debug(request, "Account not found")
            return redirect('/register/')
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/dashboard/')
        messages.debug(request,'Invalid User')
        return redirect('/')
    else:
        return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            return redirect('/register/')
        user_obj = User.objects.create(username = email)
        user_obj.set_password(password)
        user_obj.save()
        return redirect('/')
    else:
        return render(request, "register.html")

def dashboard(request):
    total_questions = len(Question.objects.all())
    user = len(User.objects.all())
    context ={
        "user": user,
        "total_questions" : total_questions
    }
    
    return render(request , 'dashboard.html', context)

def create_poll(request):
    if request.method == "POST":
        question = request.POST.get('question')
        answer = request.POST.getlist('answers')
        question_obj = Question.objects.create(
            user = request.user,
            question_text = question
        )
        for answer in answer:
            Answers.objects.create(
                answer_text = answer,
                question = question_obj
            )
        messages.info(request, 'Your Poll Has been created')
        return redirect('/create_poll/')
    return render(request, 'create_poll.html')

def see_answers(request):
    questions = Question.objects.filter(user = request.user)
    for question in questions:

        answe =  question.answer.all()
        for i in answe:
            print(i.answer_text)
            print("calculate % ", i.calculate_percentage)
    context = {
        'questions' : questions,
        
        }
    return render(request ,'see_ansswers.html' ,context)

@api_view(['POST'])
def save_question_result(request):
    data = request.data
    question_uid = data.get('question_uid')
    answer_uid = data.get('answer_uid')

    if question_uid is None and answer_uid is None:
        payload ={'data': "Both question uid and answer uid are required", 'status':False}


    question_obj = Question.objects.get(uid = question_uid)
    answer_obj = Answers.objects.get(uid = answer_uid)
    answer_obj.counter += 1
    answer_obj.save()

    payload ={'data': question_obj.calculate_percentage(), 'status':True}

    return Response(payload)



def question_detail(request, question_uid):
    try:
        question_obj = Question.objects.get(uid = question_uid)
        context={
            "question": question_obj,
            "answer" : Answers.objects.all()
        }
        return render (request, 'question.html', context)
    except Exception as e:
        print(e)
        return redirect('/question/')


def answers(request, uid):
    questions = Question.objects.filter(uid = uid)
    for question in questions:

        answe =  question.answer.all()
        for i in answe:
            print(i.answer_text)
            print("calculate % ", i.calculate_percentage)
    context = {
        'questions' : questions,
        
        }
    return render(request ,'answers.html' ,context)