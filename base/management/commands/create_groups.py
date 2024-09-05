from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create default groups and assign permissions for all models'

    def handle(self, *args, **kwargs):
        groups_permissions = {
            'AdminGroup': ['add', 'change', 'delete', 'view'],
            'ManagerGroup': ['change', 'view','add'],
            'UserGroup': ['view'],
        }

        for group_name, actions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group {group_name} already exists'))
            
            group.permissions.clear()
            
            for content_type in ContentType.objects.all():
                for action in actions:
                    codename = f'{action}_{content_type.model}'
                    try:
                        permission = Permission.objects.get(
                            codename=codename, 
                            content_type=content_type
                        )
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f'Permission {codename} does not exist for model {content_type.model}'
                        ))

            self.stdout.write(self.style.SUCCESS(f'Assigned permissions to group {group_name}'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been set up.'))
