# Edge Enterprise — MT/WI GC Cold Email Sequence

**Sender:** Ramon Trigueros — Edge Enterprise LLC
**Send-from email:** rtrigueros@edgeenterprise.net
**Sequence length:** 3 emails over 10 days
**Audience:** GCs and multi-family developers in MT and WI

## Email 1 — Day 0

**Subject:** framing sub now licensed in {state}

Hi {first_name},

I'm Ramon with Edge Enterprise — a family-run wood and steel framing outfit out of Long Prairie, MN. 25+ years framing multi-family and commercial across MN and ND, and we just registered to do business in {state} this week.

That means we now have legal authority to bid {company}'s projects in {city} and statewide.

Recent multi-family: ENVY Apartments and 45th Street Apartments in Fargo, plus EOLA in Fargo — all completed for repeat GC partners (Comeland Builders, Gast Construction).

If you've got framing scopes coming up in the next 6-12 months, I'd like to be on your bid list. Worth a 15-minute intro call?

{scheduling_link}

Ramon Trigueros
Edge Enterprise LLC
701-318-1231 | edgeenterprise.net

---

## Email 2 — Day 4

**Subject:** re: framing sub now licensed in {state}
**Reply to:** Email 1 (keeps the thread)

{first_name},

Following up — I know cold emails from out-of-state subs usually get deleted, so let me get more specific.

Most {state} framing crews are booked 6+ months on residential. We run dedicated commercial framing crews — multi-family wood framing is what we do every day, not a sideline.

On 45th Street Apartments (Fargo, 4 stories, ~120 units), we framed on schedule and on budget for Meridian Construction. Photos and references available.

If {company} has anything breaking ground in {city} in 2026 or 2027, I'd appreciate a shot at the bid — even just to give you a number to compare against your usual subs.

{scheduling_link}

Ramon
701-318-1231

---

## Email 3 — Day 10

**Subject:** closing the loop
**Reply to:** Email 1

{first_name},

Last note from me, then I'll stop crowding your inbox.

If framing isn't a need right now, no worries — could you point me to whoever handles pre-con or sub prequals at {company}? Happy to send our W-9, COI, and project list so we're in your file for whenever something comes up.

If now's just not the right time, no problem either — I'll check back in Q3.

Thanks for your time,

Ramon Trigueros
Edge Enterprise LLC
701-318-1231 | edgeenterprise.net

---

## Setup checklist (before first send)

- [x] Sending mailbox: `rtrigueros@edgeenterprise.net` (already provisioned via M365)
- [ ] Set up SPF, DKIM, DMARC on edgeenterprise.net DNS at Netlify
- [ ] Run domain through mail-tester.com — aim for 9/10 or better
- [ ] Sign up for Smartlead or Instantly
- [ ] Run inbox through warmup tool for 14 days BEFORE first cold send
- [ ] Build target list: scrape AGC of MT + AGC of WI member directories (~300-500 GCs each)
- [ ] Add personalization fields to CSV: `{first_name}`, `{company}`, `{city}`, `{state}`
- [ ] Set scheduling link (Calendly recommended)
- [ ] Configure "stop on reply" in sequencer
- [ ] Disable open tracking and link tracking pixels (hurts deliverability)

## Sending volume + cadence

- Days 1-10: 20-30 sends/day from a fresh inbox
- Days 11+: ramp to 40-50/day max
- Best send window: Tuesday-Thursday, 7-9 AM local time to recipient
- Avoid: Mondays (inbox flood), Friday afternoons

## Spam-trigger words to keep out of any future edits

free, guarantee, limited time, act now, best price, 100%, no obligation, amazing, winner, cash, ALL CAPS subject lines, excessive punctuation (!!!).

## CAN-SPAM compliance

Add to Email 1 footer:
> Edge Enterprise LLC, 15763 221st Ave, Long Prairie, MN 56347. Reply "remove" to unsubscribe.
