from django.contrib import admin

from modules.orders.models import siparis,urunler


class urunInline(admin.StackedInline):
    model = urunler
    extra = 0


class SiparisAdmin(admin.ModelAdmin):
    list_display = ('siparis_kodu', 'toplam_tutar', 'durum', 'siparis_tarihi')
    list_display_links = ('siparis_kodu',)
    list_filter = ('durum',)
    search_fields = ('siparis_kodu', 'toplam_tutar')
    list_editable = ('durum', 'toplam_tutar',)
    inlines = [urunInline]


admin.site.register(siparis, SiparisAdmin)
