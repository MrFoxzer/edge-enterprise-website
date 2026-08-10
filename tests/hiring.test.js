const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const root = path.join(__dirname, "..");
const read = (file) => fs.readFileSync(path.join(root, file), "utf8");

const careers = read("careers.html");
const careersCss = read("careers.css");
const home = read("index.html");
const styles = read("styles.css");
const success = read("application-received.html");
const { validateResume } = require(path.join(root, "careers.js"));

function blockAfter(source, marker) {
  const markerIndex = source.indexOf(marker);
  assert.notEqual(markerIndex, -1, `Missing ${marker}`);
  const openingBrace = source.indexOf("{", markerIndex + marker.length);
  assert.notEqual(openingBrace, -1, `Missing block for ${marker}`);
  let depth = 0;
  for (let index = openingBrace; index < source.length; index += 1) {
    if (source[index] === "{") depth += 1;
    if (source[index] === "}") depth -= 1;
    if (depth === 0) return source.slice(openingBrace + 1, index);
  }
  assert.fail(`Unclosed block for ${marker}`);
}

test("careers page exposes the complete Netlify resume form", () => {
  assert.match(careers, /name="employment-application"/);
  assert.match(careers, /method="POST"/);
  assert.match(careers, /data-netlify="true"/);
  assert.match(careers, /netlify-honeypot="bot-field"/);
  assert.match(careers, /enctype="multipart\/form-data"/);
  assert.match(careers, /action="\/application-received"/);
  [
    "form-name",
    "bot-field",
    "subject",
    "name",
    "email",
    "phone",
    "role",
    "experience-years",
    "work-summary",
    "resume",
    "application-consent",
  ].forEach((field) => assert.match(careers, new RegExp(`name="${field}"`)));
  assert.match(careers, /name="resume"[^>]*required/);
  assert.match(careers, /accept="\.pdf,\.doc,\.docx,application\/pdf,application\/msword,application\/vnd\.openxmlformats-officedocument\.wordprocessingml\.document"/);
  assert.match(careers, /Framing Carpenter/);
  assert.match(careers, /Framing Laborer/);
  assert.match(careers, /Fargo–Moorhead/);
});

test("careers page includes all confirmed role, process, privacy, and equal-opportunity copy", () => {
  [
    "Build With Precision. Work With Edge.",
    "Built on Skill. Grounded in Integrity.",
    "Submit your résumé",
    "We review your experience",
    "We contact qualified applicants",
    "Discuss compensation and job details",
    "Bring Your Framing Experience to Edge",
    "Edge Enterprise LLC is an equal opportunity employer.",
    "Apply privately through this form.",
  ].forEach((copy) => assert.match(careers, new RegExp(copy.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))));
});

test("rejects a resume larger than 5 MB", () => {
  assert.deepEqual(validateResume({ name: "resume.pdf", type: "application/pdf", size: 5 * 1024 * 1024 + 1 }), {
    valid: false,
    error: "Résumé must be 5 MB or smaller.",
  });
});

test("rejects a zero-byte PDF resume", () => {
  assert.deepEqual(validateResume({ name: "resume.pdf", type: "application/pdf", size: 0 }), {
    valid: false,
    error: "Résumé file cannot be empty.",
  });
});

test("accepts PDF, DOC, and DOCX resumes at or below 5 MB", () => {
  [
    { name: "resume.pdf", type: "application/pdf" },
    { name: "resume.doc", type: "application/msword" },
    { name: "resume.docx", type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" },
  ].forEach((file) => {
    assert.deepEqual(validateResume({ ...file, size: 5 * 1024 * 1024 }), { valid: true, error: "" });
  });
});

test("rejects unsupported resume file types", () => {
  assert.deepEqual(validateResume({ name: "resume.png", type: "image/png", size: 128 }), {
    valid: false,
    error: "Upload a PDF, DOC, or DOCX résumé.",
  });
});

test("rejects a resume with a disallowed extension even if its MIME is allowed", () => {
  assert.deepEqual(validateResume({ name: "resume.exe", type: "application/pdf", size: 128 }), {
    valid: false,
    error: "Upload a PDF, DOC, or DOCX résumé.",
  });
});

test("rejects a resume when its allowed extension and MIME do not match", () => {
  assert.deepEqual(validateResume({ name: "resume.docx", type: "application/pdf", size: 128 }), {
    valid: false,
    error: "Upload a PDF, DOC, or DOCX résumé.",
  });
});

test("rejects an inherited-property extension with an empty MIME", () => {
  assert.deepEqual(validateResume({ name: "resume.constructor", type: "", size: 128 }), {
    valid: false,
    error: "Upload a PDF, DOC, or DOCX résumé.",
  });
});

test("requires a resume file", () => {
  assert.deepEqual(validateResume(null), {
    valid: false,
    error: "Please attach your résumé.",
  });
});

test("homepage provides visible careers routes without replacing quote flow", () => {
  assert.match(home, /href="\/careers"[^>]*>Careers</);
  assert.match(home, /href="\/careers"[^>]*>Apply With Your Résumé</);
  assert.match(home, /id="contact"/);
});

test("application received page confirms the native application submission", () => {
  assert.match(success, /<main/);
  assert.match(success, /Application Received/);
  assert.match(success, /role="status"/);
  assert.match(success, /We review your experience/);
  assert.match(success, /href="\/careers"/);
});

test("careers page references the approved social card and accessibility essentials", () => {
  assert.match(careers, /property="og:image" content="[^\"]*hiring-social-card\.png"/);
  assert.match(careers, /property="og:image:alt" content="Edge Enterprise now hiring framing carpenters and framing laborers in Fargo–Moorhead over an aerial wood-framing project\."/);
  assert.match(careers, /property="og:image:width" content="1200"/);
  assert.match(careers, /property="og:image:height" content="628"/);
  assert.match(careers, /href="hiring-social-card\.png"/);
  assert.match(careers, /class="skip-link"/);
  assert.match(careers, /role="alert"/);
  assert.match(careers, /careers\.css/);
  assert.match(careers, /careers\.js/);
  assert.equal(fs.existsSync(path.join(root, "hiring-social-card.png")), true);
});

test("careers skip link and primary buttons keep dark text in every interaction state", () => {
  assert.match(blockAfter(careersCss, ".careers-page .skip-link"), /color:\s*var\(--black\)/);
  assert.match(
    careersCss,
    /\.careers-page \.skip-link:hover,\s*\.careers-page \.skip-link:focus\s*{[^}]*color:\s*var\(--black\)/,
  );
  assert.match(blockAfter(careersCss, ".careers-page .button-primary"), /color:\s*var\(--black\)/);
  assert.match(
    careersCss,
    /\.careers-page \.button-primary:hover,\s*\.careers-page \.button-primary:focus-visible\s*{[^}]*color:\s*var\(--black\)/,
  );
  assert.match(careersCss, /:focus-visible\s*{[^}]*outline:\s*3px solid var\(--gold-light\)/);
});

test("homepage switches to the existing overlay navigation throughout tablet widths", () => {
  const tabletStyles = blockAfter(styles, "@media (max-width: 1024px)");
  assert.match(blockAfter(tabletStyles, ".nav-links"), /position:\s*fixed/);
  assert.match(blockAfter(tabletStyles, ".nav-links"), /transform:\s*translateX\(100%\)/);
  assert.match(blockAfter(tabletStyles, ".nav-links.active"), /transform:\s*translateX\(0\)/);
  assert.match(blockAfter(tabletStyles, ".nav-toggle"), /display:\s*flex/);
});

test("homepage prevents entrance animations from creating tablet horizontal scroll", () => {
  assert.match(blockAfter(styles, "html"), /overflow-x:\s*hidden/);
  assert.match(blockAfter(styles, "body"), /overflow-x:\s*hidden/);
});
