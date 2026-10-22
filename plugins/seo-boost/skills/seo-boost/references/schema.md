# JSON-LD templates

Put one block in `<head>` (or anywhere in the page). Fill only fields that are true and visible on the page. Remove fields you can't fill rather than inventing values. Validate at validator.schema.org; check rich-result eligibility with Google's Rich Results Test.

Pick by page type: blog post / guide → **Article**; product page → **Product**; shop, clinic, restaurant, office → **LocalBusiness** (or a more specific type: `Restaurant`, `CafeOrCoffeeShop`, `Dentist`, `Store`…); homepage → **Organization** + **WebSite**; any page with a breadcrumb trail → add **BreadcrumbList**.

## Article
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Make Cold Brew Coffee at Home",
  "description": "Ratio, grind and timing for smooth cold brew.",
  "image": ["https://example.com/images/cold-brew-1200x630.jpg"],
  "datePublished": "2026-10-01",
  "dateModified": "2026-10-20",
  "inLanguage": "en",
  "author": { "@type": "Person", "name": "Author Name", "url": "https://example.com/about" },
  "publisher": { "@type": "Organization", "name": "Brand", "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" } },
  "mainEntityOfPage": "https://example.com/cold-brew-coffee"
}
</script>
```
Arabic page: `"inLanguage": "ar"`.

## Product
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Ethiopian Yirgacheffe Coffee Beans 250g",
  "image": ["https://example.com/images/yirgacheffe.jpg"],
  "description": "Light roast, floral and citrus notes.",
  "sku": "ETH-250",
  "brand": { "@type": "Brand", "name": "Brand" },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/products/yirgacheffe",
    "priceCurrency": "SAR",
    "price": "79.00",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```
Add `aggregateRating` / `review` only if real reviews are shown on the page.

## LocalBusiness
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CafeOrCoffeeShop",
  "name": "Brand Coffee",
  "image": "https://example.com/storefront.jpg",
  "url": "https://example.com",
  "telephone": "+966-5X-XXX-XXXX",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "King Fahd Rd",
    "addressLocality": "Riyadh",
    "addressCountry": "SA"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 24.7136, "longitude": 46.6753 },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday"],
    "opens": "07:00", "closes": "23:00"
  }]
}
</script>
```
For local businesses, the Google Business Profile matters more for map results than schema — mention it.

## Organization + WebSite (homepage)
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://example.com/#org", "name": "Brand", "url": "https://example.com",
      "logo": "https://example.com/logo.png",
      "sameAs": ["https://instagram.com/brand", "https://x.com/brand", "https://www.linkedin.com/company/brand"] },
    { "@type": "WebSite", "@id": "https://example.com/#website", "url": "https://example.com", "name": "Brand",
      "publisher": { "@id": "https://example.com/#org" }, "inLanguage": "ar" }
  ]
}
</script>
```

## BreadcrumbList
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Guides", "item": "https://example.com/guides" },
    { "@type": "ListItem", "position": 3, "name": "Cold Brew Coffee" }
  ]
}
</script>
```

## FAQPage
Valid markup, but Google now shows FAQ rich results mainly for well-known government and health sites. Use it when the page really has a visible FAQ section; don't promise a rich result.
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How long does cold brew last?",
    "acceptedAnswer": { "@type": "Answer", "text": "Up to 7 days in the fridge, sealed." }
  }]
}
</script>
```
