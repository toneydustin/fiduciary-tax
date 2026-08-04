#!/usr/bin/env python3
"""
build-blog.py — generates static blog post pages from blog/posts.json.

Workflow: edit blog/posts.json as before (add/edit posts), then run
`python3 build-blog.py` from the site root. One blog/<slug>.html page is
generated per post with full SEO meta and Article structured data.
Also regenerates sitemap.xml. Run before every deploy.
"""
import json
import re
import glob
from datetime import date
from html import escape

SITE = "https://fiduciary.tax"
ASSET_V = "?v=20260804"  # bump on each deploy to bust caches

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_esc} | FTAS</title>
  <meta name="description" content="{excerpt_esc}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title_esc}">
  <meta property="og:description" content="{excerpt_esc}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="Fiduciary Tax &amp; Accounting Services">
  <meta property="article:published_time" content="{iso_date}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{title_esc}">
  <meta name="twitter:description" content="{excerpt_esc}">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css{asset_v}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {title_json},
    "description": {excerpt_json},
    "datePublished": "{iso_date}",
    "author": {{"@type": "Person", "name": "Dustin C. Toney", "jobTitle": "Enrolled Agent (EA)"}},
    "publisher": {{"@type": "Organization", "name": "Fiduciary Tax & Accounting Services", "url": "{site}"}},
    "mainEntityOfPage": "{url}"
  }}
  </script>
</head>
<body>

  <div class="post-hero">
    <div class="post-hero-inner">
      <div class="post-cat">{category}</div>
      <h1>{title}</h1>
      <div class="post-meta">By Dustin C. Toney, EA &nbsp;·&nbsp; {pretty_date}</div>
    </div>
  </div>

  <div class="post-body">
    <a href="index.html" class="post-back">Back to News &amp; Insights</a>
    <div>{body}</div>
    <div class="post-cta">
      <div>
        <h3>Have questions about your situation?</h3>
        <p>Every estate and trust situation is different — reach out and we'll walk you through what's needed.</p>
      </div>
      <a href="../index.html#contact" class="btn-primary">Contact Us</a>
    </div>
    <a href="index.html" class="post-back" style="margin-top:1rem;margin-bottom:0;">Back to News &amp; Insights</a>
  </div>

  <script src="../shared.js{asset_v}"></script>
</body>
</html>
"""


def pretty(d):
    dt = date.fromisoformat(d)
    return dt.strftime("%B %#d, %Y")


def main():
    with open("blog/posts.json") as fh:
        posts = json.load(fh)

    for p in posts:
        slug = p["slug"]
        # posts.json stores some fields with entities already; unescape for re-escaping cleanly
        title = p["title"]
        category = p["category"]
        excerpt = p["excerpt"]
        url = f"{SITE}/blog/{slug}.html"
        html = TEMPLATE.format(
            title=title,
            title_esc=escape(title, quote=True),
            title_json=json.dumps(title),
            excerpt_esc=escape(excerpt, quote=True),
            excerpt_json=json.dumps(excerpt),
            category=escape(category),
            url=url,
            site=SITE,
            iso_date=p["date"],
            pretty_date=pretty(p["date"]),
            body=p["body"],
            asset_v=ASSET_V,
        )
        with open(f"blog/{slug}.html", "w") as fh:
            fh.write(html)
        print(f"  wrote blog/{slug}.html")

    # ---- sitemap ----
    today = date.today().isoformat()
    urls = [
        (f"{SITE}/", today, "monthly", "1.0"),
        (f"{SITE}/professional-fiduciaries.html", today, "monthly", "0.9"),
        (f"{SITE}/personal-fiduciaries.html", today, "monthly", "0.9"),
        (f"{SITE}/individual.html", today, "monthly", "0.9"),
        (f"{SITE}/blog/index.html", today, "weekly", "0.7"),
    ]
    for f in sorted(glob.glob("services/*.html")):
        urls.append((f"{SITE}/{f}", today, "monthly", "0.6"))
    for p in posts:
        urls.append((f"{SITE}/blog/{p['slug']}.html", p.get("date", today), "monthly", "0.5"))

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, priority in urls:
        xml += ["  <url>",
                f"    <loc>{loc}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                f"    <changefreq>{changefreq}</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>"]
    xml.append("</urlset>")
    with open("sitemap.xml", "w") as fh:
        fh.write("\n".join(xml) + "\n")
    print(f"  wrote sitemap.xml ({len(urls)} URLs)")


if __name__ == "__main__":
    main()
