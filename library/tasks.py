from celery import shared_task
from .models import Loan
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=now().date())

    for loan in overdue_loans:
        member_email = loan.member.user.email
        book_title = loan.book.title
        username = loan.member.user.username
        due_date = loan.due_date
        send_mail(
            subject="Overdue Book Reminder",
            message=(f"Dear {username}, \n\n"
                     f"The book {book_title} was due on {due_date}"
                     f"Please return it as soon as possible."
                     ),
            from_email="noreply@libary.com",
            recipient_list=[member_email],
            fail_silently=True,
        )