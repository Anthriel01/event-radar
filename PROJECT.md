# Etkinlik Radarı

## Amaç
İzmir/Manisa, Türkiye ve global; yaklaşan etkinlikleri, ücretsiz
eğitimleri ve sertifika fırsatlarını tek sayfada filtreleyerek
gösteren "fırsat radarı". Dil: Türkçe.

## Kayıt türleri
- etkinlik: tarihli. Bugünden itibaren en fazla 90 gün sonrası.
- egitim: sürekli açık (BTK Akademi, İŞKUR, vb.), tarih yok.

## Alanlar (events.json)
tur, ad, tarih, tarih_bitis, yer, aciklama, link, kaynak,
bolge (yakin|turkiye|global), ucret (ucretli|ucretsiz|bilinmiyor),
sertifika (var|yok|bilinmiyor), format (online|yuzyuze|hibrit),
kategori (siber|yapay-zeka|diger), dogrulanmadi (true|false)

## Filtreler (sayfada)
Konum · Ücret · Sertifika · Online/Yüzyüze · Kategori

## Mimari
- Öncelikli alanlar: siber güvenlik, yapay zeka. "diger" kategorisi ikinci planda.
- index.html sabit şablon, değişmez. events.js'den okur.
- Veri güncellemesi: merge.py (LLM yok).
- Linki olmayan kayıt sayfada gösterilmez.