# Kurallar
Önce PROJECT.md'yi oku. Web araması YAPMA. Tek istisna: /site skill'i kendi kurallarıyla web'e bakabilir.
research/ham çıktı dosyalarını okuma, sadece istenen dosyayı aç.
Veri uydurma; link/tarih yoksa alanı null bırak.
index.html'i yalnızca açıkça istenirse değiştir.
Küçük commit at. Yanıtların kısa olsun.

## Python
- Python betiklerini `uv run <betik>.py` ile çalıştır; `python` komutunu kullanma.

## Git
- Her anlamlı adımdan sonra küçük commit at. Mesaj Türkçe, tek satır,
  ne yapıldığını söylesin (örn. "Açıklama çekme betiği eklendi").
- Commit'ten önce git status bak. Çerez/token dosyaları, .env ve
  .cache/ asla eklenmesin. `git add .` yerine ilgili dosyaları ekle.
- Commit'ten sonra `git push origin main` çalıştır. Hata verirse DUR
  ve bildir; force push veya reset --hard YAPMA.
- Bir şey bozulursa üstüne yama yapma, git revert ile geri dön.