from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from datetime import datetime
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from TabibuNet.models import Patient


class Ward(models.Model):
    TYPE = (('children', 'CHILDREN'),
        ('male', 'MALE'),
        ('female', 'FEMALE'))
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=TYPE)

    def __str__(self):
        return self.name


class Bed(models.Model):
    name = models.CharField(max_length=20)
    ward = models.ForeignKey(Ward, related_name='ward_bed')

    def __str__(self):
        return self.name


class Admission(models.Model):
    STATUS = (
        ('active', 'ACTIVE'),
        ('closed', 'CLOSED'),


    )
    patient = models.ForeignKey(Patient, related_name='patient_admission')
    bed = models.ForeignKey(Bed, related_name='bed_admitted', null=True)
    reason = models.TextField(default='Reason for admission')
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='active')
    slug = models.SlugField(default='admission')

    def save(self, *args, **kwargs):
        super(Admission, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.patient.first_name) + "-" + str(self.id)
            self.save()
        if self.status == 'closed' and self.discharge_date is None:
            self.discharge_date = datetime.now()
        elif self.discharge_date is not None:
            self.discharge_date = self.discharge_date
        super(Admission, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.patient.id)
    def get_absolute_url(self):
        return reverse('inpatient:admission_detail', args=[self.admission_date.year,
                                                 self.admission_date.strftime('%m'),
                                                 self.admission_date.strftime('%d'),
                                                 self.slug])



class Medication(models.Model):
    admission = models.ForeignKey(Admission, related_name='medication')
    date = models.DateField(auto_now_add=True)
    medication = models.CharField(max_length=100)
    strength = models.CharField(max_length=30)
    instruction = models.CharField(max_length=200)
    refill = models.IntegerField()
    active = models.BooleanField(default=True)


class Medtest(models.Model):
    admission = models.ForeignKey(Admission, related_name='medical_test')
    name = models.CharField(max_length=200)
    examination = models.TextField()
    diagnosis = models.TextField()
    slug = models.SlugField(max_length=200)

    def save(self, *args, **kwargs):
        super(Medtest, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('TabibuNet:test-detail', args=[self.admission.admission_date.year,
                                                       self.admission.admission_date.strftime('%m'),
                                                       self.admission.admission_date.strftime('%d'),
                                                       self.slug])


class LabImage(models.Model):
    medical_test = models.ForeignKey(Medtest, related_name='lab_images')
    image = models.ImageField()


class Obstetrics(models.Model):
    admission = models.ForeignKey(Admission, related_name='Obs_Gyn')
    name = models.CharField(max_length=200)
    examination = models.TextField()
    diagnosis = models.TextField()
    slug = models.SlugField(max_length=200)

    def save(self, *args, **kwargs):
        super(Obstetrics, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('TabibuNet:ob-detail', args=[self.admission.admission_date.year,
                                                       self.admission.admission_date.strftime('%m'),
                                                       self.admission.admission_date.strftime('%d'),
                                                       self.slug])


class ObstetricsImage(models.Model):
    medical_test = models.ForeignKey(Obstetrics, related_name='obstetric_images')
    image = models.ImageField()