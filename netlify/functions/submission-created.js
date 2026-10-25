// Runs automatically on every VERIFIED Netlify form submission (contact +
// employment-application). Delivers the lead by email (via ntfy.sh's email
// bridge) and to the private ntfy push topic, independent of Netlify's
// built-in notification emails.
//
// SECURITY: an ntfy.sh topic is a bearer secret, not an identifier. ntfy.sh
// has no read authentication on free topics — anyone who learns the string can
// subscribe to https://ntfy.sh/<topic> and silently receive every lead
// forever. This repository is PUBLIC, so the topic must never appear in
// source, in a fallback, in a comment, or in a committed config file.
//
// Set NTFY_TOPIC in Netlify: Site configuration -> Environment variables.
// There is deliberately NO fallback: if the variable is missing we skip the
// push and log loudly, rather than leaking or guessing a topic.
const NTFY_TOPIC = process.env.NTFY_TOPIC;

// Lead guard v2 (_lib/lead-guard.js + js/human-check.js, the same pair on all
// of Jacob's sites). A post with no `human` token (a bot that never ran the
// page's JavaScript) is dropped on any spam sign. A visitor who passed the
// check is never dropped over wording a real customer could write: pitches,
// links and odd phones only make it quiet. Only the honeypot, adult/drug spam
// and a non-English lead drop a verified post. Only 'deliver' gets the phone
// push; every submission, quiet ones included, stays in the Netlify Forms
// dashboard for review.
const { triage, language, normalize } = require("./_lib/lead-guard.js");

// Fields that are not the visitor's own words (Netlify metadata, the honeypot,
// the token, fixed values, file uploads), or are passed to triage() by name.
const NOT_TEXT = new Set([
  "name", "email", "phone", "message", "work-summary", "human", "bot-field", "form-name",
  "ip", "user_agent", "referrer", "subject", "application-consent", "language", "plans", "resume",
]);

// Job applications are never dropped over their language (Minnesota Human
// Rights Act: national origin in hiring). A non-English one is quiet: no push,
// still in the dashboard. The lead forms drop non-English (Jacob: "if it's a
// different language I don't even wanna get to see it").
const JOB_FORMS = new Set(["employment-application"]);

// The text with every word that makes language() call it non-English blanked
// out, links left whole. The guard keeps its word list private, so each word
// is asked about on its own (three copies: language() needs three foreign words).
function withoutForeignWords(s) {
  return normalize(s).replace(/\b(?:https?:\/\/|www\.)\S+|[\p{L}']+/giu, (w) =>
    (/^(?:https?:|www\.)/i.test(w) || language(`${w} ${w} ${w}`) !== "foreign" ? w : " "));
}

function leadGuard(form, d) {
  const text = Object.entries(d)
    .filter(([k, v]) => !NOT_TEXT.has(k) && typeof v === "string")
    .map(([, v]) => v)
    .join("\n");
  const fields = { name: d.name, email: d.email, phone: d.phone, message: d.message || d["work-summary"], text };
  const job = JOB_FORMS.has(form);
  const opts = { human: d.human, honeypot: d["bot-field"], nonEnglish: job ? "quiet" : "drop" };
  const verdict = triage(fields, opts);
  // careers.html invites Spanish ("¿Hablas español? Aplica aquí", "Puede
  // responder en español"), so an application from someone who picked Español
  // is judged on everything except its language. triage() tests the language
  // before links and pitches, so it runs again with the foreign words blanked
  // out: a link shortener, a pitch, look-alike letters, a fake phone or email
  // still keep it quiet. The reason is exactly "not English" only when the
  // human token is valid, so a bot never gets here.
  if (job && verdict.action === "quiet" && verdict.reason === "not English" &&
      /^espa/i.test(String(d.language || ""))) {
    return triage({ ...fields, message: withoutForeignWords(fields.message), text: withoutForeignWords(fields.text) }, opts);
  }
  return verdict;
}

exports.handler = async (event) => {
  try {
    if (!NTFY_TOPIC) {
      console.error(
        "NTFY_TOPIC is not set — push notification skipped. " +
        "Set it in Netlify: Site configuration -> Environment variables. " +
        "The submission itself is still recorded in Netlify Forms."
      );
      return { statusCode: 200, body: "notify-skipped-no-topic" };
    }

    const { payload } = JSON.parse(event.body);
    const form = payload.form_name || "unknown-form";
    const d = payload.data || {};

    const guard = leadGuard(form, d);
    if (guard.action !== "deliver") {
      console.log(`lead guard: ${guard.action} (${guard.reason}), form ${form}: no push`);
      return { statusCode: 200, body: `guard-${guard.action}` };
    }

    const skip = new Set(["ip", "user_agent", "referrer", "bot-field", "form-name", "subject", "human"]);
    const lines = Object.entries(d)
      .filter(([k, v]) => !skip.has(k) && v && typeof v === "string" && v.trim())
      .map(([k, v]) => `${k.toUpperCase()}: ${v}`);

    const title = form === "employment-application"
      ? `JOB APPLICATION: ${d.name || "unknown"}`
      : `NEW LEAD: ${d.name || "unknown"}`;
    const body =
      `${title}\nForm: ${form}\nReceived: ${payload.created_at}\n\n` +
      lines.join("\n") +
      `\n\nReply to: ${d.email || "n/a"}  |  Phone: ${d.phone || "n/a"}` +
      `\nAll submissions: https://app.netlify.com/projects/edge-enterprise/forms`;

    const posts = [];
    // instant push to the private topic (ntfy app subscribers)
    posts.push(fetch(`https://ntfy.sh/${NTFY_TOPIC}`, {
      method: "POST",
      headers: { Title: title, Priority: "high", Tags: "rotating_light" },
      body,
    }));

    const results = await Promise.allSettled(posts);
    console.log("delivery results:", results.map(r => r.status).join(","));
    return { statusCode: 200, body: "ok" };
  } catch (err) {
    console.error("notify failed:", err);
    return { statusCode: 200, body: "logged" };
  }
};
