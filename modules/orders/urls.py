from django.urls import path

from modules.orders.views import index, detail, getByKategori, getByKategoriId

# http://127.0.0.1:8000/orders/
# http://127.0.0.1:8000/orders/kategori/eşya  => eşya
# http://127.0.0.1:8000/orders/kategori/ayakkabı  => ayakkabı
# http://127.0.0.1:8000/orders/urun/marka/model/1


urlpatterns = [
    path('', index, name="index"),
    path('detail/', detail),
    # path('kategori/<category>/', getByKategori),
    path('kategori/<int:category>', getByKategoriId, name="products_by_kategori_id"),
    path('kategori/<str:category>', getByKategori, name="products_by_kategori"),
]
