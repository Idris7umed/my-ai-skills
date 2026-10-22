# Arabic SEO

## How Arabic users search

- **Spelling variants are separate searches.** People type قهوة and قهوه, أفضل and افضل, مستشفى and مستشفي. Google normalizes many of these, but not always. Use the correct spelling in the title and H1; the audit script already treats variants as the same keyword when scoring.
- **Dialect vs. MSA.** The same need is searched in different words: جوال / موبايل / هاتف, سيارة / عربية (Egypt), تكييف / مكيف, شقق للإيجار / شقق ايجار. Ask yourself what *this* audience types. If a search tool is available, check which form returns pages like this one. Put the most-searched form in the title and use the others naturally in the body and H2s. Pass them all to the script: `-k "جوال|موبايل"`.
- **English and Arabizi alongside Arabic.** Many Gulf users search brand and product names in English ("iphone 16 سعر", "best cafe riyadh"). Mixed-language titles are fine when that's how people search: `سعر iPhone 16 في السعودية — مقارنة المتاجر`.
- **Local intent.** Add the city or country when the business is local: `قهوة مختصة في الرياض`, `محامي في جدة`. Arabic searches are often local.

## Titles and descriptions

- Aim for 30–60 characters, like English. Arabic letters are narrower on screen, so an Arabic title near 60 characters usually still fits.
- Put the keyword first: `قهوة مختصة في الرياض | اسم المتجر` rather than `اسم المتجر - نبيع قهوة مختصة`.
- Use the Arabic separators naturally: `|` or `—` work in both directions. Avoid starting a title with a Latin word followed by punctuation, which can display in the wrong order.
- Meta description: 70–160 characters, ending with a call to action: `اطلب الحين`, `تصفح القائمة`, `احجز موعدك`.

## Technical

- `<html lang="ar" dir="rtl">` on every Arabic page. Wrong `dir` breaks layout and can confuse language detection.
- **Bilingual sites:** separate URLs per language (`/ar/…` and `/en/…`), each with its own title, description and content. Never show both languages on one URL by toggling with JavaScript. Link them with hreflang on both pages:
  ```html
  <link rel="alternate" hreflang="ar" href="https://example.com/ar/coffee">
  <link rel="alternate" hreflang="en" href="https://example.com/en/coffee">
  <link rel="alternate" hreflang="x-default" href="https://example.com/en/coffee">
  ```
  Use `ar-SA`, `ar-EG`, etc. only if the content really differs by country.
- **Slugs:** Arabic slugs work, and Google displays them decoded. However, when copied and shared they become long `%D8%A7…` strings. A short Latin transliteration (`/qahwa-mukhtasa` or `/specialty-coffee`) shares more cleanly. Pick one style per site and keep it consistent. Changing live URLs needs 301 redirects.
- **Numbers:** keep one style per page, either Western (1, 2, 3) or Arabic-Indic (١، ٢، ٣). Western numerals are more common in Gulf searches for prices and models.

## Content

- Write in the dialect register your audience uses for headings and calls to action, but keep body text clear enough for MSA readers if the market is pan-Arab.
- Arabic sentences often chain clauses with و. Split long sentences; the audit flags an average above ~30 words.
- Answer the questions people actually ask in your market: price in local currency (ريال، درهم، جنيه), delivery areas, working hours, payment methods (مدى، Apple Pay، تمارا/تابي when true).
