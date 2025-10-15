from django.urls import path,include
from .views import *

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('register_employee/', register_employee, name='register_employee'),
    path('employee_list/', employee_list, name='employee_list'),
    path('department/<str:dept_name>/', department_details_view, name='department_details'),
    path('employee_profile/<str:emp_id>/', employee_profile_view, name='employee_profile'),
    path('edit_dashboard/', edit_dashboard, name='edit_dashboard'),
    path('edit_employee/<str:emp_id>/', edit_employee, name='edit_employee'),
    path('delete_employee/<str:emp_id>/', delete_employee, name='delete_employee'),
    path('search_employee/', search_employee, name='search_employee'),
    path('employee-details/', employee_details, name='employee_details_by_department'),
    path('export-csv/',  export_csv, name='export_csv'),
    path('export-excel/',export_excel, name='export_excel'),
    path('export-pdf/', export_pdf, name='export_pdf'), 
    path('analytics/', analytics_view, name='employee_analytics'),
    path('employees/', employee_list_all, name='all_staff'),
    path('employees/teaching/', employee_list_teaching, name='teaching_staff'),
    path('employees/non-teaching/', employee_list_non_teaching, name='non_teaching_staff'),
    path('employees/phd/', employee_list_phd, name='phd_staff'),
    path('h/',he,name='hello'),
    path('gg/',gg,name='gg'),
]