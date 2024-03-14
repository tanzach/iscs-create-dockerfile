from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip
from django.contrib import messages
from django.db.models import Q

# Create your views here.

# for reseting: Account.objects.all().delete()

def base(request):
    return render(request, 'myapp/base.html')

def homepage(request):
    employee = Employee.objects.all()
    return render(request, 'myapp/homepage.html', {'employee':employee})

def create_employee(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        id_number = request.POST.get('idnumber')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        all_id_number = Employee.objects.values_list('id_number', flat=True) # all id numbers present in database
        
        all_id_number_list = []
        for i in all_id_number: 
            all_id_number_list.append(i)
        
        if id_number in all_id_number_list: 
            messages.error(request, "ID Number is already taken.", extra_tags='alert-danger')
            return redirect('create_employee')
        else: 
            employee = Employee.objects.filter(name=name, id_number=id_number, rate=rate, allowance=allowance) # check again if exact duplicate exists
            if employee.exists() == True:
                messages.error(request, "Employee already exists.", extra_tags='alert-danger')
                return redirect('create_employee')
            else: 
                Employee.objects.create(name=name, id_number=id_number, rate=rate, allowance=allowance)
                messages.success(request, "Employee added successfully.", extra_tags='alert-success')
                return redirect('homepage')
    else: 
        return render(request, 'myapp/create_employee.html')

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    messages.success(request, "Employee deleted successfully.", extra_tags='alert-success')
    return redirect('homepage')

def update_employee(request, pk):
    if(request.method=="POST"):
        name = request.POST.get('newname')
        id_number = request.POST.get('newidnumber')
        rate = request.POST.get('newrate')
        allowance = request.POST.get('newallowance')

        original_id = Employee.objects.filter(pk=pk).values_list('id_number', flat=True) # original id number of employee
        original_id_list = []
        for og_id in original_id: 
            original_id_list.append(og_id)
        orig_id = str(original_id_list[0])
        
        all_id_number = Employee.objects.values_list('id_number', flat=True) # all id numbers present in database
        all_id_number_list = []
        for a in all_id_number:
            all_id_number_list.append(a)

        # ID Number must be unique, or the same with original ID Number
        if id_number in all_id_number_list:
            if id_number == orig_id: 
                Employee.objects.filter(pk=pk).update(name=name, id_number=id_number, rate=rate, allowance=allowance)
                messages.success(request, "Employee Details Updated.", extra_tags='alert-success')
                return redirect('homepage')  
            else: 
                messages.error(request, "ID already exists!", extra_tags='alert-danger')
                return redirect('update_employee', pk=pk)
        else: 
            Employee.objects.filter(pk=pk).update(name=name, id_number=id_number, rate=rate, allowance=allowance)
            messages.success(request, "Employee Details Updated.", extra_tags='alert-success')
            return redirect('homepage')         
    else: 
        emp = get_object_or_404(Employee, pk=pk)
        return render(request, 'myapp/update_employee.html', {'emp':emp})

def add_overtime(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if(request.method=="POST"):
        overtime = float(request.POST.get('overtimehours'))
        overtime_pay = (emp.rate/160)*(1.5)*(overtime)
        Employee.objects.filter(pk=pk).update(overtime_pay=overtime_pay)
        return redirect('homepage')
    else:
        return redirect('homepage')
    
def payslips(request):
    employee = Employee.objects.all()
    payslips = Payslip.objects.all()
    return render(request, 'myapp/payslips.html', {'payslips':payslips, 'employee':employee})

def view_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    employee = payslip.FKid_number  # Assuming the FK field is named 'FKid_number'
    cycle = payslip.pay_cycle
    if cycle == 1:  
        return render(request, 'myapp/view_payslipC1.html', {'employee': employee, 'payslip': payslip})
    elif cycle == 2:  
        return render(request, 'myapp/view_payslipC2.html', {'employee': employee, 'payslip': payslip})
    else:
        return render(request, 'myapp/error.html', {'error_message': 'Invalid pay cycle.'})

def create_payslip(request):
    if request.method == "POST":
        employee_id = request.POST.get('payrollfor')
        if employee_id == "all_employees":  # For all employees
            employee = Employee.objects.all()
            for emp in employee:
                month = request.POST.get('month')
                year = request.POST.get('year')
                cycle = int(request.POST.get('cycle'))

                empID = emp.id_number
                rate = float(emp.rate)
                allowances = float(emp.allowance)
                overtime = float(emp.overtime_pay)

                oldPayslip = Payslip.objects.filter(
                    Q(FKid_number=emp) & Q(month=month) & Q(year=year) & Q(pay_cycle=cycle)
                )
                if oldPayslip.exists():
                    messages.error(request, "Payslip already exists.", extra_tags='alert-danger')
                    return redirect('payslips')
                else:
                    if cycle == 1:
                        tax = ((rate/2) + allowances + overtime - 100) * 0.2
                        total_pay_with_tax = ((rate/2) + allowances + overtime - 100) - tax

                        payslip = Payslip(
                            FKid_number=emp,
                            month=month,
                            date_range="1-15",
                            year=year,
                            pay_cycle=cycle,
                            rate=rate,
                            earnings_allowance=allowances,
                            deductions_tax=tax,
                            deductions_health="0",
                            pag_ibig="100",
                            sss="0",
                            overtime=overtime,
                            total_pay=total_pay_with_tax
                        )
                        payslip.save()
                        Employee.objects.filter(id_number=empID).update(overtime_pay=0)
                        messages.success(request, "Payslip created successfully.", extra_tags='success')
                    elif cycle == 2:
                        PhilHealth = rate * 0.04
                        SSS = rate * 0.045
                        tax = ((rate/2) + allowances + overtime - PhilHealth - SSS) * 0.2
                        total_pay_with_tax = ((rate/2) + allowances + overtime - PhilHealth - SSS) - tax

                        if month in ["January", "March", "May", "July", "August", "October", "December"]:
                            date_range = "16-31"
                        elif month == "February":
                            date_range = "16-28"
                        else:
                            date_range = "16-30"

                        payslip = Payslip(
                            FKid_number=emp,
                            month=month,
                            date_range=date_range,
                            year=year,
                            pay_cycle=cycle,
                            rate=rate,
                            earnings_allowance=allowances,
                            deductions_tax=tax,
                            deductions_health=PhilHealth,
                            pag_ibig="0",
                            sss=SSS,
                            overtime=overtime,
                            total_pay=total_pay_with_tax
                        )
                        payslip.save()
                        Employee.objects.filter(id_number=empID).update(overtime_pay=0)
                        messages.success(request, "Payslip created successfully.", extra_tags='success')
                    else:
                        messages.error(request, "Invalid cycle value.", extra_tags='error')
            return redirect('payslips')
        else:  # For one employee at a time
            month = request.POST.get('month')
            year = request.POST.get('year')
            cycle = int(request.POST.get('cycle'))

            emp = get_object_or_404(Employee, id_number=employee_id)
            rate = float(emp.rate)
            allowances = float(emp.allowance)
            overtime = float(emp.overtime_pay)
            oldPayslip = Payslip.objects.filter(
                Q(FKid_number=emp) & Q(month=month) & Q(year=year) & Q(pay_cycle=cycle)
            )
            if oldPayslip.exists():
                messages.error(request, "Payslip already exists.", extra_tags='error')
            else:
                if cycle == 1:
                    tax = ((rate/2) + allowances + overtime - 100) * 0.2
                    total_pay_with_tax = ((rate/2) + allowances + overtime - 100) - tax

                    payslip = Payslip(
                        FKid_number=emp,
                        month=month,
                        date_range="1-15",
                        year=year,
                        pay_cycle=cycle,
                        rate=rate,
                        earnings_allowance=allowances,
                        deductions_tax=tax,
                        deductions_health="0",
                        pag_ibig="100",
                        sss="0",
                        overtime=overtime,
                        total_pay=total_pay_with_tax
                    )
                    payslip.save()
                    Employee.objects.filter(id_number=employee_id).update(overtime_pay=0)
                    messages.success(request, "Payslip created successfully.", extra_tags='success')
                elif cycle == 2:
                    PhilHealth = rate * 0.04
                    SSS = rate * 0.045
                    tax = ((rate/2) + allowances + overtime - PhilHealth - SSS) * 0.2
                    total_pay_with_tax = ((rate/2) + allowances + overtime - PhilHealth - SSS) - tax

                    if month in ["January", "March", "May", "July", "August", "October", "December"]:
                        date_range = "16-31"
                    elif month == "February":
                        date_range = "16-28"
                    else:
                        date_range = "16-30"

                    payslip = Payslip(
                        FKid_number=emp,
                        month=month,
                        date_range=date_range,
                        year=year,
                        pay_cycle=cycle,
                        rate=rate,
                        earnings_allowance=allowances,
                        deductions_tax=tax,
                        deductions_health=PhilHealth,
                        pag_ibig="0",
                        sss=SSS,
                        overtime=overtime,
                        total_pay=total_pay_with_tax
                    )
                    payslip.save()
                    Employee.objects.filter(id_number=employee_id).update(overtime_pay=0)
                    messages.success(request, "Payslip created successfully.", extra_tags='success')

            return redirect('payslips')
    else:
        return redirect('payslips')




