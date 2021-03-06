# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Project, Bug
from .forms import CreateNewBug
from django.contrib import messages

from rest_framework import viewsets,generics
from app.serializers import ProjectSerializer,ProjectBugSerializer
from rest_framework.decorators import api_view




""" Render html template, List of bugs and projects will handled by Vuejs"""
def homepage(request):
	
	return render(request, 'index.html')


""" API for listing projects """
class ProjectViewSet(viewsets.ModelViewSet):

	queryset = Project.objects.all()

	serializer_class = ProjectSerializer


""" API for listing project bugs """
class ProjectBugViewSet(viewsets.ModelViewSet):

	queryset = Bug.objects.all()
	serializer_class = ProjectBugSerializer



""" API filter by project """
class BugByProjectList(generics.ListAPIView):

    serializer_class = ProjectBugSerializer

    def get_queryset(self):
        """ Return a list of all bugs by the project id passed on url"""
        project = self.kwargs['project']
        return Bug.objects.filter(project=project)



""" Create a new bug """
def new_bug(request):
	
	""" 
	Get list of projects to show on selection 
	"""
	list_of_projects = Project.objects.all()

	""" Handle form submission for creating new project bug """
	if request.method == "POST":
		form = CreateNewBug(request.POST)
		if form.is_valid():
			""" Get project instance """
			project = Project.objects.get(pk=request.POST.get('project'))
			description = form.cleaned_data['description']

			""" save bug """
			savebug = Bug(description=description,project=project)
			savebug.save()

			msg = messages.success(request, 'Project bug created successfuly')
			return redirect(new_bug)

		""" Handle invalid form submission """
		args = {"form":form, "projects":list_of_projects}
		return render(request, 'new-bug.html', args)

	""" Handle other type of requests such as GET """
	form = CreateNewBug()
	args = {"form":form, "projects":list_of_projects}
	return render(request, 'new-bug.html', args)