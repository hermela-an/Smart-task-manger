from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends email reminders for tasks due tomorrow'

    def handle(self, *args, **options):
        tomorrow = timezone.now().date() + timedelta(days=1)
        tasks_due = Task.objects.filter(due_date=tomorrow).exclude(status='completed')
        
        if not tasks_due.exists():
            self.stdout.write(self.style.SUCCESS('No tasks due tomorrow. No emails sent.'))
            return

        user_tasks = {}
        for task in tasks_due:
            if task.owner not in user_tasks:
                user_tasks[task.owner] = []
            user_tasks[task.owner].append(task)

        for user, tasks in user_tasks.items():
            if not user.email:
                self.stdout.write(self.style.WARNING(f'User {user.username} has no email set. Skipping.'))
                continue

            subject = 'Reminder: You have tasks due tomorrow!'
            message = f"Hello {user.username},\n\nYou have {len(tasks)} task(s) due tomorrow ({tomorrow}):\n\n"
            for task in tasks:
                message += f"- {task.title} (Priority: {task.priority.capitalize()})\n"
            message += "\nGood luck with your work!\n- Smart Task Manager Team"
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                self.stdout.write(self.style.SUCCESS(f'Successfully sent reminder to {user.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to send email to {user.email}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Finished sending reminders.'))
