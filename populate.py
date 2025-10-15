# demo_employees_standalone.py

import os
import django
import random
from faker import Faker
from django.core.files import File

# ----------------------------
# Setup Django environment
# ----------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_mgmt.settings')  # Replace 'student_mgmt' with your project name
django.setup()

# ----------------------------
# Import models
# ----------------------------
from employees.models import (
    Department, Designation, Employee, EmployeeProfessionalDetails,
    EmployeePersonalDetails, EmployeeContactDetails, EmployeeDocuments, EmployeeBankDetails
)

fake = Faker()

# ----------------------------
# Departments
# ----------------------------
dept_names = ['BSC', 'BBA', 'BCOM', 'BCA', 'BA', 'MA', 'MSC', 'MCOM']
departments = {}
for name in dept_names:
    dept, _ = Department.objects.get_or_create(name=name)
    departments[name] = dept

# ----------------------------
# Designations
# ----------------------------
teaching_designations = ['Lecturer', 'HOD']
non_teaching_designations = ['Peon', 'Clerk', 'Attendant']
designations = {}

for name in teaching_designations:
    des, _ = Designation.objects.get_or_create(name=name, category='Teaching')
    designations[name] = des

for name in non_teaching_designations:
    des, _ = Designation.objects.get_or_create(name=name, category='Non-Teaching')
    designations[name] = des

# ----------------------------
# Employees Data
# ----------------------------
base_doc_path = r"C:\Users\medar\OneDrive\Documents\Documents"
employee_list = [
    {
        'employee_id': 'TCH001',
        'first_name': 'Rohit',
        'last_name': 'Sharma',
        'short_name': 'RSh',
        'employee_type': 'Permanent',
        'category': 'Teaching',
        'department': departments['BSC'],
        'designation': designations['Lecturer'],
        'qualifications': 'MSc, PhD',
        'date_of_join': '2020-07-01',
        'previous_experience_years': 5.0,
        'gender': 'Male',
        'blood_group': 'O+',
        'dob': '1985-08-15',
        'marital_status': 'Married'
    },
    {
        'employee_id': 'TCH002',
        'first_name': 'Priya',
        'last_name': 'Verma',
        'short_name': 'PVer',
        'employee_type': 'Temporary',
        'category': 'Teaching',
        'department': departments['BBA'],
        'designation': designations['HOD'],
        'qualifications': 'MBA',
        'date_of_join': '2022-01-15',
        'previous_experience_years': 2.0,
        'gender': 'Female',
        'blood_group': 'A+',
        'dob': '1990-11-22',
        'marital_status': 'Single'
    },
    {
        'employee_id': 'TCH003',
        'first_name': 'Anil',
        'last_name': 'Kumar',
        'short_name': 'AKu',
        'employee_type': 'Permanent',
        'category': 'Teaching',
        'department': departments['MSC'],
        'designation': designations['Lecturer'],
        'qualifications': 'MSc, PhD',
        'date_of_join': '2018-05-10',
        'previous_experience_years': 10.0,
        'gender': 'Male',
        'blood_group': 'B+',
        'dob': '1978-04-30',
        'marital_status': 'Married'
    },
    {
        'employee_id': 'NTC001',
        'first_name': 'Sunita',
        'last_name': 'Patel',
        'short_name': 'SPa',
        'employee_type': 'Permanent',
        'category': 'Non-Teaching',
        'department': departments['BCOM'],
        'designation': designations['Clerk'],
        'qualifications': 'BBA',
        'date_of_join': '2015-03-01',
        'previous_experience_years': 8.0,
        'gender': 'Female',
        'blood_group': 'AB+',
        'dob': '1988-07-10',
        'marital_status': 'Married'
    },
    {
        'employee_id': 'NTC002',
        'first_name': 'Rajesh',
        'last_name': 'Singh',
        'short_name': 'RS',
        'employee_type': 'Temporary',
        'category': 'Non-Teaching',
        'department': departments['BA'],
        'designation': designations['Peon'],
        'qualifications': 'BCA',
        'date_of_join': '2021-09-20',
        'previous_experience_years': 3.0,
        'gender': 'Male',
        'blood_group': 'O-',
        'dob': '1992-02-05',
        'marital_status': 'Single'
    }
]

# ----------------------------
# File paths
# ----------------------------
for emp in employee_list:
    # Employee
    employee = Employee.objects.create(
        employee_id=emp['employee_id'],
        first_name=emp['first_name'],
        last_name=emp['last_name'],
        short_name=emp['short_name'],
        photo=File(open(os.path.join(base_doc_path, "download.jpeg"), 'rb'), name="download.jpeg"),
        employee_type=emp['employee_type'],
        category=emp['category'],
        department=emp['department'],
        designation=emp['designation'],
        qualifications=emp['qualifications']
    )

    # Professional Details
    exp_file_path = os.path.join(base_doc_path, "experience_certificate.pdf")
    EmployeeProfessionalDetails.objects.create(
        employee=employee,
        present_working_as=employee.designation.name,
        date_of_join=emp['date_of_join'],
        previous_experience_years=emp['previous_experience_years'],
        experience_certificate=File(open(exp_file_path, 'rb'), name=os.path.basename(exp_file_path))
    )

    # Personal Details
    EmployeePersonalDetails.objects.create(
        employee=employee,
        gender=emp['gender'],
        blood_group=emp['blood_group'],
        date_of_birth=emp['dob'],
        marital_status=emp['marital_status'],
        father_name=fake.name_male(),
        mother_name=fake.name_female()
    )

    # Contact Details
    EmployeeContactDetails.objects.create(
        employee=employee,
        mobile_number=fake.phone_number(),
        email=fake.email(),
        permanent_address=fake.address(),
        contact_address=fake.address()
    )

    doc_kwargs = {
        'employee': employee,
        'aadhar_number': str(fake.random_number(digits=12, fix_len=True)),
        'pan_number': fake.bothify(text='?????#??##?')
    }

    # Set image files for Aadhar and PAN
    aadhar_path = os.path.join(base_doc_path, 'download.jpeg')
    if os.path.exists(aadhar_path):
        doc_kwargs['aadhar_certificate'] = File(open(aadhar_path, 'rb'), name='aadhar_certificate.jpeg')

    pan_path = os.path.join(base_doc_path, 'download.jpeg')
    if os.path.exists(pan_path):
        doc_kwargs['pan_certificate'] = File(open(pan_path, 'rb'), name='pan_certificate.jpeg')

    # Create EmployeeDocuments record
    EmployeeDocuments.objects.create(**doc_kwargs)

# Bank Details
    bank_file_path = os.path.join(base_doc_path, "download.jpeg")
    EmployeeBankDetails.objects.create(
        employee=employee,
        pf_account_number=fake.bothify(text='PF######'),
        esi_number=fake.bothify(text='ESI######'),
        uan_number=fake.bothify(text='UAN######'),
        bank_name=fake.company(),
        branch_name=fake.city(),
        ifsc_code=fake.bothify(text='IFSC#######'),
        account_number=str(fake.random_number(digits=12, fix_len=True)),
        bank_passbook=File(open(bank_file_path, 'rb'), name=os.path.basename(bank_file_path))  # NO with open
    )

print("✅ All demo employees inserted successfully with complete details!")
