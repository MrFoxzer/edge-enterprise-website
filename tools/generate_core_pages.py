#!/usr/bin/env python3
"""Edge Enterprises core pages + blog generator.

Builds: about.html, services.html, projects.html, contact.html,
application-received.html, blog.html, blog/*.html

Reuses styles.css classes from the location-page system. Idempotent.
Run:  python3 tools/generate_core_pages.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://edgeenterprise.net"

NAV = """
    <nav class="nav nav-city" id="mainNav">
        <div class="nav-inner">
            <a href="/" class="nav-logo">
                <span class="nav-logo-text">EDGE <span class="nav-logo-accent">ENTERPRISE</span></span>
                <img src="/logo-icon.png" alt="" class="nav-icon">
            </a>
            <div class="nav-links" id="navLinks">
                <a href="/about.html" class="nav-link">About</a>
                <a href="/services.html" class="nav-link">Services</a>
                <a href="/projects.html" class="nav-link">Projects</a>
                <a href="/index.html#service-areas" class="nav-link">Service Areas</a>
                <a href="/blog.html" class="nav-link">Blog</a>
                <a href="/careers.html" class="nav-link">Careers</a>
                <a href="tel:+13202172691" class="nav-link nav-phone">(320) 217-2691</a>
                <a href="/contact.html" class="nav-link nav-link-cta">Get a Quote</a>
            </div>
            <button class="nav-toggle" id="navToggle" aria-label="Toggle menu">
                <span></span><span></span><span></span>
            </button>
        </div>
    </nav>"""

FOOTER = """
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <img src="/logo.png" alt="Edge Enterprise LLC" class="footer-logo">
                    <p>Professional construction services built on integrity, precision, and excellence. Serving clients nationwide from our Minnesota &amp; North Dakota headquarters.</p>
                </div>
                <div class="footer-links">
                    <h4>Quick Links</h4>
                    <a href="/about.html">About Us</a>
                    <a href="/services.html">Services</a>
                    <a href="/projects.html">Portfolio</a>
                    <a href="/blog.html">Blog</a>
                    <a href="/careers.html">Careers</a>
                    <a href="/for-gcs.html">For GCs</a>
                    <a href="/estimate.html">Instant Estimate</a>
                    <a href="/contact.html">Contact</a>
                </div>
                <div class="footer-links">
                    <h4>Service Areas</h4>
                    <a href="/locations/minnesota.html">Minnesota</a>
                    <a href="/locations/north-dakota.html">North Dakota</a>
                    <a href="/locations/wisconsin.html">Wisconsin</a>
                    <a href="/locations/montana.html">Montana</a>
                </div>
                <div class="footer-links">
                    <h4>Contact</h4>
                    <a href="tel:+13202172691">(320) 217-2691</a>
                    <a href="mailto:rtrigueros@edgeenterprise.net">rtrigueros@edgeenterprise.net</a>
                    <a href="/contact.html">Send a message</a>
                    <span>15763 221st Ave, Long Prairie, MN 56347</span>
                    <span>Horace, ND</span>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Edge Enterprise LLC. All rights reserved.</p>
                <p>Licensed &amp; Insured · HQ Long Prairie, MN · Crews serving MN, ND, WI &amp; MT · COI available on request</p>
            </div>
        </div>
    </footer>
    <div class="mobile-call-bar">
        <a href="tel:+13202172691" class="mcb-call">Call (320) 217-2691</a>
        <a href="/contact.html" class="mcb-quote">Free Estimate</a>
    </div>
    <script src="/script.js?v=nc3"></script>
</body>
</html>"""


def head(title, desc, canon, schema="", extra_head=""):
    schema_tag = f'\n    <script type="application/ld+json">\n{schema}\n    </script>' if schema else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{BASE}/{canon}">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <meta name="theme-color" content="#0a0a0a">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{BASE}/{canon}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:site_name" content="Edge Enterprise LLC">
    <meta property="og:image" content="{BASE}/og-card.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{BASE}/og-card.jpg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css?v=nc3">{extra_head}{schema_tag}
</head>
<body>"""


def hero(label, title_html, sub, ctas=""):
    return f"""
    <section class="city-hero">
        <div class="city-hero-bg"></div>
        <div class="container">
            <div class="city-hero-inner">
                <span class="section-label">{label}</span>
                <h1 class="city-hero-title">{title_html}</h1>
                <p class="city-hero-sub">{sub}</p>
                {ctas}
            </div>
        </div>
    </section>"""


CTA_BAND = """
    <section class="section section-cta">
        <div class="container">
            <div class="cta-block">
                <h2 class="cta-title">Ready to Talk About Your <span class="text-accent">Project?</span></h2>
                <p class="cta-text">Tell us about your build. We'll get back to you with a clear, honest scope and estimate — typically within one business day.</p>
                <a href="/contact.html" class="btn btn-primary btn-large">
                    <span>Request a Free Estimate</span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </a>
            </div>
        </div>
    </section>"""


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)
    print("wrote", path)


# ============================================================== ABOUT
def build_about():
    schema = """    {
      "@context": "https://schema.org",
      "@type": "AboutPage",
      "name": "About Edge Enterprise LLC",
      "url": "https://edgeenterprise.net/about.html"
    }"""
    body = hero("WHO WE ARE",
                'About <span class="text-accent">Edge Enterprise</span>',
                "A family-owned commercial framing company with 25+ years in the trade, 1,000+ multi-family units framed, and crews that show up.") + f"""
    <section class="section section-city-context">
        <div class="container">
            <div class="city-context-grid">
                <div class="city-context-main">
                    <span class="section-label">OUR STORY</span>
                    <h2 class="section-title">Built on <span class="text-accent">Integrity</span>. Driven by <span class="text-accent">Excellence</span>.</h2>
                    <div class="city-context-body">
                        <p>Edge Enterprise LLC is a family-owned construction company rooted in precision, quality, and an unwavering work ethic. For more than 25 years our crews have framed the buildings people live, work, and heal in — from large-scale apartment communities and senior living campuses to commercial structures and complex custom homes across the Upper Midwest and Mountain West.</p>
                        <p>We specialize in commercial wood and steel framing, and multi-family is our core: more than 1,000 units framed, including 45th Street Apartments, ENVY, EOLA, Oxbow Heights, and the Rogers Senior Living &amp; Senior Center. We work as a trusted framing subcontractor for repeat general contractor partners — Comeland Builders, Gast Construction, and Miller Architects &amp; Builders — and directly with owners on design-build work.</p>
                        <p>Headquartered in Long Prairie, Minnesota with a satellite presence in Horace, North Dakota, we serve builders across Minnesota, North Dakota, Wisconsin, and Montana — and travel nationwide for the right project. Our promise is simple: frame it straight, frame it on schedule, and leave every GC glad they hired us.</p>
                    </div>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>Edge at a Glance</h3>
                        <ul>
                            <li><strong>Founded</strong><span>Family-owned &amp; operated</span></li>
                            <li><strong>Experience</strong><span>25+ years</span></li>
                            <li><strong>Units framed</strong><span>1,000+</span></li>
                            <li><strong>Headquarters</strong><span>Long Prairie, MN</span></li>
                            <li><strong>Satellite</strong><span>Horace, ND</span></li>
                            <li><strong>Licensed &amp; insured</strong><span>MN · ND · WI · MT</span></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>
    <section class="section section-city-why">
        <div class="container">
            <div class="section-header">
                <span class="section-label">WHY EDGE</span>
                <h2 class="section-title">What Sets Us <span class="text-accent">Apart</span></h2>
            </div>
            <div class="city-why-grid">
                <div class="city-why-card"><div class="city-why-num">01</div><h3>Family-owned, crew-operated</h3><p>Our own crews frame every project, run by people whose name is on the company. No brokered labor, no bait-and-switch.</p></div>
                <div class="city-why-card"><div class="city-why-num">02</div><h3>Multi-family production discipline</h3><p>Unit-by-unit QC and honest look-ahead scheduling keep floor 4 as tight as floor 1 — and keep the OAC meeting boring, the way GCs like it.</p></div>
                <div class="city-why-card"><div class="city-why-num">03</div><h3>Built for northern climates</h3><p>Real snow loads, open-prairie wind, and frost depths measured in feet. We frame for the actual code environment, all year round.</p></div>
            </div>
        </div>
    </section>""" + CTA_BAND
    write("about.html", head("About Us | Family-Owned Commercial Framing | Edge Enterprise LLC",
                             "Edge Enterprise LLC is a family-owned commercial framing company with 25+ years of experience and 1,000+ multi-family units framed across MN, ND, WI, and MT.",
                             "about.html", schema) + NAV + body + FOOTER)


# ============================================================== SERVICES
SERVICES = [
    ("commercial-framing", "Commercial Framing", "Structural framing for retail, office, hospitality, and light-industrial buildings — wood or steel, built to commercial code and schedule."),
    ("wood-framing", "Wood Framing", "Dimensional lumber and engineered wood framing — floors, walls, roofs, and everything between — cut and stood by career framers."),
    ("steel-framing", "Steel & Metal Stud Framing", "Light-gauge metal stud framing for commercial interiors, exterior non-bearing walls, and load-bearing cold-formed steel structures."),
    ("multi-family-framing", "Multi-Family Framing", "Apartment buildings, townhomes, and senior living — 1,000+ units framed and counting."),
    ("framing-subcontractor", "Framing Subcontractor", "A reliable framing sub for general contractors — real scopes, real schedules, clean paperwork, and crews that show up."),
    ("custom-home-framing", "Custom Home Framing", "Complex custom homes — vaulted great rooms, long-span beams, complicated roofs — framed by crews who like the hard ones."),
    ("finished-carpentry", "Finished Carpentry", "Trim, doors, millwork, and the detail work people actually touch — installed by carpenters who care about the last 2%."),
]


def build_services():
    cards = "\n".join(f"""                <a class="city-why-card" href="/locations/{slug}/index.html" style="text-decoration:none">
                    <div class="city-why-num">0{i+1}</div>
                    <h3>{name}</h3>
                    <p>{desc}</p>
                    <p style="margin-top:12px;color:var(--primary);font-weight:600">Explore {name} →</p>
                </a>""" for i, (slug, name, desc) in enumerate(SERVICES))
    schema = """    {
      "@context": "https://schema.org",
      "@type": "Service",
      "provider": { "@type": "GeneralContractor", "name": "Edge Enterprise LLC", "url": "https://edgeenterprise.net/" },
      "serviceType": "Commercial Framing",
      "areaServed": ["Minnesota", "North Dakota", "Wisconsin", "Montana"]
    }"""
    body = hero("WHAT WE DO",
                'Framing Services <span class="text-accent">Done Right</span>',
                "Full-scope structural framing — commercial, multi-family, custom residential, and finished carpentry — across Minnesota, North Dakota, Wisconsin, and Montana.") + f"""
    <section class="section section-city-why">
        <div class="container">
            <div class="section-header">
                <span class="section-label">SERVICES</span>
                <h2 class="section-title">Seven Trades. <span class="text-accent">One Sub.</span></h2>
                <p class="section-subtitle">Every service links to city-by-city pages with local specs and FAQs for all 183 cities we serve.</p>
            </div>
            <div class="city-why-grid">
{cards}
            </div>
        </div>
    </section>""" + CTA_BAND
    write("services.html", head("Framing Services | Commercial, Multi-Family, Steel & Wood | Edge Enterprise LLC",
                                "Commercial framing, wood & steel framing, multi-family construction, framing subcontracting, custom home framing, and finished carpentry across MN, ND, WI & MT.",
                                "services.html", schema) + NAV + body + FOOTER)


# ============================================================== PROJECTS
def build_projects():
    idx = open(os.path.join(ROOT, "index.html")).read()
    m = re.search(r'(<section class="section section-projects" id="projects">.*?</section>)\s*<!-- Stats Section -->', idx, re.S)
    section_html = m.group(1)
    extra = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/css/glightbox.min.css">
    <script src="https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/js/glightbox.min.js"></script>"""
    body = hero("OUR PORTFOLIO",
                'Projects That <span class="text-accent">Speak for Themselves</span>',
                "Multi-family communities, senior living, commercial builds, and custom retreats — framed by Edge Enterprise crews alongside GC partners Comeland Builders, Gast Construction, and Miller Architects & Builders.") + section_html + CTA_BAND
    schema = """    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "Edge Enterprise Project Portfolio",
      "url": "https://edgeenterprise.net/projects.html"
    }"""
    write("projects.html", head("Project Portfolio | Multi-Family & Commercial Framing | Edge Enterprise LLC",
                                "See Edge Enterprise framing projects: Rogers Senior Living, 45th Street Apartments, ENVY, EOLA, Oxbow Heights, Panda Express, and more across the Upper Midwest.",
                                "projects.html", schema, extra) + NAV + body + FOOTER)


# ============================================================== CONTACT
def build_contact():
    schema = """    {
      "@context": "https://schema.org",
      "@type": "ContactPage",
      "name": "Contact Edge Enterprise LLC",
      "url": "https://edgeenterprise.net/contact.html"
    }"""
    body = hero("GET IN TOUCH",
                "Let&#39;s Talk About Your <span class=\"text-accent\">Build</span>",
                "Send your plans or just a description — we respond to every inquiry, typically within one business day.") + """
    <section class="section section-city-context">
        <div class="container">
            <div class="city-context-grid">
                <div class="city-context-main">
                    <span class="section-label">SEND A MESSAGE</span>
                    <h2 class="section-title">Request a <span class="text-accent">Free Estimate</span></h2>
                    <form class="contact-form" name="contact-plans" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data" style="margin-top:24px">
                        <input type="hidden" name="form-name" value="contact-plans">
                        <p style="display:none"><label>Don't fill this out: <input name="bot-field"></label></p>
                        <div class="form-group">
                            <input type="text" id="formName" name="name" required placeholder=" ">
                            <label for="formName">Your Name</label>
                            <div class="form-line"></div>
                        </div>
                        <div class="form-group">
                            <input type="email" id="formEmail" name="email" required placeholder=" ">
                            <label for="formEmail">Email Address</label>
                            <div class="form-line"></div>
                        </div>
                        <div class="form-group">
                            <input type="tel" id="formPhone" name="phone" placeholder=" ">
                            <label for="formPhone">Phone Number</label>
                            <div class="form-line"></div>
                        </div>
                        <div class="form-group">
                            <input type="text" id="formCompany" name="company" placeholder=" ">
                            <label for="formCompany">Company (if GC / developer)</label>
                            <div class="form-line"></div>
                        </div>
                        <div class="form-group">
                            <input type="text" id="formProject" name="project-type" placeholder=" ">
                            <label for="formProject">Project Type &amp; Location (city, state)</label>
                            <div class="form-line"></div>
                        </div>
                        <div class="form-group">
                            <input type="text" id="formBidDue" name="bid-due-date" placeholder=" ">
                            <label for="formBidDue">Bid Due Date (if bidding)</label>
                            <div class="form-line"></div>
                        </div>
                        <div class="form-group" style="padding-top:8px">
                            <label style="position:static;display:block;margin-bottom:8px;font-size:14px;color:var(--gray-light)">Attach plans (PDF or ZIP, up to 8&nbsp;MB &mdash; email larger sets to <a href="mailto:rtrigueros@edgeenterprise.net" style="color:var(--primary)">rtrigueros@edgeenterprise.net</a>)</label>
                            <input type="file" name="plans" accept=".pdf,.zip">
                        </div>
                        <div class="form-group">
                            <textarea id="formMessage" name="message" rows="5" required placeholder=" "></textarea>
                            <label for="formMessage">Tell us about your project</label>
                            <div class="form-line"></div>
                        </div>
                        <button type="submit" class="btn btn-primary btn-large"><span>Send Message</span>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                        </button>
                        <p style="margin-top:14px;color:var(--gray-light);font-size:14px">We respond within 1 business day &mdash; or call <a href="tel:+13202172691" style="color:var(--primary)">(320) 217-2691</a> for same-day answers.</p>
                    </form>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>Reach Us Directly</h3>
                        <ul>
                            <li><strong>Phone</strong><span>(320) 217-2691</span></li>
                            <li><strong>Headquarters</strong><span>Long Prairie, MN</span></li>
                            <li><strong>Satellite</strong><span>Horace, ND</span></li>
                            <li><strong>Response time</strong><span>Within 1 business day</span></li>
                            <li><strong>Hiring?</strong><span><a href="/careers.html" style="color:var(--primary)">See open roles →</a></span></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>"""
    write("contact.html", head("Contact Us | Free Framing Estimates | Edge Enterprise LLC",
                               "Contact Edge Enterprise LLC for commercial framing, multi-family, and finished carpentry estimates in MN, ND, WI & MT. Call (320) 217-2691 or send your plans.",
                               "contact.html", schema) + NAV + body + FOOTER)

    # thank-you + application-received pages
    for fname, title, msg in [
        ("thank-you.html", "Message Received", "Thanks for reaching out — your message is in our inbox and we'll get back to you within one business day. Need it sooner? Call (320) 217-2691."),
        ("application-received.html", "Application Received", "Thanks for applying to Edge Enterprise. We review every application and will contact you about next steps."),
    ]:
        body = hero("THANK YOU", f'{title.split()[0]} <span class="text-accent">{" ".join(title.split()[1:])}</span>', msg,
                    '''<div class="city-hero-ctas"><a href="/" class="btn btn-primary"><span>Back to Home</span></a><a href="/projects.html" class="btn btn-ghost"><span>See Our Work</span></a></div>''')
        write(fname, head(f"{title} | Edge Enterprise LLC", msg, fname,
                          extra_head='\n    <meta name="robots" content="noindex">') + NAV + body + FOOTER)


# ============================================================== BLOG
POSTS = [
    {
        "slug": "wood-vs-steel-framing-commercial",
        "title": "Wood vs. Steel Framing for Commercial Buildings: How to Choose",
        "desc": "Wood framing usually wins on cost for low-rise commercial buildings; steel wins on non-combustible construction, long spans, and Type II code requirements. Here's how GCs and owners should decide.",
        "date": "2026-08-18",
        "read": "6 min read",
        "body": """
<p><strong>The short answer:</strong> for most low-rise commercial and multi-family buildings, wood framing costs 10–20% less installed than light-gauge steel. Steel earns its premium when the code requires non-combustible construction (Type I/II), when spans and ceiling heights stretch beyond dimensional lumber's comfort zone, or when the owner prioritizes dimensional stability in long interior runs.</p>
<h2>When wood framing is the right call</h2>
<p>Wood is the default structure for buildings up to five stories across the Upper Midwest, and for good reason. Material is regionally abundant, every inspector knows the code path, and crews can frame through a Minnesota winter without specialized equipment. For garden-style apartments, townhomes, senior living, and podium buildings (wood over a concrete or steel first floor), wood framing delivers the lowest cost per square foot and the fastest dry-in.</p>
<p>Modern engineered wood — I-joists, LVL, PSL, glulam, and floor trusses — has also erased many of the span limitations that once pushed projects to steel.</p>
<h2>When steel takes over</h2>
<ul>
<li><strong>Non-combustible construction:</strong> hospitals, some schools, and buildings where the code analysis lands on Type I or II construction require steel or concrete structure.</li>
<li><strong>Commercial interiors:</strong> demising walls, shaft walls, and furring in commercial shells are almost always metal stud — faster, straighter, and rated assemblies are well documented.</li>
<li><strong>Long spans and tall walls:</strong> cold-formed steel handles 20-foot-plus wall heights and long floor spans without the creep wood can develop.</li>
<li><strong>Moisture and insects:</strong> steel doesn't rot, warp, or feed anything.</li>
</ul>
<h2>The hybrid reality</h2>
<p>Most commercial projects we frame use both: wood structure with metal-stud interiors, or a steel shell with wood-framed infill. The advantage of hiring a framing contractor that self-performs both — like Edge Enterprise — is that the wood-to-steel interface details actually get built the way the engineer drew them, under one subcontract and one schedule.</p>
<h2>Cost comparison rules of thumb (2026)</h2>
<ul>
<li>Wood framing labor + material: roughly $12–$22 per square foot for multi-family, depending on complexity and region.</li>
<li>Light-gauge steel framing: typically 10–25% above comparable wood, narrowing on repetitive commercial interiors.</li>
<li>Deflection, fire-rating, and insurance requirements can flip the math — run both numbers on borderline projects.</li>
</ul>
<p>Planning a commercial or multi-family build in Minnesota, North Dakota, Wisconsin, or Montana? <a href="/contact.html">Send us your plans</a> — we frame both systems and will give you an honest comparison rather than steering you to the only thing we sell.</p>""",
    },
    {
        "slug": "commercial-framing-cost-guide",
        "title": "How Much Does Commercial Framing Cost in 2026?",
        "desc": "Commercial framing costs in 2026 typically run $12–$30+ per square foot installed depending on building type, height, and structure. A framing contractor breaks down the real numbers.",
        "date": "2026-08-18",
        "read": "7 min read",
        "body": """
<p><strong>The short answer:</strong> in the Upper Midwest in 2026, expect installed framing costs (labor + lumber/steel package) of roughly <strong>$12–$22 per square foot for wood-framed multi-family</strong>, <strong>$15–$30+ for commercial steel stud structures</strong>, and more for complex custom work. Labor alone typically represents $5–$10/SF of that. Here's what moves the number.</p>
<h2>What drives framing cost</h2>
<h3>1. Building type and repetition</h3>
<p>A 100-unit garden apartment with stacked, repeating floor plans frames dramatically cheaper per foot than a one-off commercial building with unique conditions on every wall. Repetition lets crews build production rhythm — that's why experienced multi-family framers can beat generalist bids without cutting corners.</p>
<h3>2. Structure and materials</h3>
<p>Dimensional lumber remains the value play. Engineered wood (I-joists, LVL, glulam) adds material cost but saves labor and callbacks. Light-gauge steel adds 10–25%. Panelized walls shift cost from field labor to the panel plant — often a wash on price but a win on schedule.</p>
<h3>3. Height and access</h3>
<p>Every story above the second adds hoisting time, fall-protection overhead, and crane or forklift cost. Four-story wood over podium is the sweet spot for density vs. framing cost across MN and ND right now.</p>
<h3>4. Climate and season</h3>
<p>Winter framing in Minnesota and North Dakota is routine for local crews but adds snow removal, cold-weather sequencing, and temporary enclosure costs — typically 3–8% on a winter start.</p>
<h3>5. Prevailing wage</h3>
<p>Public and publicly financed projects in Minnesota pay state prevailing wage rates with certified payroll. Budget accordingly — an experienced sub prices this correctly up front instead of surprising you with change orders.</p>
<h2>What a real framing bid should include</h2>
<ul>
<li>Complete scope: plates, walls, floor systems, roof or truss set, sheathing, blocking, backing, rough openings, hardware</li>
<li>Crew size and schedule commitment (ask how many carpenters, not just "a crew")</li>
<li>Insurance certificates naming the GC and owner as additional insureds</li>
<li>Clean lien-waiver and pay-app process</li>
</ul>
<p>Want a real number instead of a range? <a href="/contact.html">Send Edge Enterprise your plans</a> for a line-item framing proposal — typically within a few business days.</p>""",
    },
    {
        "slug": "what-is-turnkey-framing",
        "title": "What Is Turn-Key Framing? (And Why GCs Ask for It)",
        "desc": "Turn-key framing means one subcontractor delivers the complete framed shell — labor, coordination, sheathing, windows, and housewrap — ready for the next trades. Here's what's included and why it de-risks your schedule.",
        "date": "2026-08-18",
        "read": "5 min read",
        "body": """
<p><strong>Turn-key framing</strong> means a single subcontractor takes your building from foundation to a complete, weather-tight framed shell — structure, sheathing, exterior windows and doors, and housewrap — so the next trades walk into a building that's ready for them. One contract, one schedule, one throat to choke.</p>
<h2>What's included in a turn-key framing package</h2>
<ul>
<li><strong>Structural framing:</strong> walls, floor systems, roof framing or truss set — wood, steel, or both</li>
<li><strong>Sheathing and weather barrier:</strong> roof and wall sheathing, Zip System taping or Tyvek housewrap, installed to manufacturer spec so warranties hold</li>
<li><strong>Exterior windows and doors:</strong> set, flashed, and integrated with the WRB</li>
<li><strong>Blocking and backing:</strong> for cabinets, handrails, fixtures, and everything the finish trades will hang</li>
<li><strong>Coordination:</strong> crane and lift logistics, panel deliveries, and sequencing with plumbers, electricians, and HVAC</li>
</ul>
<h2>Why GCs prefer it</h2>
<p>Every handoff between subs is a schedule risk and a warranty gap. When one sub frames the wall, sheathes it, tapes it, and sets the window, there's no argument about who left the leak. Superintendents also spend dramatically less time refereeing between a framer, a sheathing crew, and a window installer who all blame each other.</p>
<h2>Questions to ask a turn-key framing bidder</h2>
<ul>
<li>Do your own crews perform all scopes, or do you broker parts out?</li>
<li>Who is certified for the Zip or Tyvek installation, and will the manufacturer warranty stand?</li>
<li>What crew size will you commit, and what's your weekly production plan?</li>
<li>Can you show completed turn-key projects at this scale?</li>
</ul>
<p>Edge Enterprise delivers turn-key commercial framing — wood and metal framing, finished carpentry, windows, and housewrap — across Minnesota, North Dakota, Wisconsin, and Montana. <a href="/projects.html">See our completed work</a> or <a href="/contact.html">request a bid</a>.</p>""",
    },
    {
        "slug": "multi-family-framing-schedule",
        "title": "How to Keep a Multi-Family Framing Schedule From Slipping",
        "desc": "Multi-family framing schedules fail from undersized crews, late deliveries, and unmanaged inspections — not bad luck. A framing sub with 1,000+ units explains the production plan that holds.",
        "date": "2026-08-18",
        "read": "6 min read",
        "body": """
<p>Framing sits on the critical path of every multi-family project: nothing rocks, ropes, or roughs-in until the frame is up. When framing slips a week, the whole job slips a week. After 1,000+ framed units, here's what we've learned actually keeps the schedule.</p>
<h2>1. Crew size is a commitment, not a guess</h2>
<p>The number-one cause of slipped framing schedules is a sub who bid with 14 carpenters and shows up with 6. Demand a crew-size commitment in the subcontract — ours typically specify a minimum (12+ carpenters with a working foreman on multi-family) with the schedule tied to it.</p>
<h2>2. Build unit-by-unit, report weekly</h2>
<p>A framing schedule that says "Building B: 6 weeks" is a wish. A production plan that says "4 units framed per week, walls Monday–Wednesday, decks Thursday–Friday" is a plan you can verify every Friday. If production drops below plan, everyone knows in days — not at the monthly OAC meeting.</p>
<h2>3. Sequence deliveries like they're trades</h2>
<p>Lumber drops, truss deliveries, and panel shipments need the same look-ahead discipline as subcontractors. A truss crane sitting idle costs money; trusses buried under next week's lumber drop cost more.</p>
<h2>4. Make inspections a non-event</h2>
<p>Rated assemblies, draft stopping, shear nailing, and hold-downs should be photographed and self-inspected before the official walk. A failed framing inspection can freeze three trades. Our foremen walk every building against the inspection checklist before we ever call it in.</p>
<h2>5. Respect the weather, don't fear it</h2>
<p>Upper-Midwest framing means snow. Winter framing works when you plan it: sequence dry-in early, stage materials for snow removal, and keep temporary enclosure in the budget instead of pretending January won't happen.</p>
<p>Need a framing sub whose schedule promises hold? <a href="/contact.html">Talk to Edge Enterprise</a> — multi-family is our core trade, from Fargo to the Twin Cities metro.</p>""",
    },
    {
        "slug": "zip-system-vs-tyvek-housewrap",
        "title": "Zip System vs. Tyvek Housewrap: What Framers Actually See",
        "desc": "Zip System integrates sheathing and WRB in one taped panel; Tyvek wraps standard sheathing with a mechanically fastened membrane. A framing contractor compares cost, speed, and real-world performance.",
        "date": "2026-08-18",
        "read": "6 min read",
        "body": """
<p>Both systems work when installed right — and both fail when installed wrong. The honest comparison from crews that install both:</p>
<h2>Zip System: sheathing and WRB in one</h2>
<p>Huber's Zip System builds the water-resistive barrier into the sheathing panel; seams get taped with acrylic tape. What we like: the building is effectively dried-in the day the sheathing is nailed and taped, which matters enormously on fast-tracked multi-family where trades stack up behind dry-in. What demands discipline: tape adhesion. Tape rolled onto a dusty or wet panel in the cold is tomorrow's leak — manufacturer spec calls for rolling every inch of tape, and inspectors increasingly check it.</p>
<h2>Tyvek: the proven wrap</h2>
<p>DuPont Tyvek over OSB or plywood is the system every crew in America knows. What we like: it's forgiving, fast, cheap, and the drainage-wrap variants handle bulk water well behind fiber cement and LP siding. What demands discipline: fastening and integration. Wind-shredded wrap flapping on a winter jobsite protects nothing, and window flashing sequence (wrap first vs. flange first) has to be consistent or you build in leaks.</p>
<h2>Cost and schedule</h2>
<ul>
<li>Zip panels cost more per sheet than OSB + Tyvek, but remove a whole installation step and trade.</li>
<li>On multi-family, Zip's instant dry-in routinely buys back 1–2 weeks of schedule vs. wrap-behind-the-framer sequencing.</li>
<li>On wind-exposed sites (western MN, the Dakotas), taped panels shrug off gusts that destroy unclad wrap.</li>
</ul>
<h2>Our bottom line</h2>
<p>Production multi-family on a tight schedule: Zip, taped by trained crews, rolled and inspected. Budget-driven projects with experienced siding contractors right behind the framer: Tyvek remains excellent value. Either way, the warranty follows the installation quality — which is why window and WRB installation belongs in the framing subcontract, not split across three trades.</p>
<p>Edge Enterprise installs both systems as part of our turn-key framing packages. <a href="/blog/what-is-turnkey-framing.html">Read what turn-key framing includes</a> or <a href="/contact.html">get a bid</a>.</p>""",
    },
    {
        "slug": "how-to-vet-a-framing-subcontractor",
        "title": "How to Vet a Framing Subcontractor: A GC's 10-Point Checklist",
        "desc": "Before you sign a framing sub, verify insurance, crew size, schedule history, payroll compliance, and lien practices. A 10-point checklist from a framing contractor that works for repeat GCs.",
        "date": "2026-08-18",
        "read": "7 min read",
        "body": """
<p>The cheapest framing bid is often the most expensive line on your job. Here's the 10-point vetting checklist we'd use if we were sitting on your side of the table:</p>
<h2>The checklist</h2>
<ol>
<li><strong>Certificates of insurance — before mobilization.</strong> CGL ($1M/$2M minimum), auto, umbrella, and workers' comp, with your company and the owner as additional insureds on ISO CG 20 10 and CG 20 37 forms. No COI, no gate access.</li>
<li><strong>Who actually swings the hammers?</strong> Ask whether the sub self-performs or brokers labor. Brokered crews mean the low bid gets re-shopped after you sign — and quality follows the margin.</li>
<li><strong>Crew-size commitment in writing.</strong> "We'll staff it appropriately" is not a number. Get minimum crew size and a weekly production plan in the subcontract.</li>
<li><strong>References from repeat GCs.</strong> One glowing reference means one good job. What you want is a GC who has hired them three times — repeat hires are the entire signal.</li>
<li><strong>Comparable project scale.</strong> A framer whose biggest job is a duplex will drown on a 120-unit podium building. Ask for addresses, unit counts, and the GC on each.</li>
<li><strong>Payroll and workforce compliance.</strong> On prevailing-wage work: certified payroll capability and IC-134 affidavits (in Minnesota). Everywhere: workers' comp that matches the state, and W-2 crews or properly registered subs — GC wage liability laws now reach up the chain.</li>
<li><strong>Schedule history, not schedule promises.</strong> Ask the last three GCs one question: did they hit the framing milestones?</li>
<li><strong>Safety program you can audit.</strong> Written program, OSHA training cards, fall-protection plan, and an EMR they'll show you.</li>
<li><strong>Clean paperwork machine.</strong> Timely pay apps, partial lien waivers with every payment, and final waivers at closeout. Subs who fight about paperwork fight about everything.</li>
<li><strong>Financial capacity for your pay cycle.</strong> Framing is labor-heavy; a sub who can't float payroll to your first draw becomes your problem in week three.</li>
</ol>
<h2>The one-question shortcut</h2>
<p>If you only ask one thing: <em>"Which GCs hire you again and again — and can I call them?"</em> Everything else shows up in that answer.</p>
<p>Edge Enterprise works as a framing subcontractor for repeat GC partners across MN, ND, WI, and MT — Comeland Builders, Gast Construction, and Miller Architects &amp; Builders among them. <a href="/contact.html">Request our qualification package</a> and put us through this exact checklist.</p>""",
    },
]


def build_blog():
    # blog index
    cards = "\n".join(f"""                <a href="/blog/{p['slug']}.html" class="city-why-card" style="text-decoration:none">
                    <div class="city-why-num">{p['date']}</div>
                    <h3>{p['title']}</h3>
                    <p>{p['desc'][:150]}…</p>
                    <p style="margin-top:12px;color:var(--primary);font-weight:600">Read article → <span style="color:var(--gray);font-weight:400">· {p['read']}</span></p>
                </a>""" for p in POSTS)
    schema = """    {
      "@context": "https://schema.org",
      "@type": "Blog",
      "name": "Edge Enterprise Framing Blog",
      "url": "https://edgeenterprise.net/blog.html"
    }"""
    body = hero("INSIGHTS FROM THE FIELD",
                'The Edge Enterprise <span class="text-accent">Blog</span>',
                "Straight answers on framing costs, schedules, materials, and hiring — written by the crews that build it, not a marketing agency.") + f"""
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
    write("blog.html", head("Framing Blog | Costs, Schedules & How-Tos | Edge Enterprise LLC",
                            "Straight answers on commercial framing costs, wood vs. steel, turn-key framing, multi-family schedules, and vetting subcontractors — from Edge Enterprise LLC.",
                            "blog.html", schema) + NAV + body + FOOTER)

    # posts
    for p in POSTS:
        canon = f"blog/{p['slug']}.html"
        others = [q for q in POSTS if q["slug"] != p["slug"]][:3]
        related = "\n".join(f"""                <a href="/blog/{q['slug']}.html" class="city-nearby-card">
                    <span class="city-nearby-state">BLOG</span>
                    <h3>{q['title'][:60]}</h3>
                    <span class="city-nearby-arrow">→</span>
                </a>""" for q in others)
        schema = f"""    [{{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{p['title'].replace('"', '')}",
      "description": "{p['desc'].replace('"', '')}",
      "datePublished": "{p['date']}",
      "dateModified": "{p['date']}",
      "author": {{ "@type": "Organization", "name": "Edge Enterprise LLC", "url": "https://edgeenterprise.net/" }},
      "publisher": {{ "@type": "Organization", "name": "Edge Enterprise LLC", "logo": {{ "@type": "ImageObject", "url": "https://edgeenterprise.net/logo.png" }} }},
      "mainEntityOfPage": "{BASE}/{canon}"
    }},
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{BASE}/blog.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "{p['title'].replace('"', '')}", "item": "{BASE}/{canon}" }}
      ]
    }}]"""
        body = hero("EDGE ENTERPRISE BLOG",
                    f'<span class="text-accent">{p["title"].split(":")[0]}</span>' + (f': {p["title"].split(":", 1)[1]}' if ":" in p["title"] else ""),
                    f"Published {p['date']} · {p['read']} · By the Edge Enterprise crew") + f"""
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
        write(canon, head(f"{p['title']} | Edge Enterprise LLC", p["desc"], canon, schema) + NAV + body + FOOTER)


if __name__ == "__main__":
    build_about()
    build_services()
    build_projects()
    build_contact()
    build_blog()
