// Runs automatically on every VERIFIED Netlify form submission (contact +
// employment-application). Delivers the lead by email (via ntfy.sh's email
// bridge) and to the private ntfy push topic, independent of Netlify's
// built-in notification emails.
const NTFY_TOPIC = "edge-leads-f3b7085b406399e1";
const EMAILS = [
  "jacob@revisionsunlimited.com",
  "jacobfischer54@icloud.com",
];

exports.handler = async (event) => {
  try {
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
    // one email per address via ntfy's email bridge
    for (const em of EMAILS) {
      posts.push(fetch(`https://ntfy.sh/${NTFY_TOPIC}`, {
        method: "POST",
        headers: { Title: title, Email: em, Tags: "moneybag" },
        body,
      }));
    }
    // one plain push for anyone subscribed to the topic in the ntfy app
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
