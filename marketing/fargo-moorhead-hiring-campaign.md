# Fargo–Moorhead Hiring Campaign

## Campaign objective and non-negotiables

Recruit qualified applicants for the full-time **Framing Carpenter** and **Framing Laborer** roles in the Fargo–Moorhead area. Every paid or organic placement must use this one CTA and destination: **Apply with a résumé at https://edgeenterprise.net/careers.** Do not route applicants to direct messages, comments, a phone number, or another form.

Both roles require prior framing knowledge or experience. Compensation and job details are provided upon contact. Do not add unverified pay, benefits, schedules, travel, certifications, start dates, guarantees, founding dates, state counts, or geographic claims.

## Three recruitment angles

1. **Skilled craft** — For people who value precise framing work and can bring prior framing knowledge or experience to the job.
2. **Local full-time opportunity** — For qualified applicants seeking full-time framing work in the Fargo–Moorhead area.
3. **Family-owned integrity and precision** — For qualified applicants drawn to a family-owned construction company and a direct, hardworking approach grounded in integrity and precision.

Use existing Edge Enterprise project photography only; avoid stock employee imagery. Pair the creative with the dark/gold palette, Inter body type, and Playfair Display accents used on the careers experience.

## Platform-ready copy

### Meta / Instagram 1 — Skilled craft

#### Meta 1 primary text (289 characters)

```text
Know framing? Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles for commercial and multi-family wood and steel framing in Fargo–Moorhead. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

#### Meta 1 headline (32 characters)

```text
Bring Your Framing Skill to Edge
```

#### Meta 1 description (79 characters)

```text
Full-time Fargo–Moorhead roles; prior framing knowledge or experience required.
```

#### Meta 1 CTA button (9 characters)

```text
Apply Now
```

CTA destination: `https://edgeenterprise.net/careers`

### Meta / Instagram 2 — Local full-time opportunity

#### Meta 2 primary text (301 characters)

```text
Looking for full-time framing work in Fargo–Moorhead? Edge Enterprise LLC is hiring for the Framing Carpenter and Framing Laborer roles for commercial and multi-family wood and steel framing. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

#### Meta 2 headline (40 characters)

```text
Full-Time Framing Work in Fargo–Moorhead
```

#### Meta 2 description (77 characters)

```text
Framing Carpenter and Framing Laborer opportunities with Edge Enterprise LLC.
```

#### Meta 2 CTA button (9 characters)

```text
Apply Now
```

CTA destination: `https://edgeenterprise.net/careers`

### Meta / Instagram 3 — Family-owned integrity and precision

#### Meta 3 primary text (338 characters)

```text
Bring your framing experience to a family-owned construction company that values hard work, integrity, and precision. Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles in Fargo–Moorhead. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

#### Meta 3 headline (34 characters)

```text
Frame With Integrity and Precision
```

#### Meta 3 description (75 characters)

```text
Family-owned Edge Enterprise is hiring qualified framers in Fargo–Moorhead.
```

#### Meta 3 CTA button (9 characters)

```text
Apply Now
```

CTA destination: `https://edgeenterprise.net/careers`

### LinkedIn / Indeed-style job post (796 characters)

```text
Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles in the Fargo–Moorhead area.

Our work includes commercial and multi-family wood and steel framing. We are looking for applicants who bring prior framing knowledge or experience and a hardworking, precise approach to assigned project work.

For the Framing Carpenter role, applicants will complete assigned wood and steel framing work. For the Framing Laborer role, applicants will assist with assigned wood and steel framing tasks and support commercial and multi-family project work.

Edge Enterprise is a family-owned construction company. We value integrity, precision, and excellence. Compensation and job details are provided upon contact.

Apply with a résumé at https://edgeenterprise.net/careers.
```

### Shareable / SMS version (159 characters)

```text
Full-time Framing Carpenter and Framing Laborer jobs in Fargo-Moorhead. Framing experience required. Apply with a resume at https://edgeenterprise.net/careers.
```

### Suggested image alt text (109 characters)

```text
Wood framing in progress on an Edge Enterprise commercial or multi-family project in the Fargo–Moorhead area.
```

### Organic Facebook / Instagram caption (218 characters)

```text
Fargo–Moorhead: Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

## Character-count verification

Counts above include spaces, punctuation, paragraph breaks, and the URL; they exclude the Markdown fence line breaks. Run this from the repository root after any copy edit. This verifies each individual Meta/Instagram field, rather than only a combined ad block.

```bash
node - <<'NODE'
const fs = require('node:fs');
const source = fs.readFileSync('marketing/fargo-moorhead-hiring-campaign.md', 'utf8');
const blocks = [...source.matchAll(/^#{3,4} (.+?) \((\d+) characters\)\n\n```text\n([\s\S]*?)\n```/gm)];
let failed = false;
for (const [, title, stated, copy] of blocks) {
  const actual = [...copy].length;
  console.log(`${title}: stated ${stated}, actual ${actual}`);
  failed ||= actual !== Number(stated);
}
if (blocks.length !== 16 || failed) process.exitCode = 1;
NODE
```

Verified output:

```text
Meta 1 primary text: stated 289, actual 289
Meta 1 headline: stated 32, actual 32
Meta 1 description: stated 79, actual 79
Meta 1 CTA button: stated 9, actual 9
Meta 2 primary text: stated 301, actual 301
Meta 2 headline: stated 40, actual 40
Meta 2 description: stated 77, actual 77
Meta 2 CTA button: stated 9, actual 9
Meta 3 primary text: stated 338, actual 338
Meta 3 headline: stated 34, actual 34
Meta 3 description: stated 75, actual 75
Meta 3 CTA button: stated 9, actual 9
LinkedIn / Indeed-style job post: stated 796, actual 796
Shareable / SMS version: stated 159, actual 159
Suggested image alt text: stated 109, actual 109
Organic Facebook / Instagram caption: stated 218, actual 218
```

## Publishing guardrails

**LAUNCH BLOCKER — do not publish in production or paid-promote in Moorhead until Edge Enterprise has determined whether it meets Minnesota's 30-employee threshold and, if covered, added the required salary-range and benefits/other-compensation disclosure to every job posting.**

- **Meta employment ads:** In Ads Manager, select the **Employment** Special Ad Category before building the campaign. Meta requires this category for employment ads; see its [Special Ad Category guidance](https://www.facebook.com/business/help/298000447747885) and [ads fairness update](https://about.fb.com/news/2023/01/an-update-on-our-ads-fairness-efforts/).
- **No targeting shortcuts:** Do not target or exclude people by age, gender, race, ethnicity, religion, disability, family status, ZIP code, or other protected-characteristic proxies. Do not write creative that signals a preference for, exclusion of, or assumption about a protected group. Keep location and qualification language job-related and objective. See the [EEOC's prohibited employment policies and practices](https://www.eeoc.gov/prohibited-employment-policiespractices).
- **Pay disclosure decision:** Minnesota's job-posting salary-range and benefits-disclosure requirement applies to employers with 30 or more employees at one or more Minnesota sites. Confirm Edge Enterprise's covered employee count with the owner or counsel before publishing. If covered, add the required starting salary range and general description of benefits and other compensation to each posting; do not substitute "provided upon contact." Primary source: [Minn. Stat. § 181.173](https://www.revisor.mn.gov/statutes/cite/181.173).
- **Pay history:** Do not ask for, seek, require, or use an applicant's pay history to determine compensation. Applicants may voluntarily disclose it without prompting in negotiation, subject to the statute. Primary source: [Minnesota Department of Human Rights pay-history guidance](https://mn.gov/mdhr/employers/pay-history/).
- **Objective qualifications:** Use only the stated, job-related requirement: prior framing knowledge or experience. Evaluate résumés against the selected role, framing knowledge or experience, and ability to work full-time in Fargo–Moorhead. Document the same criteria for every applicant.
- **Résumé privacy:** Send applicants only to the careers form. Never request résumés or personal details in public comments or direct messages. Limit form-dashboard access to the hiring team, use individual access, do not download résumés to personal devices, and delete or retain submissions only under the company's approved retention process. The initial form must not solicit Social Security numbers, birth dates, financial information, medical information, or identity documents. Follow the FTC's [Protecting Personal Information: A Guide for Business](https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business).

This is an operational checklist, not legal advice. Obtain a final legal and payroll review before launch.
