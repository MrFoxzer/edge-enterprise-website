# Fargo–Moorhead Hiring Launch Checklist

Use this checklist before the recruitment campaign goes live. The destination for every channel is `/careers` (public URL: `https://edgeenterprise.net/careers`).

## Application and notifications

- [ ] Confirm the Netlify form is named `employment-application` and appears in the Netlify Forms dashboard.
- [ ] Configure form-submission notifications to the responsible hiring inbox; confirm the recipients and escalation owner.
- [ ] Use one safe dummy résumé (no real applicant data) for one real end-to-end test submission; it must be a PDF, DOC, or DOCX and no larger than 5 MB.
- [ ] Confirm the dummy submission creates a dashboard record, opens the uploaded file for an authorized hiring user, reaches `/application-received`, and sends the configured email notification to the responsible hiring inbox.
- [ ] Delete the dummy dashboard submission and dummy file after verification, then remove the related test notification artifacts according to the company's retention process.
- [ ] Name the owner for résumé-dashboard access and secure that account with MFA; grant only individual, least-privilege access to the hiring team.
- [ ] Name the owner for résumé retention and deletion; document the approved retention schedule and deletion method before launch.
- [ ] Confirm no résumé data is handled through public comments or direct messages.

## Careers-page quality check

- [ ] On a mobile phone, confirm the careers page, role selector, résumé upload, error message, and submit button are usable without horizontal scrolling.
- [ ] With a keyboard only, tab from the skip link through the navigation and form; verify each control has a visible focus state and the résumé error is announced.
- [ ] With reduced motion enabled, confirm the page remains usable and no essential information depends on motion.
- [ ] Check page and campaign copy for spelling, exact role names, required CTA text, and intact links before approval.
- [ ] Confirm privacy copy is present, the form does not ask for sensitive information beyond the application, and résumé access/retention controls match the documented owners.
- [ ] Confirm the page states the exact roles: Framing Carpenter and Framing Laborer.
- [ ] Confirm both roles are described as full-time in Fargo–Moorhead and require prior framing knowledge or experience.
- [ ] Confirm the form accepts one PDF, DOC, or DOCX résumé up to 5 MB.

## Content, legal, and platform review

- [ ] Use only approved project photography, the Edge Enterprise logo, and the approved dark/gold, Inter, and Playfair Display presentation.
- [ ] Confirm every asset uses the single CTA: “Apply with a résumé at https://edgeenterprise.net/careers.”
- [ ] Confirm copy does not invent pay, benefits, schedules, travel, certifications, a start date, or unverified company claims.
- [ ] **LAUNCH BLOCKER — before any production publication or paid promotion in Moorhead:** document whether the company meets Minnesota's 30-employee threshold. If it does, add the required salary-range and benefits/other-compensation disclosure to every job posting before approval.
- [ ] Confirm nobody asks for or uses applicant pay history to determine compensation.
- [ ] In Meta Ads Manager, select the Employment Special Ad Category and remove prohibited demographic or protected-characteristic targeting and proxy targeting.
- [ ] Use objective, role-related qualification language only; retain the same screening criteria for all applicants.

## URLs, measurement, and approval

- [ ] Use these final, campaign-ready URLs; each preserves the required `/careers` destination:
  - Skilled craft: `https://edgeenterprise.net/careers?utm_source=meta&utm_medium=paid_social&utm_campaign=fargo_moorhead_hiring&utm_content=skilled_craft`
  - Local full-time opportunity: `https://edgeenterprise.net/careers?utm_source=meta&utm_medium=paid_social&utm_campaign=fargo_moorhead_hiring&utm_content=local_full_time`
  - Family-owned integrity and precision: `https://edgeenterprise.net/careers?utm_source=meta&utm_medium=paid_social&utm_campaign=fargo_moorhead_hiring&utm_content=family_integrity_precision`
- [ ] Record the assigned final URL and campaign owner in the launch tracker; do not create substitute campaign destinations.
- [ ] Test every final destination URL in a private browser window and confirm it loads `/careers` over HTTPS.
- [ ] Review the live-form dashboard and notification configuration one final time after the test submission.
- [ ] Define the conversion/logging plan before launch: record each channel/angle UTM, landing-page visit, form start, valid form submission, dashboard receipt, and qualified-contact outcome in the launch tracker; review only aggregated campaign results outside the restricted hiring team.
- [ ] Assign a campaign owner to review delivery, destination links, form/dashboard receipt, notifications, UTM-attributed conversions, and privacy/access issues daily for the first 7 days. Record findings and pause or correct any broken route, notification, or privacy issue immediately.
- [ ] Get production approval from the designated owner after legal/payroll, creative, destination, and measurement checks are complete.
- [ ] Publish only after the production approver records approval and the responsible hiring owner confirms they can receive and review applications.
