from django.db import models

tipList = (
    ('internal', 'Internal'),
    ('external', 'External')
)

domainList = (
    ('mobil', 'Mobil'),
    ('fixed', 'Fixed'),
    ('broadband', 'Broad Band')
)


class dc(models.Model):
    name = models.CharField(max_length=20, verbose_name="Dc Adı")
    location = models.CharField(max_length=25, verbose_name="Lokasyon")
    tip = models.CharField(max_length=15, choices=tipList, verbose_name="Tipi")
    domain = models.CharField(max_length=15, choices=domainList, verbose_name="Domain")

    class Meta:
        verbose_name = "Veri Merkezi"
        verbose_name_plural = "Veri Merkezleri"

    def __str__(self):
        return self.name



