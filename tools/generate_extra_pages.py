#!/usr/bin/env python3
"""Extra pages: for-gcs, estimate calculator, Rogers case study, locations index."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_core_pages import head, hero, CTA_BAND, NAV, FOOTER, write


def build_for_gcs():
    schema = """    {
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "Subcontractor Prequalification - Edge Enterprise LLC",
      "url": "https://edgeenterprise.net/for-gcs.html"
    }"""
    body = hero("FOR GENERAL CONTRACTORS",
                'Prequalify Edge in <span class="text-accent">One Stop</span>',
                "Everything your estimating and compliance team needs to add Edge Enterprise to your bid list — no phone tag required.") + """
    <section class="section section-city-context">
        <div class="container">
            <div class="city-context-grid">
                <div class="city-context-main">
                    <span class="section-label">PREQUALIFICATION PACKAGE</span>
                    <h2 class="section-title">The Paperwork, <span class="text-accent">Handled</span></h2>
                    <div class="city-context-body">
                        <p><strong>Entity:</strong> Edge Enterprises, LLC — Minnesota limited liability company, family-owned and crew-operated. Headquarters: 15763 221st Ave, Long Prairie, MN 56347. Satellite presence: Horace, ND.</p>
                        <p><strong>Trade scope:</strong> Rough carpentry / structural framing (wood and light-gauge steel), multi-family and commercial, plus finished carpentry, window installation, and weather-barrier (Zip System / housewrap) packages — turn-key framed shells under one subcontract.</p>
                        <p><strong>Track record:</strong> 1,000+ multi-family units framed with repeat GC partners including Comeland Builders, Gast Construction, and Miller Architects &amp; Builders. Recent work includes the Rogers Senior Living &amp; Senior Center (Rogers, MN) and 45th Street Apartments (Fargo, ND).</p>
                        <p><strong>Insurance:</strong> Commercial general liability, automobile, umbrella, and statutory workers' compensation. Certificates of insurance with additional-insured endorsements (ISO CG&nbsp;20&nbsp;10 / CG&nbsp;20&nbsp;37) issued before mobilization. <strong>W-9, COI, and license details available on request</strong> — same business day.</p>
                        <p><strong>Payroll compliance:</strong> Certified payroll and prevailing-wage experience (Minnesota §§ 177.41–177.44), weekly reporting, IC-134 closeout affidavits.</p>
                        <p><strong>Crew capacity:</strong> Production framing crews with working foremen; crew sizes written into the subcontract as commitments — ask our references whether the milestones held.</p>
                    </div>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>Quick Facts</h3>
                        <ul>
                            <li><strong>Trade</strong><span>Framing / rough carpentry</span></li>
                            <li><strong>Units framed</strong><span>1,000+</span></li>
                            <li><strong>Markets</strong><span>MN · ND · WI · MT</span></li>
                            <li><strong>Bid response</strong><span>24 hours</span></li>
                            <li><strong>Email</strong><span><a href="mailto:Office@edgeenterprise.net" style="color:var(--primary)">rtrigueros@…</a></span></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>
    <section class="section section-city-context">
        <div class="container">
            <div class="section-header">
                <span class="section-label">GET US ON YOUR BID LIST</span>
                <h2 class="section-title">Add Edge to Your <span class="text-accent">Bid List</span></h2>
                <p class="section-subtitle">Tell us who to send bids and quals to — we reply with our full prequalification package.</p>
            </div>
            <form class="contact-form" name="bid-list" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="bot-field" style="max-width:640px;margin:24px auto 0">
                <input type="hidden" name="form-name" value="bid-list">
                <p style="display:none"><label>Don't fill this out: <input name="bot-field"></label></p>
                <div class="form-group"><input type="text" id="gcName" name="name" required placeholder=" "><label for="gcName">Your Name</label><div class="form-line"></div></div>
                <div class="form-group"><input type="text" id="gcCompany" name="company" required placeholder=" "><label for="gcCompany">GC / Company</label><div class="form-line"></div></div>
                <div class="form-group"><input type="email" id="gcEmail" name="email" required placeholder=" "><label for="gcEmail">Estimating Email</label><div class="form-line"></div></div>
                <div class="form-group"><input type="text" id="gcMarkets" name="markets" placeholder=" "><label for="gcMarkets">Markets / project types you bid</label><div class="form-line"></div></div>
                <button type="submit" class="btn btn-primary btn-large"><span>Request Prequal Package</span></button>
            </form>
        </div>
    </section>"""
    write("for-gcs.html", head("Subcontractor Prequalification for GCs | Edge Enterprise LLC",
                               "Add Edge Enterprise to your bid list: framing subcontractor prequalification — insurance, certified payroll capability, 1,000+ units framed, references from repeat GC partners.",
                               "for-gcs.html", schema) + NAV + body + FOOTER)


def build_estimate():
    schema = """    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "Framing Cost Ballpark Calculator",
      "url": "https://edgeenterprise.net/estimate.html",
      "applicationCategory": "Calculator",
      "provider": { "@type": "GeneralContractor", "name": "Edge Enterprise LLC" }
    }"""
    body = hero("INSTANT BALLPARK",
                'Framing Cost <span class="text-accent">Calculator</span>',
                "A 30-second ballpark for budgeting and feasibility — firm numbers still come from your plans.") + """
    <section class="section section-city-context">
        <div class="container">
            <div class="city-context-grid">
                <div class="city-context-main">
                    <div class="city-spec-card" style="position:static;max-width:640px">
                        <h3>Project Inputs</h3>
                        <div style="display:grid;gap:18px;margin-top:18px">
                            <label style="display:block">Framed area (square feet)
                                <input type="number" id="calcSqft" value="20000" min="500" step="500" style="width:100%;margin-top:6px;padding:12px;background:var(--dark);border:1px solid var(--dark-5);color:var(--light);border-radius:8px">
                            </label>
                            <label style="display:block">Project type
                                <select id="calcType" style="width:100%;margin-top:6px;padding:12px;background:var(--dark);border:1px solid var(--dark-5);color:var(--light);border-radius:8px">
                                    <option value="multi">Multi-family (repetitive units)</option>
                                    <option value="commercial">Commercial (office/retail/hospitality)</option>
                                    <option value="custom">Custom home / one-off</option>
                                </select>
                            </label>
                            <label style="display:block">Structure
                                <select id="calcStruct" style="width:100%;margin-top:6px;padding:12px;background:var(--dark);border:1px solid var(--dark-5);color:var(--light);border-radius:8px">
                                    <option value="wood">Wood frame</option>
                                    <option value="steel">Light-gauge steel</option>
                                    <option value="hybrid">Hybrid wood + steel</option>
                                </select>
                            </label>
                            <label style="display:block">Scope
                                <select id="calcScope" style="width:100%;margin-top:6px;padding:12px;background:var(--dark);border:1px solid var(--dark-5);color:var(--light);border-radius:8px">
                                    <option value="labor">Labor only</option>
                                    <option value="turnkey">Turn-key (labor + sheathing/WRB + windows)</option>
                                </select>
                            </label>
                        </div>
                        <div id="calcOut" style="margin-top:24px;padding:20px;background:var(--dark);border:1px solid var(--primary);border-radius:12px">
                            <div style="font-size:13px;letter-spacing:2px;color:var(--gray-light)">BALLPARK RANGE</div>
                            <div id="calcRange" style="font-size:32px;font-weight:800;color:var(--primary);margin-top:6px">—</div>
                            <div id="calcPerSf" style="color:var(--gray-light);margin-top:4px">—</div>
                        </div>
                        <p style="color:var(--gray);font-size:13px;margin-top:14px">Ballpark only — regional labor rates, height, complexity, and schedule move real numbers. Firm pricing comes from your drawings, free, within a few business days.</p>
                    </div>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>Turn It Into a Real Number</h3>
                        <ul>
                            <li><strong>Send plans</strong><span><a href="/contact.html" style="color:var(--primary)">Free line-item quote →</a></span></li>
                            <li><strong>How we price</strong><span><a href="/blog/commercial-framing-cost-guide.html" style="color:var(--primary)">2026 cost guide →</a></span></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>
    <script>
    (function(){
        var rates = {
            multi:      { labor: [5.5, 9],  turnkey: [12, 22] },
            commercial: { labor: [6.5, 11], turnkey: [15, 30] },
            custom:     { labor: [8, 14],   turnkey: [18, 34] }
        };
        var structMult = { wood: 1, steel: 1.18, hybrid: 1.1 };
        function fmt(n){ return '$' + Math.round(n).toLocaleString(); }
        function calc(){
            var sf = Math.max(500, parseInt(document.getElementById('calcSqft').value || 0, 10));
            var t = document.getElementById('calcType').value;
            var st = document.getElementById('calcStruct').value;
            var sc = document.getElementById('calcScope').value;
            var r = rates[t][sc], m = structMult[st];
            var lo = sf * r[0] * m, hi = sf * r[1] * m;
            document.getElementById('calcRange').textContent = fmt(lo) + ' – ' + fmt(hi);
            document.getElementById('calcPerSf').textContent = '$' + (r[0]*m).toFixed(2) + ' – $' + (r[1]*m).toFixed(2) + ' per SF · ' + sf.toLocaleString() + ' SF';
        }
        ['calcSqft','calcType','calcStruct','calcScope'].forEach(function(id){
            document.getElementById(id).addEventListener('input', calc);
            document.getElementById(id).addEventListener('change', calc);
        });
        calc();
    })();
    </script>""" + CTA_BAND
    write("estimate.html", head("Framing Cost Calculator — Instant Ballpark | Edge Enterprise LLC",
                                "Free instant ballpark for commercial, multi-family, and custom framing costs — square footage x project type x wood or steel. Then send plans for a firm line-item quote.",
                                "estimate.html", schema) + NAV + body + FOOTER)


def build_rogers_case():
    canon = "projects/rogers-senior-living.html"
    schema = """    [{
      "@context": "https://schema.org",
      "@type": "VideoObject",
      "name": "Rogers Senior Living & Senior Center - Framing Flyover",
      "description": "Drone flyover of the Rogers Senior Living & Senior Center in Rogers, MN - full rough-carpentry framing scope by Edge Enterprise LLC.",
      "thumbnailUrl": "https://edgeenterprise.net/projects/rogers-senior-living-1.jpg",
      "uploadDate": "2026-08-18",
      "contentUrl": "https://edgeenterprise.net/projects/rogers-senior-living-flyover.mp4"
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://edgeenterprise.net/" },
        { "@type": "ListItem", "position": 2, "name": "Projects", "item": "https://edgeenterprise.net/projects.html" },
        { "@type": "ListItem", "position": 3, "name": "Rogers Senior Living & Senior Center", "item": "https://edgeenterprise.net/projects/rogers-senior-living.html" }
      ]
    }]"""
    body = hero("CASE STUDY · ROGERS, MN",
                'Rogers Senior Living <span class="text-accent">&amp; Senior Center</span>',
                "Full rough-carpentry framing scope — a 4-story senior living community with attached single-story senior center on Main Street in Rogers, Minnesota. GC: Miller Architects &amp; Builders.") + """
    <section class="section section-city-context">
        <div class="container">
            <video controls preload="metadata" poster="/projects/rogers-senior-living-1.jpg" style="width:100%;border-radius:16px;border:1px solid var(--dark-4)">
                <source src="/projects/rogers-senior-living-flyover.mp4" type="video/mp4">
            </video>
            <div class="city-context-grid" style="margin-top:48px">
                <div class="city-context-main">
                    <span class="section-label">THE WORK</span>
                    <h2 class="section-title">What Edge <span class="text-accent">Delivered</span></h2>
                    <div class="city-context-body">
                        <p>Edge Enterprise carried the complete rough-carpentry framing package on this senior living campus: wall panels, floor and roof sheathing, trusses, draft/fire/smoke stopping, sill sealing, exterior window and hollow-metal frame installation, Zip System taping through panel-field inspection, wood blocking for handrails, vanities, and wall-hung fixtures throughout, and daily-cleanup jobsite discipline under Miller Architects &amp; Builders' safety program.</p>
                        <p>The project pairs a 4-story wood-framed residential building with an attached single-story senior center — two different structural rhythms on one tight urban site along Main Street, with occupied businesses and live traffic on two sides.</p>
                        <p>Framing crews of 12+ carpenters with a working foreman held the GC's milestone schedule through the full scope — the same crew-size commitment we write into every subcontract.</p>
                    </div>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>Project Facts</h3>
                        <ul>
                            <li><strong>Location</strong><span>13001 Main St, Rogers, MN</span></li>
                            <li><strong>GC</strong><span>Miller Architects &amp; Builders</span></li>
                            <li><strong>Architect</strong><span>Cole Group Architects</span></li>
                            <li><strong>Type</strong><span>Senior living + senior center</span></li>
                            <li><strong>Structure</strong><span>4-story wood frame + 1-story wing</span></li>
                            <li><strong>Scope</strong><span>Full rough-carpentry framing</span></li>
                            <li><strong>Envelope</strong><span>Zip System, taped &amp; inspected</span></li>
                        </ul>
                    </div>
                </aside>
            </div>
            <div class="city-nearby-grid" style="margin-top:40px">
                <a href="/projects/rogers-senior-living-1.jpg" class="city-nearby-card glightbox" data-gallery="rogers-cs"><span class="city-nearby-state">PHOTO</span><h3>Aerial — street side</h3><span class="city-nearby-arrow">→</span></a>
                <a href="/projects/rogers-senior-living-2.jpg" class="city-nearby-card glightbox" data-gallery="rogers-cs"><span class="city-nearby-state">PHOTO</span><h3>Aerial — full campus</h3><span class="city-nearby-arrow">→</span></a>
                <a href="/projects/rogers-senior-living-4.jpg" class="city-nearby-card glightbox" data-gallery="rogers-cs"><span class="city-nearby-state">PHOTO</span><h3>Framing detail</h3><span class="city-nearby-arrow">→</span></a>
                <a href="/projects/rogers-senior-living-5.jpg" class="city-nearby-card glightbox" data-gallery="rogers-cs"><span class="city-nearby-state">PHOTO</span><h3>Senior center wing</h3><span class="city-nearby-arrow">→</span></a>
            </div>
        </div>
    </section>""" + CTA_BAND
    extra = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/css/glightbox.min.css">
    <script src="https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/js/glightbox.min.js" defer></script>
    <script>window.addEventListener('DOMContentLoaded',function(){ if (window.GLightbox) GLightbox({selector: '.glightbox'}); });</script>"""
    write(canon, head("Rogers Senior Living & Senior Center — Framing Case Study | Edge Enterprise LLC",
                      "Case study: Edge Enterprise framed the 4-story Rogers Senior Living & Senior Center in Rogers, MN under Miller Architects & Builders — full rough-carpentry scope with drone flyover video.",
                      canon, schema, extra) + NAV + body + FOOTER)


def build_locations_index():
    body = hero("SERVICE AREAS",
                'Where We <span class="text-accent">Frame</span>',
                "183 cities across four states — pick your state to find local specs, FAQs, and every service we offer in your market.") + """
    <section class="section section-city-nearby">
        <div class="container">
            <div class="city-nearby-grid">
                <a href="/locations/minnesota.html" class="city-nearby-card"><span class="city-nearby-state">MN</span><h3>Minnesota — HQ</h3><span class="city-nearby-arrow">→</span></a>
                <a href="/locations/north-dakota.html" class="city-nearby-card"><span class="city-nearby-state">ND</span><h3>North Dakota</h3><span class="city-nearby-arrow">→</span></a>
                <a href="/locations/wisconsin.html" class="city-nearby-card"><span class="city-nearby-state">WI</span><h3>Wisconsin</h3><span class="city-nearby-arrow">→</span></a>
                <a href="/locations/montana.html" class="city-nearby-card"><span class="city-nearby-state">MT</span><h3>Montana</h3><span class="city-nearby-arrow">→</span></a>
            </div>
        </div>
    </section>""" + CTA_BAND
    write("locations/index.html", head("Service Areas — MN, ND, WI, MT | Edge Enterprise LLC",
                                       "Edge Enterprise frames in 183 cities across Minnesota, North Dakota, Wisconsin, and Montana. Find your city for local framing specs and FAQs.",
                                       "locations/index.html") + NAV + body + FOOTER)


def build_faq():
    faqs = [
        ("What areas does Edge Enterprise serve?",
         "We're headquartered in Long Prairie, Minnesota with a satellite presence in Horace, North Dakota. Our crews frame across Minnesota, North Dakota, Wisconsin, and Montana — 183 cities and counting — and we travel nationwide for the right project."),
        ("What types of framing do you do?",
         "Full-scope structural framing: commercial wood and light-gauge steel framing, multi-family (apartments, townhomes, senior living), custom homes, framing subcontracting for GCs, finished carpentry, window installation, and weather-barrier packages (Zip System and housewrap) — turn-key framed shells under one subcontract."),
        ("How big are the projects you take on?",
         "Everything from garages and custom homes to 100+ unit multi-family buildings. We've framed more than 1,000 multi-family units, including the Rogers Senior Living & Senior Center and 45th Street Apartments in Fargo."),
        ("How do I get a quote?",
         "Fill out the form on our contact page — attach plans if you have them (PDF or ZIP). We respond within one business day with a call or email back from Jacob or Ramon directly. For a instant budgeting number first, try our free framing cost calculator."),
        ("How much does framing cost?",
         "As a 2026 rule of thumb in the Upper Midwest: wood-framed multi-family runs roughly $12-22 per square foot installed (labor + material), labor-only packages roughly $5.50-9 per square foot for multi-family, with commercial and custom work higher. Our estimate calculator gives you a project-specific ballpark in 30 seconds."),
        ("Do you work as a subcontractor for general contractors?",
         "Yes — framing subcontracting for GCs is our core business, with repeat partners including Comeland Builders, Gast Construction, and Miller Architects & Builders. See our For GCs page for the full prequalification package."),
        ("Are you licensed and insured?",
         "Yes. Edge Enterprises, LLC is licensed and insured, headquartered in Minnesota. We carry commercial general liability, automobile, umbrella, and statutory workers' compensation coverage — certificates of insurance with additional-insured endorsements are issued before mobilization, and our COI is available on request."),
        ("Can you frame through a Minnesota winter?",
         "Yes — our crews frame year-round. Cold-weather framing is standard practice for us: material staging, snow removal, and dry-in sequencing are planned so winter doesn't stall your schedule."),
        ("Do you handle prevailing-wage projects?",
         "Yes. We have certified payroll and prevailing-wage experience under Minnesota statutes 177.41-177.44, with weekly reporting and IC-134 closeout affidavits."),
        ("How far out are you booking?",
         "It varies by season — spring and summer crews book out furthest. Check the banner at the top of the site for current availability, or send your project through the contact form and we'll tell you exactly what our lead time looks like for your start date."),
        ("Do you supply materials or labor only?",
         "Both models. We run labor-only packages where the GC supplies the lumber package, and full labor-plus-material scopes. Turn-key packages add sheathing, weather barrier, and window installation under the same subcontract."),
        ("Who will actually be on my jobsite?",
         "Our own crews — we don't broker your frame to whoever's cheapest this month. Multi-family crews run 12+ carpenters with a working foreman on site for the duration, and that crew commitment is written into our subcontracts."),
    ]
    import json as _json
    faq_schema_items = ",\n".join(f"""        {{
          "@type": "Question",
          "name": {_json.dumps(q)},
          "acceptedAnswer": {{ "@type": "Answer", "text": {_json.dumps(a)} }}
        }}""" for q, a in faqs)
    schema = f"""    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
{faq_schema_items}
      ]
    }}"""
    LINKS = {
        "contact page": '<a href="/contact.html" style="color:var(--primary)">contact page</a>',
        "framing cost calculator": '<a href="/estimate.html" style="color:var(--primary)">framing cost calculator</a>',
        "estimate calculator": '<a href="/estimate.html" style="color:var(--primary)">estimate calculator</a>',
        "For GCs page": '<a href="/for-gcs.html" style="color:var(--primary)">For GCs page</a>',
        "Rogers Senior Living & Senior Center": '<a href="/projects/rogers-senior-living.html" style="color:var(--primary)">Rogers Senior Living &amp; Senior Center</a>',
    }
    cards = []
    for i, (q, a) in enumerate(faqs, 1):
        a_html = a
        for k, v in LINKS.items():
            a_html = a_html.replace(k, v, 1)
        cards.append(f"""                <div class="city-why-card">
                    <h3>{q}</h3>
                    <p>{a_html}</p>
                </div>""")
    body = hero("STRAIGHT ANSWERS",
                'Frequently Asked <span class="text-accent">Questions</span>',
                "The questions GCs, developers, and homeowners ask us most — answered the way we'd answer them on the phone.") + f"""
    <section class="section section-city-why">
        <div class="container">
            <div class="city-why-grid">
{chr(10).join(cards)}
            </div>
        </div>
    </section>""" + CTA_BAND
    write("faq.html", head("FAQ — Framing Costs, Coverage, Scheduling | Edge Enterprise LLC",
                           "Answers to the questions we hear most: framing costs per square foot, service areas, winter framing, prevailing wage, labor-only vs turn-key, and how to get a quote.",
                           "faq.html", schema) + NAV + body + FOOTER)


if __name__ == "__main__":
    build_faq()
    build_for_gcs()
    build_estimate()
    build_rogers_case()
    build_locations_index()
