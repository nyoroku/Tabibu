from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from datetime import datetime, date
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_fsm import transition, FSMIntegerField
from django_fsm_log.decorators import fsm_log_by
from django_fsm.signals import post_transition, pre_transition
from django.contrib import messages
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_nurse = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    is_pharmacy = models.BooleanField(default=False)
    is_dental = models.BooleanField(default=False)


class Insurance(models.Model):
    company = models.CharField(max_length=100)
    description = models.TextField()
    added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.company


class Patient(models.Model):
    GENDER = (
        ('male', 'MALE'),
        ('female', 'FEMALE'),

    )
    MARRIED = (
        ('no', 'NO'),
        ('yes', 'YES'),

    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = ProcessedImageField(upload_to='patients', processors=[ResizeToFill(200, 150)],
                                format='JPEG',
                                options={'quality': 100}, blank=True)
    phone = PhoneNumberField()
    email = models.EmailField()
    gender = models.CharField(choices=GENDER, default='female', max_length=20)
    address = models.CharField(max_length=100)
    contact_person = PhoneNumberField()
    location = models.CharField(max_length=100)
    dob = models.DateField()
    insurance = models.ForeignKey(Insurance, related_name='patient')
    married = models.CharField(choices=MARRIED, default='no', max_length=20)
    slug = models.SlugField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)

    def age(self):
        days_in_year = 365.2425
        age = int((date.today() - self.dob).days / days_in_year)
        return age


    def get_absolute_url(self):
        return reverse('TabibuNet:patient-detail', args=[self.added.year,
                                                 self.added.strftime('%m'),
                                                 self.added.strftime('%d'),
                                                 self.slug])

    class Meta:
        ordering = ('-added',)

    def save(self, *args, **kwargs):
        super(Patient, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.first_name) + "-" + str(self.id)
            self.save()

    def __str__(self):
        return str(self.id)


class MedicalInfo(models.Model):
    BLOOD = (
     ('A+', 'A+ Type'),
     ('B+', 'B+ Type'),
     ('AB+', 'AB+ Type'),
     ('O+', 'O+ Type'),
     ('A-', 'A- Type'),
     ('B-', 'B- Type'),
     ('AB-', 'AB- Type'),
     ('O-', 'O- Type'),
       )

    patient = models.OneToOneField(Patient, related_name='medical_info', on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=10, choices=BLOOD)
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    allergy = models.CharField(max_length=100)
    alzheimer = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    stroke = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    height = models.DecimalField(blank=True, decimal_places=2, max_digits=5, default=0.00)
    weight = models.DecimalField(blank=True, decimal_places=2, max_digits=5, default=0.00)
    chronic_disease = models.CharField(max_length=200, default='No')
    drinker = models.BooleanField(default=False)
    smoker = models.BooleanField(default=False)

    @receiver(post_save, sender=Patient)
    def create_patient_info(sender, instance, created, **kwargs):
        if created:
            MedicalInfo.objects.create(patient=instance)

    @receiver(post_save, sender=Patient)
    def save_patient_info(sender, instance, **kwargs):
        instance.medical_info.save()

    def __str__(self):
        return 'MedicalInfo for patient {}'.format(self.patient.id)


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.user.first_name


class Visit(models.Model):
    RECEPTION = 1
    WAIT_FOR_PROVIDER = 2
    PROVIDER = 3
    WAIT_FOR_DENTAL = 4
    DENTAL = 5
    WAIT_FOR_LAB = 6
    LAB = 7
    WAIT_FOR_PHARMACY = 8
    PHARMACY = 9
    BILLING = 10
    READY_TO_CLOSE = 11
    CLOSED = 12

    STATUS = (
        (RECEPTION, 'Reception'),
        (WAIT_FOR_PROVIDER, 'Wait_for_provider'),
        (PROVIDER, 'Provider'),
        (WAIT_FOR_DENTAL, 'Wait_for_dental'),
        (DENTAL, 'Dental'),
        (WAIT_FOR_LAB, 'Waiting_for_lab'),
        (LAB, 'Lab'),
        (WAIT_FOR_PHARMACY, 'Wait_for_pharmacy'),
        (PHARMACY, 'Pharmacy'),
        (BILLING, 'Billing'),
        (READY_TO_CLOSE, 'Ready_to_close'),
        (CLOSED, 'Closed'),

    )

    patient = models.ForeignKey(Patient, related_name='visit')
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(null=True)
    status = FSMIntegerField(choices=STATUS, default=RECEPTION)
    chief_complaints = models.CharField(max_length=300)
    slug = models.SlugField(max_length=100)

    @fsm_log_by
    @transition(field=status, source=RECEPTION, target=WAIT_FOR_PROVIDER)
    def waiting_for_provider(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=RECEPTION, target=RECEPTION)
    def reception(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=WAIT_FOR_PROVIDER, target=PROVIDER)
    def provider(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=[RECEPTION, PROVIDER], target=WAIT_FOR_LAB)
    def send_to_lab(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=WAIT_FOR_LAB, target=LAB)
    def to_lab(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=LAB, target=WAIT_FOR_PROVIDER)
    def to_lab_provider(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=PROVIDER, target=WAIT_FOR_PHARMACY)
    def to_pharmacy(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=WAIT_FOR_PHARMACY, target=PHARMACY)
    def pharmacy(self, by=User):
        pass

    def save(self, *args, **kwargs):
        super(Visit, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(self.patient.first_name) + "-" + str(self.id)
            self.save()
        if self.status == 'closed' and self.finish_date is None:
            self.finish_date = datetime.now()
        elif self.finish_date is not None:
            self.finish_date = self.finish_date
        super(Visit, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('TabibuNet:visit-detail', args=[self.start_date.year,
                                                 self.start_date.strftime('%m'),
                                                 self.start_date.strftime('%d'),
                                                 self.slug])

    class Meta:
        ordering = ('-start_date',)

    def __str__(self):
        return str(self.id)


class Test(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Prescription(models.Model):
    undelivered = 1
    delivered = 2

    STATUS = (
        ('undelivered', 'UNDELIVERED'),
        ('delivered', 'DELIVERED'),


    )
    visit = models.OneToOneField(Visit, related_name='prescription')
    date = models.DateField(auto_now_add=True)
    status = FSMIntegerField(choices=STATUS, default=undelivered)

    def get_absolute_url(self):
        return reverse('TabibuNet:prescription', args=[self.visit.pk])

    @receiver(post_save, sender=Visit)
    def create_prescription(sender, instance, created, **kwargs):
        if created:
            Prescription.objects.create(visit=instance)

    @receiver(post_save, sender=Visit)
    def save_prescription(sender, instance, **kwargs):
        instance.prescription.save()

    @fsm_log_by
    @transition(field=status, source=undelivered, target=delivered)
    def pharmacy(self, by=User):
        pass


class Medication(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='medications')
    medication = models.CharField(max_length=100)
    strength = models.CharField(max_length=30)
    instruction = models.CharField(max_length=200)
    refill = models.IntegerField()
    active = models.BooleanField(default=True)


class MedicalTest(models.Model):
    visit = models.ForeignKey(Visit, related_name='medical_test')
    history = models.TextField(blank=True, default='History')
    examination = models.TextField()
    diagnosis = models.CharField(max_length=200)
    ddx = models.CharField(max_length=200)

    slug = models.SlugField(max_length=200)

    def save(self, *args, **kwargs):
        super(MedicalTest, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.visit.id) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('TabibuNet:test-detail', args=[self.visit.start_date.year,
                                                       self.visit.start_date.strftime('%m'),
                                                       self.visit.start_date.strftime('%d'),
                                                       self.slug])


class LabTest(models.Model):
    active = 1
    in_progress = 2
    sent_to_provider = 3
    sent_to_pharmacy = 4
    ready_to_close = 5

    STATUS = (
        ('active', 'ACTIVE'),
        ('in progress', 'IN PROGRESS'),
        ('sent_to_provider', 'SENT_TO_PROVIDER'),
        ('sent_to_pharmacy', 'SENT_TO_PHARMACY'),
        ('ready_close', 'READY_TO_CLOSE'),


    )
    status = FSMIntegerField(choices=STATUS, default=active)
    created = models.DateTimeField(default=datetime.now())
    medical_test = models.ForeignKey(Test, related_name='lab_test')
    visit = models.ForeignKey(Visit, related_name='lab_test')
    examination = models.TextField()
    diagnosis = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('-created',)

    def proceed_to_lab(self):
        if self.labbill.status == 1:
            return False
        return True

    @fsm_log_by
    @transition(field=status, source=active, target=in_progress, conditions=[proceed_to_lab])
    def lab(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=in_progress, target=sent_to_provider)
    def lab_to_provider(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=in_progress, target=sent_to_pharmacy)
    def lab_to_pharmacy(self, by=User):
        pass

    @fsm_log_by
    @transition(field=status, source=in_progress, target=ready_to_close)
    def ready_for_close(self, by=User):
        pass

    def save(self, *args, **kwargs):
        super(LabTest, self).save(*args, **kwargs)
        if self.visit.lab_test.filter(status=2).exists():
            self.visit.status = 7
            self.visit.save()
        if self.status == 3:
            self.visit.status = 2
            self.visit.save()

        if not self.slug:
            self.slug = slugify(self.medical_test) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('TabibuNet:labtest-detail', args=[self.visit.start_date.year,
                                                       self.visit.start_date.strftime('%m'),
                                                       self.visit.start_date.strftime('%d'),
                                                       self.slug])


class Obstetrics(models.Model):
    visit = models.ForeignKey(Visit, related_name='Obs_Gyn')
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
        return reverse('TabibuNet:ob-detail', args=[self.visit.start_date.year,
                                                       self.visit.start_date.strftime('%m'),
                                                       self.visit.start_date.strftime('%d'),
                                                       self.slug])


class ObstetricsImage(models.Model):
    medical_test = models.ForeignKey(Obstetrics, related_name='obstetric_images')
    image = models.ImageField()








