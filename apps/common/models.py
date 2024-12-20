from django.db import models

class Sponsor(models.Model):
    STATUS = (
        ("new","Yangi"),
        ("in_moderation","Moderatsiyada"),
        ("confirmed","Tasdiqlangan"),
        ("canceled","Bekor qilingan")
    )
    SPONSOR_TYPE = (
        ("physical_person","Jismoniy shaxs"),
        ("legal_entity","Yuridik shaxs")
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS, default="Moderatsiyada")
    sponsor_type = models.CharField(max_length=255, choices=SPONSOR_TYPE)
    organization_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name

class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    STUDENT_TYPE = (
        ("bakalavr","Bakalavr"),
        ("magister", "Magister")
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    student_type = models.CharField(max_length=255, choices=STUDENT_TYPE, default="Bakalavr")
    contract_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name

class StudentSponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    allocated_amount = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.sponsor.full_name} --- {self.student.full_name}"