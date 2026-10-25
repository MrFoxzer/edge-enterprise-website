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

// Lead guard (_lib/lead-guard.js, shared by all of Jacob's sites): bots that
// never ran the page's JavaScript (no `human` token from js/human-check.js),
// foreign-language runs, "I wanted to know your price", adult/casino/SEO spam.
// Anything it does not deliver gets no phone push; the submission itself is
// still in the Netlify Forms dashboard for review.
const { triage } = require("./_lib/lead-guard.js");

// Fields that are not the visitor's own words (Netlify metadata, the honeypot,
// the token, fixed values, file uploads), or are passed to triage() by name.
const NOT_TEXT = new Set([
  "name", "email", "phone", "message", "work-summary", "human", "bot-field", "form-name",
  "ip", "user_agent", "referrer", "subject", "application-consent", "language", "plans", "resume",
]);

function leadGuard(form, d) {
  const text = Object.entries(d)
    .filter(([k, v]) => !NOT_TEXT.has(k) && typeof v === "string")
    .map(([, v]) => v)
    .join("\n");
  const fields = { name: d.name, email: d.email, phone: d.phone, message: d.message || d["work-summary"], text };
  const opts = { human: d.human, honeypot: d["bot-field"], nonEnglish: "drop" };
  const verdict = triage(fields, opts);
  // careers.html invites Spanish ("¿Hablas español? Aplica aquí", "Puede
  // responder en español"), so a Spanish application from someone who picked
  // Español is judged on everything except its language. triage() only gets to
  // the language test after the spam-word, price-template and link tests have
  // passed, so re-running it without the free text still requires the human
  // token, a real phone and a real name.
  if (form === "employment-application" && verdict.action === "drop" && verdict.reason === "not English" &&
      /^espa/i.test(String(d.language || ""))) {
    return triage({ ...fields, message: "", text: "" }, opts);
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
