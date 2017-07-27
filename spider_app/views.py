from django.shortcuts import render

# Create your views here.
from spider_app.models import Item, Project


def pages(request):
    project_name = request.GET.get('project')

    if not project_name:
        project = Project.objects.first()
    else:
        project = Project.objects.filter(name=project_name).first()

    return render(request, "index.html", context={
        'project': project,
        'projects': Project.objects.all(),
        'items': Item.objects.filter(entry__project_id=project.id).order_by("-pk")[0:100] if project else []
    })
