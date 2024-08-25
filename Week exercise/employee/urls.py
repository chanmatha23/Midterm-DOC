from django.urls import path
from .views import *

urlpatterns = [
    path('', EmployeeView.as_view(), name='employee'),
    path('position/', PositionView.as_view(), name='position'),
    path('project/', ProjectView.as_view(), name='project'),
    path('project/detail/<int:id>/', ProjectDetail.as_view(), name='projectdetail'),
    path('project/detail/<int:id>/remove/<int:staffid>/', ProjectDetail.as_view(), name='projectremovestaff'),
    path('project/detail/<int:id>/add/<int:staffid>/', ProjectDetail.as_view(), name='projectaddstaff'),
    path('project/delete/<int:id>/', ProjectView.as_view(), name='projectdelete'),
]
