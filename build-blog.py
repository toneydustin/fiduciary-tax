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
from datetime import date, datetime
from html import escape
from email.utils import format_datetime

SITE = "https://fiduciary.tax"
ASSET_V = "?v=20260805e"  # bump on each deploy to bust caches

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
  <meta property="og:image" content="{site}/og-image.png">
  <meta name="twitter:image" content="{site}/og-image.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <link rel="alternate" type="application/rss+xml" title="FTAS News &amp; Insights" href="{site}/feed.xml">
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

  <main id="main-content">
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
    {services_html}
    <div class="post-cta">
      <div>
        <h3>Have questions about your situation?</h3>
        <p>Every estate and trust situation is different — reach out and we'll walk you through what's needed.</p>
      </div>
      <a href="../index.html#contact" class="btn-primary">Contact Us</a>
    </div>
    <a href="index.html" class="post-back" style="margin-top:1rem;margin-bottom:0;">Back to News &amp; Insights</a>
  </div>

  </main>

  <script src="../shared.js{asset_v}"></script>
</body>
</html>
"""


def pretty(d):
    dt = date.fromisoformat(d)
    return dt.strftime("%B %#d, %Y")


def main():
    with open("blog/posts.json", encoding="utf-8") as fh:
        posts = json.load(fh)

    for p in posts:
        slug = p["slug"]
        title = p["title"]
        category = p["category"]
        excerpt = p["excerpt"]
        url = f"{SITE}/blog/{slug}.html"
        svcs = p.get("services", [])
        if svcs:
            cards = "".join(
                f'<a href="../services/{s["slug"]}.html" class="post-svc-card">'
                f'<span class="psc-icon">{s["icon"]}</span>'
                f'<span class="psc-title">{escape(s["title"])}</span></a>'
                for s in svcs
            )
            services_html = (
                '<div class="post-services">'
                '<h3>Related Services</h3>'
                f'<div class="post-services-grid">{cards}</div>'
                '</div>'
            )
        else:
            services_html = ""
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
            services_html=services_html,
            asset_v=ASSET_V,
        )
        with open(f"blog/{slug}.html", "w", encoding="utf-8") as fh:
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

    # ---- RSS feed ----
    sorted_posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    def rfc822(iso):
        dt = datetime.fromisoformat(iso + "T12:00:00+00:00")
        return format_datetime(dt, usegmt=True)

    items = []
    for p in sorted_posts[:20]:
        items.append(
            f"    <item>\n"
            f"      <title>{escape(p['title'])}</title>\n"
            f"      <link>{SITE}/blog/{p['slug']}.html</link>\n"
            f"      <description>{escape(p['excerpt'])}</description>\n"
            f"      <pubDate>{rfc822(p['date'])}</pubDate>\n"
            f"      <guid isPermaLink=\"true\">{SITE}/blog/{p['slug']}.html</guid>\n"
            f"      <category>{escape(p['category'])}</category>\n"
            f"    </item>"
        )
    build_date = rfc822(date.today().isoformat())
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        '  <channel>\n'
        '    <title>FTAS News &amp; Insights</title>\n'
        f'    <link>{SITE}/blog/index.html</link>\n'
        '    <description>Tax law updates, estate planning insights, and fiduciary guidance from Fiduciary Tax &amp; Accounting Services.</description>\n'
        '    <language>en-us</language>\n'
        f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        f'    <lastBuildDate>{build_date}</lastBuildDate>\n'
        + "\n".join(items) + "\n"
        '  </channel>\n'
        '</rss>\n'
    )
    with open("feed.xml", "w", encoding="utf-8") as fh:
        fh.write(rss)
    print(f"  wrote feed.xml ({len(items)} items)")


if __name__ == "__main__":
    main()
