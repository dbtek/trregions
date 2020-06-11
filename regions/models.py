from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=100)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.title


class District(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    city = models.ForeignKey(City, verbose_name=_('City'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

    def __str__(self):
        return self.title


class Neighborhood(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    district = models.ForeignKey(District, verbose_name=_('District'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Neighborhood')
        verbose_name_plural = _('Neighborhoods')

    def __str__(self):
        return self.title


