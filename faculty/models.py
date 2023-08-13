from django.db import models
from authentication.models import User
from core.models import City, TimestampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Institute(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    helpline_number = PhoneNumberField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)


class Course(TimestampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="courses")
    duration = models.IntegerField(verbose_name="course duration in days")

    def __str__(self) -> str:
        return str(self.id)


class Enrollment(TimestampedModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.id)
