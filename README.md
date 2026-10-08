# Etkinlik Radarı

İzmir, Manisa ve Türkiye genelindeki siber güvenlik ve yapay zeka etkinliklerini ile sürekli açık ücretsiz eğitimleri tek sayfada listeleyen, kendi kendine güncellenen statik bir sayfa.

## Ne işe yarar?

- **Etkinlikler:** Önümüzdeki 90 gün içinde gerçekleşecek seminer, konferans ve buluşmalar.
- **Sürekli eğitimler:** Tarihi olmayan, istediğin zaman başlayabileceğin kurs ve programlar (BTK Akademi, IBM SkillsBuild, Google gibi).
- **Filtreler:** Konum, ücret, sertifika, format (online / yüz yüze / hibrit) ve alan (siber, yapay zeka, diğer).

Sayfa tamamen statiktir. Sunucu, veritabanı ya da API gerektirmez. Veriler `events.js` dosyasında tutulur.

## Veri nereden geliyor?

| Kaynak | Ne sağlar | Script |
|---|---|---|
| [confs.tech](https://github.com/tech-conferences/conference-data) (MIT lisanslı) | Küresel konferanslar | `fetch_confs.py` |
| NotebookLM (kendi araştırma defterim) | İzmir/Manisa, Türkiye geneli ve sürekli eğitimler | `fetch_notebooklm.py` |
| Etkinlik sayfalarının kendisi | Kısa açıklama (`og:description`) | `enrich_descriptions.py` |

## Kurallar

- **Uydurma veri yok.** Kaynakta yazmayan bilgi `null` veya `bilinmiyor` olarak kalır.
- **Link zorunlu.** Geçerli `http`/`https` linki olmayan kayıtlar gösterilmez.
- **Geçmiş etkinlik gösterilmez.** Bitiş tarihi (ya da başlangıç tarihi) geçmiş olanlar atılır.
- **Doğrulanmamış kayıtlar işaretlenir.** Link, kaynağın kendi alan adında değilse `dogrulanmadi: true` olur ve kartta belirtilir.
- **`index.html` sabittir.** Veri değişir, sayfanın kodu değişmez.

## Kurulum

Gereksinimler:
- Windows, PowerShell
- [uv](https://docs.astral.sh/uv/) (`winget install astral-sh.uv`)
- Git ve GitHub hesabı
- NotebookLM için Google hesabı ve `notebooklm-py` paketi

NotebookLM girişi (Windows'ta Firefox çerezleriyle):

```powershell
uv tool install --force --python 3.12 "notebooklm-py[browser,cookies]"
notebooklm login --browser-cookies firefox
notebooklm auth check --test
```

Kimlik bilgileri (`storage_state.json`, `master_token.json`) proje klasörünün dışında, `C:\Users\<kullanıcı>\.notebooklm\` içinde tutulur. Bunlar **parola niteliğindedir**, asla commit edilmez. `.gitignore` bunları zaten dışarıda bırakır.

## Kullanım

Tüm güncellemeyi tek komutla çalıştır:

```powershell
uv run update.py
```

Bu komut sırayla şunları yapar:
1. `fetch_confs.py`: confs.tech verisini indirir ve son 90 güne göre süzer.
2. `fetch_notebooklm.py`: `sorgu.txt` şablonundaki tarihleri doldurur, NotebookLM'e sorar, sonucu `data/tr.json` dosyasına yazar.
3. `enrich_descriptions.py`: linklerden kısa açıklamaları çeker.
4. `merge.py`: tüm `data/*.json` dosyalarını birleştirip `events.js` üretir.
5. Git: değişiklik varsa `events.js` ve `data/` dosyalarını commit'leyip `origin main`e gönderir.

Bayraklar:

| Bayrak | Ne yapar |
|---|---|
| `--no-nlm` | NotebookLM adımını atlar, eski `data/tr.json` kalır |
| `--no-git` | Commit ve push yapmaz |

NotebookLM girişi süresi dolduysa adım uyarı verir ve eski veriyle devam eder. Site bozulmaz.

## Dosya yapısı

```
etkinlik-radari/
├── index.html                  # Sayfa (sabit, değiştirilmez)
├── events.js                   # Sayfanın okuduğu veri (üretilir)
├── data/
│   ├── confs.json              # confs.tech'ten (üretilir)
│   └── tr.json                 # NotebookLM'den (üretilir)
├── fetch_confs.py
├── fetch_notebooklm.py
├── enrich_descriptions.py
├── merge.py
├── update.py
├── sorgu.txt                   # NotebookLM'e giden sorgu şablonu
├── PROJECT.md                  # Proje kuralları ve veri şeması
├── CLAUDE.md                   # Claude Code için çalışma kuralları
└── .claude/skills/site/        # /site bilgi kartı komutu
```

`.cache/` klasörü geçici dosyaları tutar ve git'e girmez.

## Veri şeması

Her kayıt şu alanlara sahiptir:

| Alan | Değerler |
|---|---|
| `tur` | `etkinlik` veya `egitim` |
| `ad`, `link`, `kaynak` | Metin, link zorunlu |
| `tarih`, `tarih_bitis` | `YYYY-MM-DD` veya `null` |
| `yer`, `aciklama` | Metin veya `null` |
| `bolge` | `yakin` (İzmir/Manisa), `turkiye`, `global` |
| `ucret` | `ucretli`, `ucretsiz`, `bilinmiyor` |
| `sertifika` | `var`, `yok`, `bilinmiyor` |
| `format` | `online`, `yuzyuze`, `hibrit`, `bilinmiyor` |
| `kategori` | `siber`, `yapay-zeka`, `diger` |
| `dogrulanmadi` | `true` / `false` |

## Bilinen sınırlamalar

- NotebookLM'in kullandığı Google API'leri resmi değildir. Google bir değişiklik yaparsa `notebooklm-py` güncellenmek zorunda kalabilir.
- Çerez süresi dolunca `notebooklm login --browser-cookies firefox` komutunu yeniden çalıştırmak gerekir.
- Bazı etkinlik sayfaları bot engeli nedeniyle açıklama çekilemez (ör. 403). Bu kayıtlar açıklamasız görünür.
- Yabancı dildeki açıklamalar henüz Türkçeye çevrilmiyor.
- Ücret ve sertifika bilgisi kaynakta yoksa `bilinmiyor` olarak kalır. Bu bilerek böyledir.

## Yol haritası

- [ ] Haftalık otomatik çalıştırma (Windows Görev Zamanlayıcı)
- [ ] GitHub Pages ile yayın
- [ ] Yabancı açıklamaların çevirisi (toplu ve önbellekli)
- [ ] Luma iCal kaynakları

## Lisans ve teşekkür

- Küresel konferans verisi: [tech-conferences/conference-data](https://github.com/tech-conferences/conference-data), MIT lisansı.
- NotebookLM erişimi: [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py), resmi olmayan istemci.