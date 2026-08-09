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

### Meta / Instagram 1 — Skilled craft (289 characters)

```text
Know framing? Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles for commercial and multi-family wood and steel framing in Fargo–Moorhead. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

### Meta / Instagram 2 — Local full-time opportunity (301 characters)

```text
Looking for full-time framing work in Fargo–Moorhead? Edge Enterprise LLC is hiring for the Framing Carpenter and Framing Laborer roles for commercial and multi-family wood and steel framing. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

### Meta / Instagram 3 — Family-owned integrity and precision (338 characters)

```text
Bring your framing experience to a family-owned construction company that values hard work, integrity, and precision. Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles in Fargo–Moorhead. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

### LinkedIn / Indeed-style job post (796 characters)

```text
Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles in the Fargo–Moorhead area.

Our work includes commercial and multi-family wood and steel framing. We are looking for applicants who bring prior framing knowledge or experience and a hardworking, precise approach to assigned project work.

For the Framing Carpenter role, applicants will complete assigned wood and steel framing work. For the Framing Laborer role, applicants will assist with assigned wood and steel framing tasks and support commercial and multi-family project work.

Edge Enterprise is a family-owned construction company. We value integrity, precision, and excellence. Compensation and job details are provided upon contact.

Apply with a résumé at https://edgeenterprise.net/careers.
```

### Shareable / SMS version (220 characters)

```text
Edge Enterprise LLC is hiring for the full-time Framing Carpenter and Framing Laborer roles in Fargo–Moorhead. Prior framing knowledge or experience is required. Apply with a résumé at https://edgeenterprise.net/careers.
```

### Suggested image alt text (109 characters)

```text
Wood framing in progress on an Edge Enterprise commercial or multi-family project in the Fargo–Moorhead area.
```

## Character-count verification

Counts above include spaces, punctuation, paragraph breaks, and the URL; they exclude the Markdown fence line breaks. Run this from the repository root after any copy edit:

```bash
node - <<'NODE'
const fs = require('node:fs');
const source = fs.readFileSync('marketing/fargo-moorhead-hiring-campaign.md', 'utf8');
const blocks = [...source.matchAll(/^### (.+?) \((\d+) characters\)\n\n```text\n([\s\S]*?)\n```/gm)];
let failed = false;
for (const [, title, stated, copy] of blocks) {
  const actual = [...copy].length;
  console.log(`${title}: stated ${stated}, actual ${actual}`);
  failed ||= actual !== Number(stated);
}
if (blocks.length !== 6 || failed) process.exitCode = 1;
NODE
```

Verified output:

```text
Meta / Instagram 1 — Skilled craft: stated 289, actual 289
Meta / Instagram 2 — Local full-time opportunity: stated 301, actual 301
Meta / Instagram 3 — Family-owned integrity and precision: stated 338, actual 338
LinkedIn / Indeed-style job post: stated 796, actual 796
Shareable / SMS version: stated 220, actual 220
Suggested image alt text: stated 109, actual 109
```

## Publishing guardrails

- **Meta employment ads:** In Ads Manager, select the **Employment** Special Ad Category before building the campaign. Meta requires the applicable Special Ad Category for employment-related campaigns. See Meta's [campaign setup guidance](https://www.facebook.com/help/messenger-app/621956575422138/) and [Instagram boosting guidance](https://www.facebook.com/help/instagram/570215404599013).
- **No targeting shortcuts:** Do not target or exclude people by age, gender, race, ethnicity, religion, disability, family status, ZIP code, or other protected-characteristic proxies. Do not write creative that signals a preference for, exclusion of, or assumption about a protected group. Keep location and qualification language job-related and objective.
- **Pay disclosure decision:** Minnesota's job-posting salary-range and benefits-disclosure requirement applies to employers with 30 or more employees at one or more Minnesota sites. Confirm Edge Enterprise's covered employee count with the owner or counsel before publishing. If covered, add the required starting salary range and general description of benefits/other compensation to each posting; do not substitute "provided upon contact." Primary source: [Minnesota Session Laws 2024, chapter 110](https://www.revisor.mn.gov/laws/2024/0/110/laws.2.1.0).
- **Pay history:** Do not ask for, seek, require, or use an applicant's pay history to determine compensation. Applicants may voluntarily disclose it without prompting in negotiation, subject to the statute. Primary source: [Minn. Stat. § 363A.08, subd. 8](https://www.revisor.mn.gov/statutes/2024/cite/363A.08).
- **Objective qualifications:** Use only the stated, job-related requirement: prior framing knowledge or experience. Evaluate résumés against the selected role, framing knowledge or experience, and ability to work full-time in Fargo–Moorhead. Document the same criteria for every applicant.
- **Résumé privacy:** Send applicants only to the careers form. Never request résumés or personal details in public comments or direct messages. Limit form-dashboard access to the hiring team, use individual access, do not download résumés to personal devices, and delete or retain submissions only under the company's approved retention process. The initial form must not solicit Social Security numbers, birth dates, financial information, medical information, or identity documents.

This is an operational checklist, not legal advice. Obtain a final legal and payroll review before launch.
