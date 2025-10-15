from django.contrib import admin
from .models import *

admin.site.register(Department)
admin.site.register(Designation)
#admin.site.register(Qualification)
admin.site.register(Employee)
admin.site.register(EmployeeProfessionalDetails)
admin.site.register(EmployeePersonalDetails)
admin.site.register(EmployeeContactDetails)
admin.site.register(EmployeeDocuments)
admin.site.register(EmployeeBankDetails)
