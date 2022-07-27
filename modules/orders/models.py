from django.db import models


class siparis(models.Model):
    siparis_kodu = models.CharField(max_length=9, verbose_name="Sipariş Kodu")
    siparis_tarihi = models.DateTimeField(verbose_name="Sipariş Tarihi", auto_now=True)
    durum = models.BooleanField(verbose_name="Durumu", default=True)
    toplam_tutar = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Toplam Tutar")

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"

    def __str__(self):
        return self.siparis_tarihi.strftime("%d/%m/%Y %H:%M")


class urunler(models.Model):
    urun_adi = models.CharField(max_length=100, verbose_name="Ürün Adı")
    urun_aciklamasi = models.TextField(verbose_name="Ürün Açıklması", blank=True)
    stok_sayisi = models.IntegerField(verbose_name="Toplam Stok")
    fiyat = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ürün Fiyatı")
    siparis_urunu = models.ForeignKey(siparis, verbose_name="Sipariş Ürünü", related_name="siparisUrunler",
                                      on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return self.urun_adi


