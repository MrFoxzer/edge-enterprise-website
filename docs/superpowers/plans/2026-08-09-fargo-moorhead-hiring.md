# Fargo–Moorhead Hiring Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested, branded careers page with résumé submission to the real Edge Enterprise Netlify website, then prepare and privately preview the recruitment campaign.

**Architecture:** Static HTML/CSS/JavaScript stays consistent with the existing site. Netlify Forms receives multipart applications and résumé files; a small CommonJS-compatible browser script provides testable client validation while preserving native form submission.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, Node’s built-in test runner, Netlify Forms, Netlify CLI.

## Global Constraints

- Use the exact roles “Framing Carpenter” and “Framing Laborer.”
- Describe both roles as full-time in the Fargo–Moorhead area and require prior framing knowledge or experience.
- Compensation and job details are provided upon contact; do not invent pay, benefits, schedules, travel, certifications, or a start date.
- Accept one PDF, DOC, or DOCX résumé up to 5 MB through the website.
- Use the existing Edge Enterprise logo, first-party project photography, dark/gold palette, Inter body type, and Playfair Display accents.
- Do not repeat disputed live-site claims such as an exact founding date, a state count, “nationwide,” dual headquarters, 100% satisfaction, or unverified guarantees.
- Keep production unchanged; deliver a Netlify draft deploy for review.

---

### Task 1: Careers Experience and Netlify Application Form

**Files:**
- Modify: `package.json`
- Create: `tests/hiring.test.js`
- Create: `careers.html`
- Create: `careers.css`
- Create: `careers.js`
- Create: `application-received.html`
- Modify: `index.html`
- Modify: `styles.css`
- Create: `hiring-social-card.png`

**Interfaces:**
- Produces: `/careers`, `/application-received`, homepage hiring routes, and Netlify form `employment-application`.
- Produces: `validateResume(file)` returning `{ valid: boolean, error: string }` from `careers.js` for both browser behavior and Node tests.
- Consumes: existing `logo.png`, `logo-icon.png`, `projects/45th-street-comeland-1.jpg`, and the generated social-card source at `/Users/jacobfischer/.codex/generated_images/019fe8be-c10d-7b90-8cd1-c0d890b8a4fd/exec-754a5f9f-7cc1-4330-92db-8fb6c72029e7.png`.

- [ ] **Step 1: Write failing page and validation tests**

```js
test("careers page exposes the complete Netlify résumé form", async () => {
  assert.match(careers, /name="employment-application"/);
  assert.match(careers, /data-netlify="true"/);
  assert.match(careers, /enctype="multipart\/form-data"/);
  assert.match(careers, /action="\/application-received"/);
  assert.match(careers, /name="resume"/);
  assert.match(careers, /Framing Carpenter/);
  assert.match(careers, /Framing Laborer/);
  assert.match(careers, /Fargo–Moorhead/);
});

test("rejects a résumé larger than 5 MB", () => {
  assert.deepEqual(validateResume({ name: "resume.pdf", type: "application/pdf", size: 5 * 1024 * 1024 + 1 }), {
    valid: false,
    error: "Résumé must be 5 MB or smaller.",
  });
});
```

Add separate tests for allowed PDF/DOC/DOCX, unsupported file types, absent files, homepage `/careers` links, and the success page.

- [ ] **Step 2: Run tests and verify RED**

Run: `npm test`
Expected: FAIL because the careers artifacts and validation module do not exist.

- [ ] **Step 3: Implement the careers and success pages**

Use semantic `header`, `nav`, `main`, `section`, and `footer` landmarks; visible focus states; no fake employee imagery; and only verified company/hiring copy.

- [ ] **Step 4: Implement the Netlify form and résumé validation**

Use native multipart POST, hidden `form-name`, honeypot, one required résumé file, named fields, an accessible error region, and no AJAX interception for valid forms.

- [ ] **Step 5: Integrate homepage recruiting routes**

Add a visible Careers nav link and a homepage hiring banner with a primary link to `/careers` without changing the existing quote flow.

- [ ] **Step 6: Add and wire the social card**

Copy the approved generated image into the repository as `hiring-social-card.png`, resize to a 1.91:1 social-card shape, and reference it in careers Open Graph metadata.

- [ ] **Step 7: Run tests and verify GREEN**

Run: `npm test`
Expected: all hiring tests pass.

- [ ] **Step 8: Commit**

```bash
git add package.json tests careers.html careers.css careers.js application-received.html index.html styles.css hiring-social-card.png
git commit -m "feat: add Fargo-Moorhead hiring experience"
```

### Task 2: Recruitment Campaign Package

**Files:**
- Create: `marketing/fargo-moorhead-hiring-campaign.md`
- Create: `marketing/hiring-launch-checklist.md`

**Interfaces:**
- Produces: three distinct recruitment angles, platform-ready copy, character counts, compliance notes, and a launch checklist that points all traffic to `/careers`.

- [ ] **Step 1: Draft three distinct campaign angles**

Use skilled-craft, local full-time opportunity, and family-owned integrity/precision angles. Keep a single CTA: apply with a résumé at `https://edgeenterprise.net/careers`.

- [ ] **Step 2: Produce platform-ready copy**

Include three Meta/Instagram variants, one LinkedIn/Indeed-style job post, one short shareable/SMS version, and suggested image alt text. Verify every stated character count programmatically.

- [ ] **Step 3: Document publishing guardrails**

Include Meta Employment Special Ad Category setup, prohibited targeting shortcuts, Minnesota’s 30-employee pay-transparency threshold, pay-history restriction, objective qualification language, and résumé privacy practices with primary-source links.

- [ ] **Step 4: Write the launch checklist**

Cover form-notification setup, a real test submission, dashboard review, mobile/keyboard checks, pay-disclosure decision, campaign URL/UTM setup, and production approval.

- [ ] **Step 5: Self-review and commit**

```bash
git add marketing
git commit -m "docs: add hiring campaign and launch checklist"
```

### Task 3: Verification and Netlify Draft Deployment

**Files:**
- Modify only if verification finds a real defect in Task 1 or Task 2 artifacts.

**Interfaces:**
- Consumes: tested repository state and linked Netlify project.
- Produces: Netlify draft deployment URL and confirmation that `employment-application` was detected.

- [ ] **Step 1: Run the full automated suite**

Run: `npm test`
Expected: all tests pass with zero failures.

- [ ] **Step 2: Run a local static server smoke check**

Serve the repository and confirm status 200 for `/`, `/careers`, `/application-received`, required CSS/JS, the project hero, logo, and social card.

- [ ] **Step 3: Create a Netlify draft deploy**

Run: `netlify deploy --dir=.`
Expected: a unique draft URL on the linked `edge-enterprise` project; no production change.

- [ ] **Step 4: Confirm form detection and draft assets**

Use the Netlify API to list site forms and confirm `employment-application` exists. Fetch the draft pages/assets and confirm successful responses and the careers metadata.

- [ ] **Step 5: Commit verification fixes if any**

If files changed, commit only the verified fixes with a focused message. Otherwise preserve the Task 2 commit as the branch head.

