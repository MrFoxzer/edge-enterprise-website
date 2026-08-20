#!/usr/bin/env python3
"""Render the Edge blog from blog-data/*.json.

Each JSON file: {slug, title, desc, date (YYYY-MM-DD), read, body (HTML)}.
Renders blog/<slug>.html for every post + blog.html index (newest first).
Weekly automation appends one JSON file and re-runs this script.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_core_pages import head, hero, CTA_BAND, NAV, FOOTER, write, BASE


def esc(s):
    return s.replace('"', '&quot;')


def jesc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def pretty_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


def load_posts():
    posts = []
    for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "blog-data", "*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        posts.append(json.load(open(f)))
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def build_post(p, all_posts):
    canon = f"blog/{p['slug']}.html"
    others = [q for q in all_posts if q["slug"] != p["slug"]][:3]
    related = "\n".join(f"""                <a href="/blog/{q['slug']}.html" class="city-nearby-card">
                    <span class="city-nearby-state">BLOG</span>
                    <h3>{q['title'][:70]}</h3>
                    <span class="city-nearby-arrow">→</span>
                </a>""" for q in others)
    schema = f"""    [{{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{jesc(p['title'])}",
      "description": "{jesc(p['desc'])}",
      "datePublished": "{p['date']}",
      "dateModified": "{p['date']}",
      "author": {{ "@type": "Organization", "name": "Edge Enterprise LLC", "url": "{BASE}/" }},
      "publisher": {{ "@type": "Organization", "name": "Edge Enterprise LLC", "logo": {{ "@type": "ImageObject", "url": "{BASE}/logo.png" }} }},
      "mainEntityOfPage": "{BASE}/{canon}"
    }},
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{BASE}/blog.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "{jesc(p['title'])}", "item": "{BASE}/{canon}" }}
      ]
    }}]"""
    title_html = p["title"]
    if ":" in title_html:
        a, b = title_html.split(":", 1)
        title_html = f'<span class="text-accent">{a}</span>:{b}'
    else:
        title_html = f'<span class="text-accent">{title_html}</span>'
    body = hero("EDGE ENTERPRISE BLOG", title_html,
                f"Published {pretty_date(p['date'])} · {p['read']} · By the Edge Enterprise crew") + f"""
    <section class="section section-city-context">
        <div class="container">
            <div class="city-context-grid">
                <div class="city-context-main">
                    <div class="city-context-body blog-post-body">
{p['body']}
                    </div>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>About Edge Enterprise</h3>
                        <ul>
                            <li><strong>Trade</strong><span>Commercial framing</span></li>
                            <li><strong>Experience</strong><span>25+ years</span></li>
                            <li><strong>Units framed</strong><span>1,000+</span></li>
                            <li><strong>Service area</strong><span>MN · ND · WI · MT</span></li>
                            <li><strong>Estimates</strong><span><a href="/contact.html" style="color:var(--primary)">Free →</a></span></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>
    <section class="section section-city-nearby">
        <div class="container">
            <div class="section-header">
                <span class="section-label">KEEP READING</span>
                <h2 class="section-title">More From the <span class="text-accent">Blog</span></h2>
            </div>
            <div class="city-nearby-grid">
{related}
            </div>
        </div>
    </section>""" + CTA_BAND
    write(canon, head(f"{p['title']} | Edge Enterprise LLC", esc(p["desc"]), canon, schema) + NAV + body + FOOTER)


def build_index(posts):
    cards = "\n".join(f"""                <a href="/blog/{p['slug']}.html" class="city-why-card" style="text-decoration:none">
                    <div class="city-why-num">{pretty_date(p['date'])}</div>
                    <h3>{p['title']}</h3>
                    <p>{p['desc'][:150]}…</p>
                    <p style="margin-top:12px;color:var(--primary);font-weight:600">Read article → <span style="color:var(--gray);font-weight:400">· {p['read']}</span></p>
                </a>""" for p in posts)
    schema = f"""    {{
      "@context": "https://schema.org",
      "@type": "Blog",
      "name": "Edge Enterprise Framing Blog",
      "url": "{BASE}/blog.html"
    }}"""
    body = hero("INSIGHTS FROM THE FIELD",
                'The Edge Enterprise <span class="text-accent">Blog</span>',
                f"{len(posts)} articles of straight answers on framing costs, schedules, materials, and hiring — a new post every week, written by the crews that build it.") + f"""
    <section class="section section-city-why">
        <div class="container">
            <div class="section-header">
                <span class="section-label">LATEST ARTICLES</span>
                <h2 class="section-title">Framing Knowledge, <span class="text-accent">Free of Charge</span></h2>
            </div>
            <div class="city-why-grid">
{cards}
            </div>
        </div>
    </section>""" + CTA_BAND
    write("blog.html", head("Framing Blog — Weekly Articles on Costs, Schedules & How-Tos | Edge Enterprise LLC",
                            "Weekly framing articles from Edge Enterprise: commercial framing costs, wood vs. steel, winter framing, schedules, hiring crews, and how to vet subcontractors.",
                            "blog.html", schema) + NAV + body + FOOTER)


if __name__ == "__main__":
    posts = load_posts()
    for p in posts:
        build_post(p, posts)
    build_index(posts)
    print(f"rendered {len(posts)} posts + index")
