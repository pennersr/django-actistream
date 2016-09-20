from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import TemplateDoesNotExist

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from .utils import import_attribute


class DefaultAdapter(object):

    def __init__(self, request=None):
        self.request = request

    def get_current_site(self):
        if self.request:
            site = get_current_site(self.request)
        elif ('django.contrib.sites' in settings.INSTALLED_APPS and
              settings.SITE_ID):
            from django.contrib.sites.models import Site
            site = Site.objects.get_current()
        else:
            site = None
        return site

    def format_email_subject(self, subject):
        prefix = getattr(settings, 'ACTISTREAM_EMAIL_SUBJECT_PREFIX', None)
        if prefix is None:
            site = self.get_current_site()
            if site:
                prefix = "[{name}] ".format(name=site.name)
            else:
                prefix = ''
        return prefix + force_text(subject)

    def format_email_body(self, body, ext):
        return body

    def get_from_email(self):
        """
        This is a hook that can be overridden to programatically
        set the 'from' email address for sending emails
        """
        return settings.DEFAULT_FROM_EMAIL

    def render_mail(self, template_prefix, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        context = dict(context)
        context['site'] = self.get_current_site()
        subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                                   context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ['html', 'txt']:
            try:
                template_name = '{0}_message.{1}'.format(template_prefix, ext)
                bodies[ext] = self.format_email_body(
                    render_to_string(template_name, context).strip(),
                    ext)
            except TemplateDoesNotExist:
                if ext == 'txt' and not bodies:
                    # We need at least one body
                    raise
        if 'txt' in bodies:
            msg = EmailMultiAlternatives(subject,
                                         bodies['txt'],
                                         from_email,
                                         [email])
            if 'html' in bodies:
                msg.attach_alternative(bodies['html'], 'text/html')
        else:
            msg = EmailMessage(subject,
                               bodies['html'],
                               from_email,
                               [email])
            msg.content_subtype = 'html'  # Main content is now text/html
        return msg

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        msg.send()


def get_adapter(request=None):
    path = getattr(
        settings, 'ACTISTREAM_ADAPTER', 'actistream.adapter.DefaultAdapter')
    return import_attribute(path)(request)
