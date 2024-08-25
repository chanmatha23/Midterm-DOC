from .models import *
from django.shortcuts import render
from django.views import View
from django.db.models import *
from django.http import JsonResponse

class EmployeeView(View):
    def get(self, request):
        emp = Employee.objects.all()
        return render(request, "employee.html", {'emp':emp})

class ProjectView(View):
    def get(self, request):
        pro = Project.objects.all()
        return render(request, "project.html", {'pro':pro})
    def delete(self, request, id):
        pro = Project.objects.get(pk=id)
        pro.delete()
        return JsonResponse({'delete': True})

class ProjectDetail(View):
    def get(self, request, id):
        pro = Project.objects.get(pk=id)
        startdate = pro.start_date.strftime('%Y-%m-%d')
        duedate = pro.due_date.strftime('%Y-%m-%d')
        staff = pro.staff.all()
        return render(request, "project_detail.html", {'pro':pro, 'start':startdate, 'due':duedate, 'staff':staff})
    def delete(self, request, id, staffid):
        pro = Project.objects.get(pk=id)
        pro.staff.remove(staffid)
        return JsonResponse({'Kickstaff': True})
    def put(self, request, id, staffid):
        pro = Project.objects.get(pk=id)
        pro.staff.add(staffid)
        return JsonResponse({'add': True})

class PositionView(View):
    def get(self, request):
        pos = Position.objects.all().annotate(count = Count('employee')).order_by('id')
        return render(request, "position.html", {'pos':pos})