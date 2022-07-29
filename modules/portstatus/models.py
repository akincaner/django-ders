from django.db import models


class swtable(models.Model):
    sw_name = models.CharField(max_length=30, verbose_name='Switch Name')

    class Meta:
        verbose_name = 'Switch List'
        verbose_name_plural = 'Switch Lists'

    def __str__(self):
        return str(self.sw_name)


class swporttable(models.Model):
    swtabledata = models.ForeignKey(swtable, verbose_name="Switch List", related_name="swdata",
                                    on_delete=models.DO_NOTHING)
    port = models.CharField(max_length=30, verbose_name='Switch Port')
    speed = models.CharField(max_length=10, verbose_name='Port Speed')
    status = models.CharField(max_length=10, verbose_name='Status')
    mac = models.CharField(max_length=30, verbose_name='MAC')

    class Meta:
        verbose_name = 'Switch Port List'
        verbose_name_plural = 'Switch Port Lists'


class documents(models.Model):
    document = models.FileField(verbose_name="Döküman", upload_to="uploads/")
    description = models.TextField(verbose_name="Açıklama", null=True, blank=True)

    class Meta:
        verbose_name = 'Döküman'
        verbose_name_plural = 'Dökümanlar'
