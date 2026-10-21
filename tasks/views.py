from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    tasks = Task.objects.order_by('-created_at')
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(done=True).count()
    remaining_tasks = total_tasks - completed_tasks

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'remaining_tasks': remaining_tasks,
    })


def toggle_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.done = not task.done
        task.save()
    return redirect('task_list')


def delete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    return redirect('task_list')


def clear_completed_tasks(request):
    if request.method == 'POST':
        Task.objects.filter(done=True).delete()
    return redirect('task_list')