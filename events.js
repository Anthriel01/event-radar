/* ÖRNEK VERİ: sayfayı ve filtreleri denemek için.
   Gerçek veriyle merge.py bu dosyanın üzerine yazacak.
   Biçim sabit kalmalı: window.EVENTS_META ve window.EVENTS.
   Tarihler bugüne göre hesaplanır, örnek kayıtlar hep "yaklaşan" görünür. */
(function () {
  function d(n) {
    var x = new Date();
    x.setDate(x.getDate() + n);
    return x.getFullYear() + '-' + String(x.getMonth() + 1).padStart(2, '0') + '-' + String(x.getDate()).padStart(2, '0');
  }

  window.EVENTS_META = { guncelleme: d(0), ornek: true };

  window.EVENTS = [
    { tur: 'etkinlik', ad: '[ÖRNEK] Siber Güvenlik Farkındalık Semineri', tarih: d(6), tarih_bitis: null,
      yer: 'İzmir', aciklama: 'Örnek kayıt: temel siber güvenlik farkındalığı, katılım sertifikalı yüz yüze seminer.',
      link: 'https://example.com/siber-seminer', kaynak: 'ornek.example',
      bolge: 'yakin', ucret: 'ucretsiz', sertifika: 'var', format: 'yuzyuze', kategori: 'siber', dogrulanmadi: false },

    { tur: 'etkinlik', ad: '[ÖRNEK] Yapay Zeka Buluşması', tarih: d(12), tarih_bitis: null,
      yer: 'Manisa', aciklama: 'Örnek kayıt: yapay zeka uygulamaları üzerine hibrit buluşma.',
      link: 'https://example.com/ai-bulusma', kaynak: 'ornek.example',
      bolge: 'yakin', ucret: 'ucretsiz', sertifika: 'yok', format: 'hibrit', kategori: 'yapay-zeka', dogrulanmadi: false },

    { tur: 'etkinlik', ad: '[ÖRNEK] Yazılım Geliştirici Zirvesi', tarih: d(25), tarih_bitis: d(26),
      yer: 'İstanbul', aciklama: 'Örnek kayıt: iki günlük, ücretli yüz yüze yazılım konferansı.',
      link: 'https://example.com/zirve', kaynak: 'ornek.example',
      bolge: 'turkiye', ucret: 'ucretli', sertifika: 'yok', format: 'yuzyuze', kategori: 'diger', dogrulanmadi: false },

    { tur: 'etkinlik', ad: '[ÖRNEK] Global AI Online Workshop', tarih: d(18), tarih_bitis: null,
      yer: null, aciklama: 'Örnek kayıt: ücretsiz, sertifikalı, online yapay zeka atölyesi.',
      link: 'https://example.com/ai-workshop', kaynak: 'ornek.example',
      bolge: 'global', ucret: 'ucretsiz', sertifika: 'var', format: 'online', kategori: 'yapay-zeka', dogrulanmadi: false },

    { tur: 'etkinlik', ad: '[ÖRNEK] Uluslararası Siber Konferans', tarih: d(40), tarih_bitis: null,
      yer: null, aciklama: 'Örnek kayıt: ücretli online konferans. Bilgileri doğrulanmamış olarak işaretli.',
      link: 'https://example.com/siber-konf', kaynak: 'ornek.example',
      bolge: 'global', ucret: 'ucretli', sertifika: 'var', format: 'online', kategori: 'siber', dogrulanmadi: true },

    { tur: 'etkinlik', ad: '[ÖRNEK] Girişimcilik Hafta Sonu Kampı', tarih: d(-1), tarih_bitis: d(3),
      yer: 'İzmir', aciklama: 'Örnek kayıt: şu an devam eden bir etkinlik (bitiş tarihi gelecekte).',
      link: 'https://example.com/kamp', kaynak: 'ornek.example',
      bolge: 'yakin', ucret: 'ucretsiz', sertifika: 'bilinmiyor', format: 'yuzyuze', kategori: 'diger', dogrulanmadi: false },

    { tur: 'egitim', ad: '[ÖRNEK] Temel Siber Güvenlik Eğitimi', tarih: null, tarih_bitis: null,
      yer: null, aciklama: 'Örnek kayıt: kendi hızında ilerlenen, sertifikalı, ücretsiz online eğitim.',
      link: 'https://example.com/siber-egitim', kaynak: 'ornek.example',
      bolge: 'turkiye', ucret: 'ucretsiz', sertifika: 'var', format: 'online', kategori: 'siber', dogrulanmadi: false },

    { tur: 'egitim', ad: '[ÖRNEK] Yapay Zekaya Giriş', tarih: null, tarih_bitis: null,
      yer: null, aciklama: 'Örnek kayıt: yapay zeka temelleri, sürekli açık online eğitim.',
      link: 'https://example.com/ai-giris', kaynak: 'ornek.example',
      bolge: 'turkiye', ucret: 'ucretsiz', sertifika: 'var', format: 'online', kategori: 'yapay-zeka', dogrulanmadi: false },

    { tur: 'egitim', ad: '[ÖRNEK] Belediye Kodlama Kursu', tarih: null, tarih_bitis: null,
      yer: 'Manisa', aciklama: 'Örnek kayıt: yerel, ücretsiz, hibrit kodlama kursu.',
      link: 'https://example.com/kodlama-kursu', kaynak: 'ornek.example',
      bolge: 'yakin', ucret: 'ucretsiz', sertifika: 'yok', format: 'hibrit', kategori: 'diger', dogrulanmadi: false },

    /* Bilerek linksiz: sayfada GÖRÜNMEMELİ, altta "1 kayıt gizlendi" notu çıkmalı */
    { tur: 'etkinlik', ad: '[ÖRNEK] Linksiz Kayıt', tarih: d(9), tarih_bitis: null,
      yer: 'İzmir', aciklama: 'Bu kayıt linki olmadığı için gösterilmemeli.',
      link: null, kaynak: null,
      bolge: 'yakin', ucret: 'ucretsiz', sertifika: 'yok', format: 'yuzyuze', kategori: 'diger', dogrulanmadi: true }
  ];
})();
