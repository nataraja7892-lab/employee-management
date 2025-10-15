from django.db import models
import os

def employee_related_upload_path(instance, filename, folder):
    """
    Upload path for related models:
    employees/{employee_id}/{folder}/{filename}
    Replaces previous files with fixed names per type.
    """
    ext = filename.split('.')[-1]
    filename_map = {
        'photo': f"profile.{ext}",
        'aadhar': f"aadhar.{ext}",
        'pan': f"pan.{ext}",
        'joining_letter': f"joining_letter.{ext}",
        'tenth': f"10th.{ext}",
        'puc': f"puc.{ext}",
        'degree': f"degree.{ext}",
        'pg': f"pg.{ext}",
        'phd': f"phd.{ext}",
        'experience': f"experience_certificate.{ext}",
        'bank_passbook': f"bank_passbook.{ext}",
    }
    new_filename = filename_map.get(folder, filename)
    return f"employees/{instance.employee.employee_id}/{folder}/{new_filename}"

def employee_upload_path(instance, filename, folder):
    """
    Upload path for Employee model (direct):
    employees/{employee_id}/{folder}/{filename}
    """
    ext = filename.split('.')[-1]
    filename_map = {
        'photo': f"profile.{ext}",
    }
    new_filename = filename_map.get(folder, filename)
    return f"employees/{instance.employee_id}/{folder}/{new_filename}"

# Employee model photo
def employee_photo_upload_path(instance, filename):
    return employee_upload_path(instance, filename, 'photo')

# EmployeeProfessionalDetails
def experience_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'experience')

# EmployeeDocuments
def aadhar_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'aadhar')

def pan_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'pan')

def joining_letter_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'joining_letter')

def tenth_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'tenth')

def puc_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'puc')

def degree_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'degree')

def pg_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'pg')

def phd_certificate_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'phd')

# EmployeeBankDetails
def bank_passbook_upload_path(instance, filename):
    return employee_related_upload_path(instance, filename, 'bank_passbook')

class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    CATEGORY_CHOICES = [('Teaching','Teaching'), ('Non-Teaching','Non-Teaching')]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

'''class Qualification(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name'''

class Employee(models.Model):
    CATEGORY_CHOICES = [('Teaching','Teaching'), ('Non-Teaching','Non-Teaching')]
    TYPE_CHOICES = [('Temporary','Temporary'), ('Permanent','Permanent')]

    employee_id = models.CharField(max_length=10, primary_key=True)  # TCH001 / NTC001
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to=employee_photo_upload_path, blank=True, null=True)
    employee_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    qualifications = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"
    
    def get_photo_url(self):
        """Safely get photo URL"""
        return self.photo.url if self.photo else None

class EmployeeProfessionalDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    present_working_as = models.CharField(max_length=100, blank=True, null=True)
    date_of_join = models.DateField(blank=True, null=True)
    date_of_exit = models.DateField(blank=True, null=True)
    previous_experience_years = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    experience_certificate = models.FileField(upload_to=experience_certificate_upload_path, blank=True, null=True)

    def get_experience_certificate_url(self):
        """Safely get experience certificate URL"""
        return self.experience_certificate.url if self.experience_certificate else None
    
    def __str__(self):
        return f"Professional Details of {self.employee.employee_id} - {self.employee.first_name} {self.employee.last_name}"

class EmployeePersonalDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')], blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=[('Single','Single'),('Married','Married'),('Divorced','Divorced'),('Widowed','Widowed')], blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Personal Details of {self.employee.employee_id} - {self.employee.first_name} {self.employee.last_name}"

class EmployeeContactDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    contact_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Contact Details of {self.employee.employee_id} - {self.employee.first_name} {self.employee.last_name}"

class EmployeeDocuments(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    aadhar_number= models.CharField(max_length=20, blank=True, null=True)
    aadhar_certificate = models.FileField(
        upload_to=aadhar_certificate_upload_path, blank=True, null=True
    )
    pan_number = models.CharField(max_length=20, blank=True, null=True)
    pan_certificate = models.FileField(
        upload_to=pan_certificate_upload_path, blank=True, null=True
    )
    joining_letter = models.FileField(
        upload_to=joining_letter_upload_path, blank=True, null=True
    )
    tenth_certificate = models.FileField(
        upload_to=tenth_certificate_upload_path, blank=True, null=True
    )
    puc_certificate = models.FileField(
        upload_to=puc_certificate_upload_path, blank=True, null=True
    )
    degree_certificate = models.FileField(
        upload_to=degree_certificate_upload_path, blank=True, null=True
    )
    pg_certificate = models.FileField(
        upload_to=pg_certificate_upload_path, blank=True, null=True
    )
    phd_certificate = models.FileField(
        upload_to=phd_certificate_upload_path, blank=True, null=True
    )

    def get_aadhar_url(self):
        """Safely get Aadhar certificate URL"""
        return self.aadhar_certificate.url if self.aadhar_certificate else None
    
    def get_pan_url(self):
        """Safely get PAN certificate URL"""
        return self.pan_certificate.url if self.pan_certificate else None
    
    def get_joining_letter_url(self):
        """Safely get joining letter URL"""
        return self.joining_letter.url if self.joining_letter else None
    
    def get_tenth_certificate_url(self):
        """Safely get 10th certificate URL"""
        return self.tenth_certificate.url if self.tenth_certificate else None
    
    def get_puc_certificate_url(self):
        """Safely get PUC certificate URL"""
        return self.puc_certificate.url if self.puc_certificate else None
    
    def get_degree_certificate_url(self):
        """Safely get degree certificate URL"""
        return self.degree_certificate.url if self.degree_certificate else None
    
    def get_pg_certificate_url(self):
        """Safely get PG certificate URL"""
        return self.pg_certificate.url if self.pg_certificate else None
    
    def get_phd_certificate_url(self):
        """Safely get PhD certificate URL"""
        return self.phd_certificate.url if self.phd_certificate else None
    
    def __str__(self):
        return f"Documents of {self.employee.employee_id} - {self.employee.first_name} {self.employee.last_name}"

class EmployeeBankDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    pf_account_number = models.CharField(max_length=50, blank=True, null=True)
    esi_number = models.CharField(max_length=50, blank=True, null=True)
    uan_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_passbook = models.FileField(
        upload_to=bank_passbook_upload_path, blank=True, null=True
    )

    def get_bank_passbook_url(self):
        """Safely get bank passbook URL"""
        return self.bank_passbook.url if self.bank_passbook else None
    
    def __str__(self):
        return f"Bank Details of {self.employee.employee_id} - {self.employee.first_name} {self.employee.last_name}"