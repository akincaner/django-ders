from django.contrib import admin
from modules.portstatus.models import swtable, swporttable, documents


class Portview(admin.ModelAdmin):
    list_display = ('swtabledata', 'port', 'speed', 'status', 'mac')
    # ekranda görünecek alanları belirler: default bir değerde var
    list_display_links = ('swtabledata', 'port',)
    # tıklanabilir alanları belirler, defaultta ilki gelir
    list_filter = ('status',)
    # filtreleneilcek alan belirlenir. virgül önemli
    search_fields = ('mac',)
    # arama butonu oluştur. Hangi değerler içinde arayaccağını seç
    # list_editable = ('durum','toplam_tutar',)
    # içine girmeden direkt dışırdan editlenebilir olanları belirliyor


admin.site.register(swtable)
admin.site.register(swporttable, Portview)
admin.site.register(documents)
