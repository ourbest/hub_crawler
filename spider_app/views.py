from django.shortcuts import render

# Create your views here.
from spider_app.models import Item, Project


def pages(request):
    project_name = request.GET.get('project')
    entry_id = request.GET.get('entry')

    if not project_name:
        project = Project.objects.first()
    else:
        project = Project.objects.filter(name=project_name).first()

    size = 200
    if entry_id:
        items = Item.objects.filter(entry_id=entry_id).order_by("-pk")[0:size]
    else:
        items = Item.objects.filter(entry__project_id=project.id).order_by("-pk")[0:size] if project else []

    return render(request, "index.html", context={
        'project': project,
        'projects': Project.objects.all(),
        'items': items
    })
