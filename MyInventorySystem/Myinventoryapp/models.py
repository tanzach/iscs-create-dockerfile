# I have not discussed the Python language code in my program with anyone other than my instructor or the teaching assistants assigned to this course.
# I have not used Python language code obtained from another student, or any other unauthorized source, either modified or unmodified.
# If any Python language code or documentation used in my program was obtained from another source, such as a textbook or course notes, that has been clearly noted with a proper citation in the comments of my program

from django.db import models
from django.utils import timezone 

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    rate = models.FloatField()
    overtime_pay = models.FloatField(null=True, default=0.0)
    allowance = models.FloatField(null=True, default=0.0)

    def getName(self):
        return self.name
    
    def getID(self):
        return self.id_number
    
    def getRate(self):
        return self.rate
    
    def getOvertime(self):
        return self.overtime_pay
    
    def resetOvertime(self):
        self.overtime_pay = 0
    
    def getAllowance(self):
        return self.allowance
    
    def __str__(self):
        return "pk: " + str(self.id_number) + ", rate: " + str(self.rate)
    
class Payslip(models.Model):
    FKid_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=15)
    date_range = models.CharField(max_length=5)
    year = models.CharField(max_length=4)
    pay_cycle = models.IntegerField()
    rate = models.FloatField()
    earnings_allowance = models.FloatField()
    deductions_tax = models.FloatField()
    deductions_health = models.FloatField()
    pag_ibig = models.FloatField()
    sss = models.FloatField()
    overtime = models.FloatField()
    total_pay = models.FloatField()

    def getIDNumber(self):
        return self.FKid_number
    
    def getMonth(self):
        return self.month
    
    def getDate_range(self):
        return self.date_range
    
    def getYear(self):
        return self.year
    
    def getPay_cycle(self):
        return self.pay_cycle
    
    def getRate(self):
        return self.rate
    
    def getCycleRate(self):
        cyclerate = self.rate * 0.5
        return cyclerate

    def getEarnings_allowance(self):
        return self.earnings_allowance

    def getDeductions_tax(self):
        self.deductions_tax = ((self.rate/2) + self.earnings_allowance + self.overtime - self.pag_ibig - self.deductions_health - self.sss) * 0.2
        return abs(self.deductions_tax)

    def getDeductions_health(self):
        return self.deductions_health
    
    def getTotal_deductions(self):
        total_deductions = abs(self.deductions_tax) + abs(self.deductions_health) + abs(self.sss) + abs(self.pag_ibig)
        return total_deductions
    
    def getPag_ibig(self):
        return self.pag_ibig
    
    def getSSS(self):
        return self.sss
    
    def getOvertime(self):
        return self.overtime
    
    def getTotalGrossPay(self):
        gross_pay = self.rate + self.earnings_allowance + self.overtime
        return gross_pay

    def getTotal_pay(self):
        total_pay = (self.rate + self.earnings_allowance + self.overtime) - (abs(self.deductions_tax) + abs(self.deductions_health) + abs(self.sss) + abs(self.pag_ibig))
        return total_pay
    
    def __str__(self):
        return "pk: " + str(self.pk) + ", Employee: " + str(self.FKid_number) + ", Period: " + str(self.month) + str(self.date_range) + ", " + str(self.year) + ", Cycle: " + str(self.pay_cycle) + ", Total Pay: " + str(self.total_pay)