from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=255)
    mobile = PhoneNumberField()

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(str(self.mobile), self.full_name)

    def report_spam(self, reporter):
        spam, created = Spam.objects.get_or_create(reported_by=reporter, spammer=self)
        if created:
            return
        else:
            raise ValueError('Already reported')

    @property
    def spam_count(self):
        return Spam.objects.filter(spammer=self).count


class Spam(models.Model):
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='who_reported')
    spammer = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='spammer')

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(str(self.reported_by), str(self.spammer))

    def check_self(self, *args, **kwargs):
        if self.reported_by == self.spammer.owner:
            raise ValueError('Forbidden')
    
    def save(self, *args, **kwargs):
        self.check_self()
        super(Spam, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['reported_by', 'spammer']
