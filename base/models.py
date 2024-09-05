# importing necessary django classes
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import Group, Permission

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('user', 'User'),
)


class customUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    first_name = models.CharField('First Name of User', blank=True, max_length=20)
    last_name = models.CharField('Last Name of User', blank=True, max_length=20)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Assign the user to the appropriate group based on their role
        self.assign_group_based_on_role()

    def assign_group_based_on_role(self):
        role_to_group_mapping = {
            'admin': 'AdminGroup',
            'manager': 'ManagerGroup',
            'user': 'UserGroup',
        }

        group_name = role_to_group_mapping.get(self.role)
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            self.groups.clear()  # Clear previous groups
            self.groups.add(group)

    def __str__(self):
        return f'{self.username} ({self.role})'




class Transaction(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.user.username} - {self.amount}"




