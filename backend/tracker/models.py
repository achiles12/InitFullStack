from django.db import models 
from django.contrib.auth.models import AbstractUser 
 
# Custom User Model 
class User(AbstractUser): 
   ROLE_CHOICES = [ 
      ('tenant', 'Tenant'),
      ('landlord', 'Landlord'), 
      ('handyman', 'Handyman'), 
      ('admin', 'Admin'), 
   ] 

   role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant') 
   phone = models.CharField(max_length=20, blank=True, null=True) 
   address = models.TextField(blank=True, null=True) 
 
   def __str__(self): 
      return f"{self.username} ({self.role})" 
 
 
class Property(models.Model): 
   landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties') 
   name = models.CharField(max_length=100) 
   address = models.TextField() 
   description = models.TextField(blank=True, null=True) 
 
   def __str__(self): 
      return self.name 
 
 
class MaintenanceIssue(models.Model): 
   STATUS_CHOICES = [ 
      ('pending', 'Pending'), 
      ('in_progress', 'In Progress'), 
      ('resolved', 'Resolved'), 
      ('closed', 'Closed'), 
   ] 
 
   property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='issues') 
   reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues') 
   title = models.CharField(max_length=100) 
   description = models.TextField() 
   photo = models.ImageField(upload_to='issues/', blank=True, null=True) 
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
   created_at = models.DateTimeField(auto_now_add=True) 
 
   def __str__(self): 
      return f"{self.title} ({self.status})" 
 
 
class RepairJob(models.Model): 
   issue = models.OneToOneField(MaintenanceIssue, on_delete=models.CASCADE, related_name='repair_job') 
   handyman = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='jobs') 
   scheduled_date = models.DateField(blank=True, null=True) 
   completed_date = models.DateField(blank=True, null=True) 
   notes = models.TextField(blank=True, null=True) 
   cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
 
   def __str__(self): 
      return f"Repair for {self.issue.title}" 
 
 
class Message(models.Model): 
   issue = models.ForeignKey(MaintenanceIssue, on_delete=models.CASCADE, related_name='messages') 
   sender = models.ForeignKey(User, on_delete=models.CASCADE) 
   content = models.TextField() 
   created_at = models.DateTimeField(auto_now_add=True) 
 
   def __str__(self): 
      return f"Message by {self.sender.username} on {self.issue.title}" 
