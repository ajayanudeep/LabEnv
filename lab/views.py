from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import create_class_form,create_assignment_form
from django.contrib.auth.models import User
from .models import ClassRoom,Assignment
from django.shortcuts import redirect



@login_required(login_url='/accounts/login')
def home(request):
    classes = ClassRoom.objects.filter(host=request.user)
    all_classes = ClassRoom.objects.all()
    classes_you_are_in=[]
    for user_class in all_classes:
        if user_class.students.filter(username = request.user):
            classes_you_are_in.append(user_class)
    return render(request, 'lab/home.html',{'classes':classes,'classes_you_are_in':classes_you_are_in})

@login_required(login_url='/accounts/login')
def classroom(request,pk):
    classroom = ClassRoom.objects.get(id=pk)
    assignments = classroom.assignment_set.all()
    students = classroom.students.all()
    return render(request, 'lab/classroom.html',{'assignments':assignments,'classroom':classroom,'students':students})

@login_required(login_url='/accounts/login')
def create_class(request):
    form = create_class_form()
    if request.method == "POST":
        form = create_class_form(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            classname = form.cleaned_data['classname']
            class_room_details = ClassRoom(subject=subject,classname=classname)
            class_room_details.host = request.user
            class_room_details.save()
            return redirect('/lab')
    return render(request, 'lab/create_class.html',{"form":form})

@login_required(login_url='/accounts/login')
def create_assignment(request,pk):
    classroom = ClassRoom.objects.get(id=pk)
    form = create_assignment_form()
    if request.method == 'POST':
        form = create_assignment_form(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            type = form.cleaned_data['type']
            due_date = form.cleaned_data['due_date']
            due_time = form.cleaned_data['due_time']
            assignment_details = Assignment(question=question,type=type,due_date=due_date,due_time=due_time)
            assignment_details.class_in = classroom
            assignment_details.save()
            return redirect('classroom',pk=pk)
    return render(request, 'lab/create_assignment.html',{"form":form,"classroom":classroom})

@login_required(login_url='/accounts/login')
def question(request,pk):
    assignment = Assignment.objects.get(id=pk)
    return render(request, 'lab/question.html',{'assignment':assignment})
