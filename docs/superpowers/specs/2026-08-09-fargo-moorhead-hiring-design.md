# Fargo–Moorhead Hiring Rollout Design

## Objective

Add a professional hiring experience to the real Edge Enterprise website for full-time framing carpenters and framing laborers with prior framing knowledge or experience in the Fargo–Moorhead area. Applicants must be able to apply through the website and attach a résumé.

The user asked for a complete first version built with professional judgment and will request changes after reviewing it, so implementation proceeds without an intermediate approval pause.

## Confirmed Requirements

- Roles: framing carpenters and framing laborers.
- Employment: full-time.
- Location: Fargo–Moorhead area.
- Experience: prior framing knowledge or experience is required.
- Compensation: contact Edge Enterprise for details; do not invent wages, benefits, schedules, travel, certifications, or a start date.
- Application: through the Edge Enterprise website with a résumé.
- Voice: direct, skilled, hardworking, precise, and professional.

## Architecture

The existing site is a static HTML/CSS/JavaScript project deployed on Netlify. The hiring experience will use the same architecture:

1. A dedicated `careers.html` page provides job details and a résumé application form.
2. The form uses Netlify Forms with `multipart/form-data`, an explicit form name, a honeypot, and a native POST to `/application-received`.
3. A dedicated `careers.js` validates PDF/DOC/DOCX files up to 5 MB before native submission; the server-side Netlify request limit remains 8 MB.
4. `application-received.html` confirms a successful submission.
5. The homepage adds a visible Careers navigation link and a concise hiring banner that routes candidates to `/careers`.
6. Netlify retains submitted fields and résumé files in the existing project dashboard; no separate public admin interface is introduced.

## Candidate Page

The careers page must include:

- a hero using Edge Enterprise’s real logo, project photography, and the existing dark/gold design system;
- both full-time roles and the Fargo–Moorhead location above the fold;
- objective responsibilities and qualifications without unsupported claims;
- a four-step process: submit résumé, review, contact qualified applicants, discuss compensation and details;
- a labeled, keyboard-accessible form with visible focus states and an accessible error/status region;
- a concise equal-opportunity statement and safe résumé privacy guidance.

The form collects only name, email, phone, desired role, years of framing experience, a short framing-work summary, and one résumé file. It must not request a Social Security number, birth date, medical information, financial information, photograph, or identity documents.

## Visual Direction

- Reuse the current CSS palette: `#D4A853`, `#B8922E`, `#E8C876`, `#0A0A0A`, and `#111111`.
- Preserve the real logo’s orange-to-red gradient without recoloring it.
- Use Inter for interface/body text and Playfair Display for editorial accents.
- Reuse real project photography; do not imply stock-photo workers are Edge employees.
- Override the current hidden desktop cursor on the careers page so native pointers remain available.
- Respect `prefers-reduced-motion`, maintain 44 px touch targets, and prevent horizontal overflow.

## Compliance Guardrails

- Use gender-neutral, job-related qualifications and an equal-opportunity statement.
- Do not target or discourage applicants based on protected characteristics.
- Paid Meta recruitment campaigns must use the Employment Special Ad Category.
- Minnesota pay-transparency law applies to employers with 30 or more employees at one or more Minnesota sites. Before public promotion in Moorhead, Edge must confirm its coverage status; a covered employer must replace “contact for details” with good-faith pay ranges and a general benefits/other-compensation description for each role.
- Do not ask applicants for pay history in a Minnesota hiring process.

## Deliverables

- Careers page, application-received page, homepage Careers promotion, and functional Netlify résumé form.
- Automated tests for page contract and résumé validation.
- Branded social recruitment card.
- Ready-to-post Meta/Instagram, LinkedIn/Indeed, and short shareable copy with publishing guardrails.
- Netlify draft deployment on the existing Edge Enterprise project for review; production remains unchanged until the user approves.

## Acceptance Criteria

- Both roles, full-time status, Fargo–Moorhead location, and experience requirement are obvious above the fold.
- The deployed Netlify build detects the `employment-application` form.
- The form accepts one PDF/DOC/DOCX résumé up to 5 MB and rejects unsupported or oversized files in the browser.
- Successful native submission routes to `/application-received`.
- Homepage visitors can reach `/careers` from both navigation and a visible hiring banner.
- No unsupported compensation, benefit, schedule, travel, certification, or company-history claim is added.
- Automated tests pass, HTML links/assets resolve in the draft deploy, and production is not modified.

