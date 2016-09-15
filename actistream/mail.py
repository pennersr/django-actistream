from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.safestring import mark_safe


def render_and_send_mail(template_prefix, recipient_list,
                         from_email=settings.CONTACT_EMAIL,
                         context={}):
    def format_subject(s):
        return s.replace('\n', ' ').strip()

    def format_body(s):
        return s.strip()

    site = Site.objects.get_current()
    subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                               context)
    body = render_to_string('{0}_message.txt'.format(template_prefix),
                            context)
    subject = format_subject(subject)
    subject = format_subject(render_to_string(
        'actistream/mail_subject.txt',
        {'site': site,
         'subject': mark_safe(subject)}))
    body = format_body(
        render_to_string
        ('actistream/mail_message.txt',
         {'site': site,
          'body': mark_safe(format_body(body))}))
    email = EmailMessage(subject,
                         body,
                         from_email,
                         recipient_list)
    email.send(fail_silently=False)
