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

    const skip = new Set(["ip", "user_agent", "referrer", "bot-field", "form-name", "subject"]);
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
