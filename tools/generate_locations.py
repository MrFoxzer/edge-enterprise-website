#!/usr/bin/env python3
"""Edge Enterprise programmatic location-page generator.

Generates:
  locations/{city}-{st}.html                    - city hub pages (skips the 22 hand-written ones)
  locations/{service}/{city}-{st}.html          - service x city pages
  locations/{service}/index.html                - service hubs
  locations/minnesota|north-dakota|wisconsin|montana.html - state hubs
  sitemap.xml                                   - regenerated with every page

Idempotent: re-running overwrites generated pages, never the hand-written city hubs
(they are patched in place to link their service pills to the new service pages).

Run:  python3 tools/generate_locations.py
"""
import hashlib
import math
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOC = os.path.join(ROOT, "locations")
BASE = "https://edgeenterprise.net"
HQ = (45.9747, -94.8653)  # Long Prairie, MN
TODAY = date.today().isoformat()

STATES = {
    "mn": ("Minnesota", "minnesota"),
    "nd": ("North Dakota", "north-dakota"),
    "wi": ("Wisconsin", "wisconsin"),
    "mt": ("Montana", "montana"),
}

# name, st, county, population, lat, lon
CITIES = [
    # ---------------- MINNESOTA (56) ----------------
    ("Minneapolis", "mn", "Hennepin", 429954, 44.9778, -93.2650),
    ("St. Paul", "mn", "Ramsey", 311527, 44.9537, -93.0900),
    ("Rochester", "mn", "Olmsted", 121395, 44.0121, -92.4802),
    ("Duluth", "mn", "St. Louis", 86697, 46.7867, -92.1005),
    ("Bloomington", "mn", "Hennepin", 89987, 44.8408, -93.2983),
    ("St. Cloud", "mn", "Stearns", 68881, 45.5579, -94.1632),
    ("Brooklyn Park", "mn", "Hennepin", 86478, 45.0941, -93.3563),
    ("Plymouth", "mn", "Hennepin", 81026, 45.0105, -93.4555),
    ("Woodbury", "mn", "Washington", 75102, 44.9239, -92.9594),
    ("Maple Grove", "mn", "Hennepin", 70253, 45.0725, -93.4557),
    ("Blaine", "mn", "Anoka", 70222, 45.1608, -93.2349),
    ("Lakeville", "mn", "Dakota", 69490, 44.6497, -93.2428),
    ("Eagan", "mn", "Dakota", 68855, 44.8041, -93.1669),
    ("Burnsville", "mn", "Dakota", 64317, 44.7677, -93.2777),
    ("Eden Prairie", "mn", "Hennepin", 64198, 44.8547, -93.4708),
    ("Coon Rapids", "mn", "Anoka", 63599, 45.1732, -93.3030),
    ("Apple Valley", "mn", "Dakota", 56374, 44.7319, -93.2177),
    ("Edina", "mn", "Hennepin", 53494, 44.8897, -93.3499),
    ("Minnetonka", "mn", "Hennepin", 53781, 44.9212, -93.4687),
    ("Shakopee", "mn", "Scott", 43698, 44.7974, -93.5272),
    ("Maplewood", "mn", "Ramsey", 42088, 44.9530, -92.9952),
    ("Cottage Grove", "mn", "Washington", 38839, 44.8277, -92.9438),
    ("Richfield", "mn", "Hennepin", 36994, 44.8833, -93.2833),
    ("Roseville", "mn", "Ramsey", 36254, 45.0061, -93.1566),
    ("Inver Grove Heights", "mn", "Dakota", 35801, 44.8480, -93.0428),
    ("Andover", "mn", "Anoka", 32601, 45.2333, -93.2914),
    ("Brooklyn Center", "mn", "Hennepin", 33782, 45.0761, -93.3327),
    ("Savage", "mn", "Scott", 32465, 44.7791, -93.3363),
    ("Oakdale", "mn", "Washington", 28303, 44.9630, -92.9649),
    ("Fridley", "mn", "Anoka", 29590, 45.0861, -93.2633),
    ("Shoreview", "mn", "Ramsey", 26921, 45.0791, -93.1472),
    ("Ramsey", "mn", "Anoka", 27646, 45.2611, -93.4500),
    ("Chaska", "mn", "Carver", 27810, 44.7894, -93.6022),
    ("Prior Lake", "mn", "Scott", 27617, 44.7133, -93.4228),
    ("Chanhassen", "mn", "Carver", 25947, 44.8622, -93.5308),
    ("White Bear Lake", "mn", "Ramsey", 24883, 45.0847, -93.0099),
    ("Elk River", "mn", "Sherburne", 25213, 45.3038, -93.5672),
    ("Rosemount", "mn", "Dakota", 25650, 44.7394, -93.1258),
    ("Farmington", "mn", "Dakota", 23632, 44.6402, -93.1436),
    ("Hastings", "mn", "Dakota", 22154, 44.7433, -92.8522),
    ("Otsego", "mn", "Wright", 19966, 45.2660, -93.6197),
    ("Sartell", "mn", "Stearns", 19351, 45.6216, -94.2069),
    ("Big Lake", "mn", "Sherburne", 11833, 45.3325, -93.7461),
    ("Monticello", "mn", "Wright", 14455, 45.3055, -93.7942),
    ("Buffalo", "mn", "Wright", 16972, 45.1719, -93.8747),
    ("St. Michael", "mn", "Wright", 18319, 45.2097, -93.6647),
    ("Albertville", "mn", "Wright", 7940, 45.2377, -93.6544),
    ("Rogers", "mn", "Hennepin", 13295, 45.1888, -93.5530),
    ("Alexandria", "mn", "Douglas", 14335, 45.8852, -95.3775),
    ("Fergus Falls", "mn", "Otter Tail", 14119, 46.2830, -96.0776),
    ("Brainerd", "mn", "Crow Wing", 14395, 46.3580, -94.2008),
    ("Baxter", "mn", "Crow Wing", 8642, 46.3433, -94.2867),
    ("Bemidji", "mn", "Beltrami", 14574, 47.4736, -94.8803),
    ("Willmar", "mn", "Kandiyohi", 21015, 45.1219, -95.0433),
    ("Moorhead", "mn", "Clay", 44505, 46.8739, -96.7678),
    ("Long Prairie", "mn", "Todd", 3442, 45.9747, -94.8653),
    ("Little Falls", "mn", "Morrison", 9140, 45.9764, -94.3625),
    ("Sauk Rapids", "mn", "Benton", 13856, 45.5919, -94.1661),
    ("Waite Park", "mn", "Stearns", 7462, 45.5569, -94.2242),
    ("Mankato", "mn", "Blue Earth", 44488, 44.1636, -93.9994),
    ("Owatonna", "mn", "Steele", 26420, 44.0839, -93.2261),
    ("Faribault", "mn", "Rice", 24406, 44.2950, -93.2688),
    ("Northfield", "mn", "Rice", 20790, 44.4583, -93.1616),
    ("Winona", "mn", "Winona", 25948, 44.0499, -91.6393),
    ("Austin", "mn", "Mower", 26174, 43.6666, -92.9746),
    ("Albert Lea", "mn", "Freeborn", 18492, 43.6480, -93.3683),
    ("Hutchinson", "mn", "McLeod", 14599, 44.8875, -94.3697),
    ("Marshall", "mn", "Lyon", 13680, 44.4469, -95.7883),
    ("New Ulm", "mn", "Brown", 14120, 44.3122, -94.4605),
    ("Grand Rapids", "mn", "Itasca", 11126, 47.2372, -93.5302),
    ("Hibbing", "mn", "St. Louis", 16214, 47.4272, -92.9377),
    ("Cloquet", "mn", "Carlton", 12568, 46.7216, -92.4594),
    ("Detroit Lakes", "mn", "Becker", 9869, 46.8172, -95.8453),
    ("Wadena", "mn", "Wadena", 4300, 46.4425, -95.1361),
    ("Staples", "mn", "Todd", 2981, 46.3555, -94.7922),
    ("Melrose", "mn", "Stearns", 3325, 45.6747, -94.8075),
    ("Sauk Centre", "mn", "Stearns", 4555, 45.7375, -94.9525),
    ("Cold Spring", "mn", "Stearns", 4396, 45.4558, -94.4289),
    ("Albany", "mn", "Stearns", 2780, 45.6300, -94.5700),
    ("Glenwood", "mn", "Pope", 2564, 45.6500, -95.3897),
    ("Morris", "mn", "Stevens", 5206, 45.5861, -95.9139),
    ("Montevideo", "mn", "Chippewa", 5222, 44.9483, -95.7236),
    ("Redwood Falls", "mn", "Redwood", 5102, 44.5394, -95.1169),
    ("Park Rapids", "mn", "Hubbard", 4170, 46.9222, -95.0586),
    ("Crookston", "mn", "Polk", 7482, 47.7742, -96.6084),
    ("Thief River Falls", "mn", "Pennington", 8749, 48.1191, -96.1811),
    ("East Grand Forks", "mn", "Polk", 9176, 47.9299, -97.0245),
    # ---------------- NORTH DAKOTA (26) ----------------
    ("Fargo", "nd", "Cass", 133188, 46.8772, -96.7898),
    ("Bismarck", "nd", "Burleigh", 74445, 46.8083, -100.7837),
    ("Grand Forks", "nd", "Grand Forks", 59166, 47.9253, -97.0329),
    ("Minot", "nd", "Ward", 47370, 48.2325, -101.2963),
    ("West Fargo", "nd", "Cass", 40269, 46.8747, -96.9003),
    ("Williston", "nd", "Williams", 29160, 48.1470, -103.6180),
    ("Dickinson", "nd", "Stark", 25679, 46.8792, -102.7896),
    ("Mandan", "nd", "Morton", 24206, 46.8267, -100.8896),
    ("Jamestown", "nd", "Stutsman", 15849, 46.9105, -98.7084),
    ("Wahpeton", "nd", "Richland", 7999, 46.2652, -96.6059),
    ("Devils Lake", "nd", "Ramsey", 7192, 48.1128, -98.8651),
    ("Valley City", "nd", "Barnes", 6575, 46.9233, -98.0032),
    ("Grafton", "nd", "Walsh", 4170, 48.4122, -97.4104),
    ("Watford City", "nd", "McKenzie", 6207, 47.8022, -103.2832),
    ("Stanley", "nd", "Mountrail", 2321, 48.3178, -102.3907),
    ("Horace", "nd", "Cass", 3085, 46.7586, -96.9040),
    ("Casselton", "nd", "Cass", 2624, 46.9005, -97.2109),
    ("Mapleton", "nd", "Cass", 1287, 46.8919, -97.0523),
    ("Kindred", "nd", "Cass", 793, 46.6519, -97.0206),
    ("Hillsboro", "nd", "Traill", 1620, 47.4039, -97.0629),
    ("Mayville", "nd", "Traill", 1852, 47.4980, -97.3248),
    ("Lisbon", "nd", "Ransom", 2074, 46.4416, -97.6812),
    ("Oakes", "nd", "Dickey", 1710, 46.1386, -98.0895),
    ("Carrington", "nd", "Foster", 2062, 47.4497, -99.1262),
    ("Harvey", "nd", "Wells", 1682, 47.7686, -99.9354),
    ("Rugby", "nd", "Pierce", 2509, 48.3689, -99.9962),
    # ---------------- WISCONSIN (40) ----------------
    ("Milwaukee", "wi", "Milwaukee", 577222, 43.0389, -87.9065),
    ("Madison", "wi", "Dane", 269840, 43.0731, -89.4012),
    ("Green Bay", "wi", "Brown", 107395, 44.5133, -88.0133),
    ("Kenosha", "wi", "Kenosha", 99986, 42.5847, -87.8212),
    ("Racine", "wi", "Racine", 77816, 42.7261, -87.7829),
    ("Appleton", "wi", "Outagamie", 75644, 44.2619, -88.4154),
    ("Waukesha", "wi", "Waukesha", 71158, 43.0117, -88.2315),
    ("Eau Claire", "wi", "Eau Claire", 69421, 44.8113, -91.4985),
    ("Oshkosh", "wi", "Winnebago", 66816, 44.0247, -88.5426),
    ("Janesville", "wi", "Rock", 65615, 42.6828, -89.0187),
    ("West Allis", "wi", "Milwaukee", 60325, 43.0167, -88.0070),
    ("La Crosse", "wi", "La Crosse", 52680, 43.8014, -91.2396),
    ("Sheboygan", "wi", "Sheboygan", 49929, 43.7508, -87.7145),
    ("Wauwatosa", "wi", "Milwaukee", 48387, 43.0495, -88.0076),
    ("Fond du Lac", "wi", "Fond du Lac", 44678, 43.7730, -88.4470),
    ("New Berlin", "wi", "Waukesha", 40451, 42.9764, -88.1084),
    ("Wausau", "wi", "Marathon", 39994, 44.9591, -89.6301),
    ("Brookfield", "wi", "Waukesha", 41464, 43.0606, -88.1065),
    ("Beloit", "wi", "Rock", 36657, 42.5083, -89.0318),
    ("Greenfield", "wi", "Milwaukee", 37803, 42.9614, -88.0126),
    ("Menomonee Falls", "wi", "Waukesha", 38527, 43.1789, -88.1173),
    ("Oak Creek", "wi", "Milwaukee", 36497, 42.8859, -87.8631),
    ("Franklin", "wi", "Milwaukee", 36816, 42.8886, -88.0384),
    ("Manitowoc", "wi", "Manitowoc", 34626, 44.0886, -87.6576),
    ("West Bend", "wi", "Washington", 31752, 43.4253, -88.1834),
    ("Sun Prairie", "wi", "Dane", 35967, 43.1836, -89.2137),
    ("Superior", "wi", "Douglas", 26751, 46.7208, -92.1041),
    ("Stevens Point", "wi", "Portage", 25666, 44.5236, -89.5746),
    ("Neenah", "wi", "Winnebago", 27319, 44.1858, -88.4626),
    ("Fitchburg", "wi", "Dane", 29609, 43.0117, -89.4262),
    ("Mount Pleasant", "wi", "Racine", 27732, 42.7142, -87.8945),
    ("Chippewa Falls", "wi", "Chippewa", 14731, 44.9369, -91.3929),
    ("Menomonie", "wi", "Dunn", 16843, 44.8755, -91.9193),
    ("Hudson", "wi", "St. Croix", 14755, 44.9747, -92.7569),
    ("River Falls", "wi", "Pierce", 16182, 44.8614, -92.6238),
    ("New Richmond", "wi", "St. Croix", 10079, 45.1230, -92.5366),
    ("Rice Lake", "wi", "Barron", 9022, 45.5061, -91.7382),
    ("Marshfield", "wi", "Wood", 18929, 44.6689, -90.1718),
    ("Wisconsin Rapids", "wi", "Wood", 18877, 44.3836, -89.8174),
    ("Rhinelander", "wi", "Oneida", 8285, 45.6366, -89.4121),
    # ---------------- MONTANA (30) ----------------
    ("Billings", "mt", "Yellowstone", 117116, 45.7833, -108.5007),
    ("Missoula", "mt", "Missoula", 75516, 46.8721, -113.9940),
    ("Great Falls", "mt", "Cascade", 60442, 47.5053, -111.3008),
    ("Bozeman", "mt", "Gallatin", 56123, 45.6770, -111.0429),
    ("Butte", "mt", "Silver Bow", 35133, 46.0038, -112.5348),
    ("Helena", "mt", "Lewis and Clark", 34464, 46.5891, -112.0391),
    ("Kalispell", "mt", "Flathead", 28450, 48.1958, -114.3129),
    ("Belgrade", "mt", "Gallatin", 12649, 45.7769, -111.1769),
    ("Livingston", "mt", "Park", 8386, 45.6605, -110.5602),
    ("Whitefish", "mt", "Flathead", 8862, 48.4111, -114.3376),
    ("Columbia Falls", "mt", "Flathead", 5737, 48.3725, -114.1815),
    ("Polson", "mt", "Lake", 5601, 47.6936, -114.1631),
    ("Hamilton", "mt", "Ravalli", 5006, 46.2469, -114.1601),
    ("Anaconda", "mt", "Deer Lodge", 9421, 46.1288, -112.9422),
    ("Miles City", "mt", "Custer", 8354, 46.4083, -105.8406),
    ("Glendive", "mt", "Dawson", 4873, 47.1053, -104.7124),
    ("Sidney", "mt", "Richland", 6346, 47.7167, -104.1563),
    ("Havre", "mt", "Hill", 9362, 48.5500, -109.6841),
    ("Lewistown", "mt", "Fergus", 5952, 47.0625, -109.4282),
    ("Laurel", "mt", "Yellowstone", 7205, 45.6691, -108.7715),
    ("Dillon", "mt", "Beaverhead", 3880, 45.2163, -112.6375),
    ("Stevensville", "mt", "Ravalli", 2002, 46.5100, -114.0932),
    ("Lolo", "mt", "Missoula", 4571, 46.7594, -114.0812),
    ("Big Sky", "mt", "Gallatin", 3591, 45.2847, -111.3683),
    ("Manhattan", "mt", "Gallatin", 2147, 45.8566, -111.3327),
    ("Three Forks", "mt", "Gallatin", 2109, 45.8925, -111.5522),
    ("East Helena", "mt", "Lewis and Clark", 2431, 46.5891, -111.9155),
    ("Deer Lodge", "mt", "Powell", 3111, 46.3966, -112.7300),
    ("Red Lodge", "mt", "Carbon", 2257, 45.1858, -109.2468),
    ("Cut Bank", "mt", "Glacier", 3056, 48.6331, -112.3261),
]

SERVICES = [
    {
        "slug": "commercial-framing",
        "name": "Commercial Framing",
        "short": "commercial framing",
        "desc": "Structural framing for retail, office, hospitality, and light-industrial buildings — wood or steel, built to commercial code and schedule.",
        "cards": [
            ("Schedule-driven crews", "Commercial GCs live and die by the critical path. Our crews are sized and sequenced to hit framing milestones so the trades behind us start on time."),
            ("Wood & steel capable", "One sub for the whole structure — dimensional lumber, engineered wood, and light-gauge metal stud framing under a single contract."),
            ("Clean pay-app paperwork", "Lien waivers, certified payroll when required, and clean draw documentation. We make the accounting side of a commercial job painless."),
        ],
        "faq": [
            ("Do you frame commercial buildings in {city}?", "Yes — Edge Enterprise frames retail, office, hospitality, and light-industrial projects in {city} and across {state}. We work as a framing subcontractor under general contractors as well as directly with owners on design-build work."),
            ("Can you handle both wood and steel framing on one project?", "Yes. Many commercial buildings in {city} mix dimensional lumber, engineered wood, and light-gauge steel. We self-perform both, which means one subcontract, one schedule, and one point of responsibility for the entire structure."),
            ("What size commercial projects do you take on?", "Anything from small tenant build-outs to full ground-up commercial structures. Our sweet spot is wood and metal-stud framing packages in the $100K–$2M range, but we scale crews to the project."),
            ("Are you licensed and insured to work in {state}?", "Yes — Edge Enterprise LLC is licensed, bonded, and fully insured for commercial work in {state}, and we carry workers' comp on every crew member on site."),
        ],
    },
    {
        "slug": "wood-framing",
        "name": "Wood Framing",
        "short": "wood framing",
        "desc": "Dimensional lumber and engineered wood framing — floors, walls, roofs, and everything between — cut and stood by career framers.",
        "cards": [
            ("Engineered wood fluency", "I-joists, LVL, PSL, glulam, and floor trusses — we read the shop drawings, catch conflicts before they're built, and install to the manufacturer's spec."),
            ("Tight tolerances", "Walls plumb, plates straight, openings square. The drywallers and finish carpenters behind us will tell you our frames are the easy ones to follow."),
            ("Weather-smart sequencing", "Upper-Midwest framing means framing through real winters. We sequence, protect, and dry-in so the schedule survives the weather."),
        ],
        "faq": [
            ("Do you do residential and commercial wood framing in {city}?", "Both. Edge Enterprise frames single-family homes, townhomes, multi-family buildings, and commercial wood structures in {city} and the surrounding {county} County area."),
            ("Can you frame through the winter?", "Yes — our crews frame year-round across {state}. Cold-weather framing is standard practice for us: we plan material staging, snow removal, and dry-in sequencing so winter doesn't stall your schedule."),
            ("Do you install engineered wood products?", "Yes. I-joists, LVL and PSL beams, glulam, and floor/roof trusses are on nearly every set of plans we frame. We install to the manufacturer's specifications and coordinate directly with the truss and EWP suppliers."),
            ("How do I get a wood framing bid for a project in {city}?", "Send us your plans through the contact form and we'll return a clear, line-item framing proposal — typically within a few business days depending on project size."),
        ],
    },
    {
        "slug": "steel-framing",
        "name": "Steel & Metal Stud Framing",
        "short": "steel framing",
        "desc": "Light-gauge metal stud framing for commercial interiors, exterior non-bearing walls, and load-bearing cold-formed steel structures.",
        "cards": [
            ("Cold-formed steel expertise", "Load-bearing CFS, curtain-wall infill, shaft walls, and ceiling framing — screwed, welded, or clipped per the engineer's details."),
            ("Commercial interiors", "Demising walls, furring, soffits, and hard-lid ceilings for tenant improvements and new commercial construction."),
            ("Hybrid structures", "Plenty of buildings mix wood and steel. Because we self-perform both, the interface details actually get built the way they were drawn."),
        ],
        "faq": [
            ("Do you do metal stud framing in {city}?", "Yes — Edge Enterprise self-performs light-gauge steel framing for commercial interiors, exterior infill walls, and load-bearing cold-formed steel projects in {city} and across {state}."),
            ("Steel studs or wood — which should my {city} project use?", "It depends on the building type, code requirements, and finish schedule. Steel wins for non-combustible construction and long interior runs; wood usually wins on cost for low-rise structures. Since we frame both, we'll give you an honest comparison rather than steering you to the only thing we sell."),
            ("Do you install shaft wall and demising wall systems?", "Yes — shaft liner, area separation walls, and rated demising assemblies are part of nearly every commercial and multi-family steel package we frame."),
            ("Can you take on just the steel package of a larger job?", "Absolutely. We regularly contract the metal-stud scope alone — interiors, soffits, or exterior infill — working alongside the GC's other framing subs."),
        ],
    },
    {
        "slug": "multi-family-framing",
        "name": "Multi-Family Framing",
        "short": "multi-family framing",
        "desc": "Apartment buildings, townhomes, and senior living — the product type Edge Enterprise has built its reputation on, with 1,000+ units framed.",
        "cards": [
            ("1,000+ units framed", "45th Street Apartments, ENVY, EOLA, Oxbow Heights, and more. Multi-family isn't a sideline for us — it's the core of our portfolio."),
            ("Repetition without sloppiness", "Multi-family rewards crews who can hold quality across hundreds of identical walls. Our unit-by-unit QC keeps floor 4 as tight as floor 1."),
            ("Fire-rated assembly discipline", "Party walls, floor-ceiling assemblies, draft stopping, and shaft walls built exactly to the listed assembly — because that's what the inspector will check."),
        ],
        "faq": [
            ("Have you framed large apartment projects before?", "Yes — multi-family is Edge Enterprise's core specialty. We've framed over 1,000 units across the Upper Midwest, including 45th Street Apartments, ENVY, EOLA, and Oxbow Heights, working with repeat GC partners like Comeland Builders, Gast Construction, and Miller Architects & Builders."),
            ("What multi-family product types do you frame in {city}?", "Garden-style apartments, wrap and podium buildings, townhomes, and senior living communities. If it's wood-frame or hybrid wood-over-podium construction in {city}, it's squarely in our wheelhouse."),
            ("How do you keep large multi-family jobs on schedule?", "Crew sizing, panel/component strategy, and honest look-ahead scheduling. We build a unit-by-unit production plan with the GC and report against it weekly — no surprises at the OAC meeting."),
            ("Do you handle fire-rated assemblies and inspections?", "Yes. Rated party walls, floor-ceiling assemblies, draft stopping, and shaft construction are standard scope on every multi-family frame, built to the listed assembly and walked with the inspector."),
        ],
    },
    {
        "slug": "framing-subcontractor",
        "name": "Framing Subcontractor",
        "short": "framing subcontracting",
        "desc": "A reliable framing sub for general contractors — real scopes, real schedules, clean paperwork, and crews that show up.",
        "cards": [
            ("GC-friendly operations", "Submittals, RFIs, look-aheads, and pay apps handled like a professional sub — because we know your job is managing twenty of us."),
            ("Honest capacity", "We tell you what our crews can actually absorb before we sign, not after we're behind. GCs re-hire us because our schedule promises hold."),
            ("Full framing scope", "Wood, steel, trusses, sheathing, blocking, backing, and rough openings — a complete structural framing package under one subcontract."),
        ],
        "faq": [
            ("Are you taking on new GC relationships in {city}?", "Yes — Edge Enterprise is actively bidding framing packages for general contractors in {city} and across {state}. Send plans through the contact form and we'll turn around a scope letter and number."),
            ("What does your framing subcontract scope typically include?", "Complete structural framing: plates, walls, floor systems, roof framing or truss set, sheathing, blocking and backing, rough openings, and hardware. We'll break out alternates however your bid form needs them."),
            ("Do you carry the insurance our contracts require?", "Yes — commercial general liability, workers' compensation, and auto, with additional-insured endorsements and waivers of subrogation as required. COIs are issued before mobilization."),
            ("Can you work under our safety program?", "Of course. Our crews run OSHA-compliant fall protection and site-specific safety plans, and we'll fold into your EMR/ toolbox-talk requirements without drama."),
        ],
    },
    {
        "slug": "custom-home-framing",
        "name": "Custom Home Framing",
        "short": "custom home framing",
        "desc": "Complex custom homes — vaulted great rooms, long-span beams, complicated roofs — framed by crews who like the hard ones.",
        "cards": [
            ("Complex roof systems", "Hips, valleys, dormers, curved and vaulted ceilings — the roofs production framers turn down are the ones our crews enjoy."),
            ("Beam & timber work", "Glulam, PSL, and steel carrying beams set right, with the temporary shoring and sequencing thought through before the crane shows up."),
            ("Architect-drawing fluency", "Custom homes come with custom details. We read the full set, flag conflicts early, and build what the architect drew — not an approximation of it."),
        ],
        "faq": [
            ("Do you frame custom homes in {city}?", "Yes — Edge Enterprise frames architect-designed custom homes in {city} and throughout {county} County, working with custom builders and directly with owners' GCs."),
            ("My plans have a complicated roof. Is that a problem?", "That's the work we like best. Vaulted ceilings, intersecting hips and valleys, dormers, and exposed structure are exactly where an experienced framing crew earns its keep."),
            ("How far in advance should I book framing for a custom build in {city}?", "For a typical custom home, 6–10 weeks of lead time lets us hold a crew slot for you. Earlier is better on lake homes and mountain builds where the season compresses everything."),
            ("Will you coordinate with my architect and engineer?", "Yes — we'd rather ask the engineer a question before the wall goes up than after. RFIs, shop-drawing review, and site visits with your design team are part of the service."),
        ],
    },
    {
        "slug": "finished-carpentry",
        "name": "Finished Carpentry",
        "short": "finished carpentry",
        "desc": "Trim, doors, millwork, and the detail work people actually touch — installed by carpenters who care about the last 2%.",
        "cards": [
            ("Doors, trim & millwork", "Interior doors hung to swing right, casing and base with tight miters, and stair parts, rails, and built-ins installed to furniture standards."),
            ("Multi-family finish packages", "Hundreds of identical units with doors, trim, shelving, and hardware — delivered at production speed without production sloppiness."),
            ("The punch-list killers", "Finish carpentry is where punch lists are born or die. Our installers work off the same list your super does, so the walk-through is short."),
        ],
        "faq": [
            ("Do you offer finished carpentry as a standalone service in {city}?", "Yes — while we frame many of the buildings we trim, we also contract finish carpentry packages on their own: doors, casing, base, rails, shelving, and specialty millwork across {city} and {state}."),
            ("Do you handle large multi-family trim packages?", "Yes. Multi-family finish work — hundreds of doors, miles of base, unit shelving and hardware — is one of our core scopes, and our production tracking keeps late-building units as clean as the first ones."),
            ("Can you match existing trim in an older home?", "Usually, yes. Between knife-ground profiles from local millwork shops and careful stain matching, we can tie new work into existing trim so the transition disappears."),
            ("What finish materials do you install?", "Paint-grade and stain-grade wood trim, MDF, PVC, prehung and slab doors, hardware, closet systems, stair parts, and custom built-ins."),
        ],
    },
]

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace(".", "")).strip("-")


def haversine(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(h))


def drive_time(city):
    miles = haversine(HQ, (city["lat"], city["lon"])) * 1.22  # road factor
    hours = miles / 58.0
    if hours < 0.35:
        return "under 30 minutes"
    q = round(hours * 4) / 4
    h = int(q)
    m = int(round((q - h) * 60))
    if h == 0:
        return f"{m} minutes"
    if m == 0:
        return f"{h} hour{'s' if h > 1 else ''}"
    return f"{h} hr {m} min"


def pick(pool, *keys):
    h = int(hashlib.md5("|".join(keys).encode()).hexdigest(), 16)
    return pool[h % len(pool)]


def specs_for(city):
    """Regionally accurate typical structural design values, phrased as typical."""
    st, lat, lon = city["st"], city["lat"], city["lon"]
    if st == "mn":
        snow = "50–60 psf" if lat > 46.3 else ("42–50 psf" if lat > 45.2 else "35–42 psf")
        wind = "105–115 mph"
    elif st == "nd":
        snow = "35–50 psf" if lat > 47.5 else "30–40 psf"
        wind = "115–120 mph (open-prairie exposure)"
    elif st == "wi":
        snow = "40–50 psf" if lat > 45.0 else ("35–40 psf" if lat > 43.7 else "30–35 psf")
        wind = "105–115 mph"
    else:  # mt
        mountain = lon < -110.5
        snow = "50–100+ psf (site-specific in mountain zones)" if mountain else "30–50 psf"
        wind = "105–115 mph" + ("; seismic detailing applies in western MT" if mountain else "")
    frost = {"mn": "60 in.", "nd": "60–80 in.", "wi": "48–60 in.", "mt": "48–72 in."}[st]
    return snow, wind, frost


def region_line(city):
    st = city["st"]
    name, county, pop = city["name"], city["county"], city["pop"]
    state = STATES[st][0]
    if pop >= 100000:
        tier = pick([
            f"{name} is one of {state}'s major construction markets, and its permit volume shows it — multi-family, commercial, and custom residential all stay busy here year-round.",
            f"As one of the largest cities in {state}, {name} carries a deep, competitive construction market where schedule reliability and clean inspections separate the framers who last from the ones who don't.",
        ], name, "region")
    elif pop >= 25000:
        tier = pick([
            f"{name} is a strong regional market in {county} County — big enough for steady multi-family and commercial work, small enough that reputation still travels fast between builders and inspectors.",
            f"With roughly {pop:,} residents, {name} anchors a healthy {county} County construction market where the same GCs, lumberyards, and inspectors see every frame that goes up — and remember who built it well.",
        ], name, "region")
    elif pop >= 5000:
        tier = pick([
            f"{name} is the kind of {county} County community where word-of-mouth is the only marketing that matters — every frame we stand here is a referral we either earn or lose.",
            f"In a town like {name}, builders and homeowners talk. We treat every {county} County project as the audition for the next three.",
        ], name, "region")
    else:
        tier = pick([
            f"Small towns like {name} are where we're from — Edge Enterprise is headquartered in Long Prairie (pop. 3,400), so we understand {county} County building the way locals do.",
            f"{name} may be small, but small-town projects get our full crew and full attention — that's the Long Prairie way, and it's how Edge Enterprise was built.",
        ], name, "region")
    return tier


def travel_line(city):
    dt = drive_time(city)
    st = city["st"]
    if st == "nd" and city["county"] in ("Cass", "Traill", "Richland"):
        return f"With our satellite presence in Horace, ND, the {city['name']} area is effectively a home market — crews are local, not visiting."
    return pick([
        f"From our Long Prairie, MN headquarters, {city['name']} is about {dt} away — close enough for our crews to mobilize quickly and staff the job for its full duration.",
        f"{city['name']} sits roughly {dt} from our Long Prairie HQ. For multi-week framing packages we stage crews locally, so drive time never becomes your schedule's problem.",
        f"Our Long Prairie, MN base puts {city['name']} about {dt} out. We plan mobilization, material staging, and crew rotations around that from day one.",
    ], city["name"], "travel")


def code_line(st):
    return {
        "mn": "Projects here fall under the Minnesota State Building Code, with local city or county building officials as the AHJ.",
        "nd": "North Dakota builds run under the state-adopted IBC/IRC, with city building departments — and open-prairie wind exposure — driving the structural detailing.",
        "wi": "Wisconsin work falls under the Wisconsin Commercial Building Code and the Uniform Dwelling Code (UDC) for residential — a code framework with its own quirks that we know well.",
        "mt": "Montana projects run under the state-adopted IBC/IRC; in mountain-zone jurisdictions, site-specific snow loads and seismic detailing are a fact of life we build for.",
    }[st]


# --------------------------------------------------------------------------
# HTML blocks
# --------------------------------------------------------------------------

def head_block(title, desc, canon_path, depth, schema_json):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{BASE}/{canon_path}">
    <link rel="icon" href="{up}favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="{up}favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="{up}favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="{up}apple-touch-icon.png">
    <meta name="theme-color" content="#0a0a0a">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{BASE}/{canon_path}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:site_name" content="Edge Enterprise LLC">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{up}styles.css">
    <script type="application/ld+json">
{schema_json}
    </script>
</head>
<body>"""


def nav_block(depth):
    up = "../" * depth
    return f"""
    <nav class="nav nav-city" id="mainNav">
        <div class="nav-inner">
            <a href="{up}index.html" class="nav-logo">
                <span class="nav-logo-text">EDGE <span class="nav-logo-accent">ENTERPRISE</span></span>
                <img src="{up}logo-icon.png" alt="" class="nav-icon">
            </a>
            <div class="nav-links" id="navLinks">
                <a href="{up}index.html#about" class="nav-link">About</a>
                <a href="{up}index.html#services" class="nav-link">Services</a>
                <a href="{up}index.html#projects" class="nav-link">Projects</a>
                <a href="{up}index.html#service-areas" class="nav-link">Service Areas</a>
                <a href="{up}index.html#process" class="nav-link">Process</a>
                <a href="{up}index.html#testimonials" class="nav-link">Testimonials</a>
                <a href="{up}index.html#contact" class="nav-link nav-link-cta">Get a Quote</a>
            </div>
            <button class="nav-toggle" id="navToggle" aria-label="Toggle menu">
                <span></span><span></span><span></span>
            </button>
        </div>
    </nav>"""


def footer_block(depth):
    up = "../" * depth
    return f"""
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <img src="{up}logo.png" alt="Edge Enterprise LLC" class="footer-logo">
                    <p>Professional construction services built on integrity, precision, and excellence. Serving clients nationwide from our Minnesota &amp; North Dakota headquarters.</p>
                </div>
                <div class="footer-links">
                    <h4>Quick Links</h4>
                    <a href="{up}index.html#about">About Us</a>
                    <a href="{up}index.html#services">Services</a>
                    <a href="{up}index.html#projects">Portfolio</a>
                    <a href="{up}index.html#service-areas">Service Areas</a>
                    <a href="{up}index.html#contact">Contact</a>
                </div>
                <div class="footer-links">
                    <h4>Service Areas</h4>
                    <a href="{up}locations/minnesota.html">Minnesota</a>
                    <a href="{up}locations/north-dakota.html">North Dakota</a>
                    <a href="{up}locations/wisconsin.html">Wisconsin</a>
                    <a href="{up}locations/montana.html">Montana</a>
                </div>
                <div class="footer-links">
                    <h4>Contact</h4>
                    <a href="{up}index.html#contact">Send a message</a>
                    <span>Long Prairie, MN</span>
                    <span>Horace, ND</span>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Edge Enterprise LLC. All rights reserved.</p>
                <p>Licensed &amp; Insured · Serving MN, ND, MT, WI</p>
            </div>
        </div>
    </footer>
    <script src="{up}script.js"></script>
</body>
</html>"""


def cta_block(depth, city_name, svc_short=None):
    up = "../" * depth
    what = svc_short or "framing"
    return f"""
    <section class="section section-cta">
        <div class="container">
            <div class="cta-block">
                <h2 class="cta-title">Planning a {what.title()} Project in <span class="text-accent">{city_name}?</span></h2>
                <p class="cta-text">Tell us about your build. We'll get back to you with a clear, honest scope and estimate — typically within one business day.</p>
                <a href="{up}index.html#contact" class="btn btn-primary btn-large">
                    <span>Request a Free Estimate</span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </a>
            </div>
        </div>
    </section>"""


def nearby_block(city, cities_by_state, depth, svc=None):
    """Nearest same-state cities. If svc, link to that service's pages."""
    same = [c for c in cities_by_state[city["st"]] if c["slug"] != city["slug"]]
    same.sort(key=lambda c: haversine((city["lat"], city["lon"]), (c["lat"], c["lon"])))
    near = same[:6]
    st_up = city["st"].upper()
    state = STATES[city["st"]][0]
    if svc:
        cards = "\n".join(
            f"""                <a href="{c['slug']}-{c['st']}.html" class="city-nearby-card">
                    <span class="city-nearby-state">{st_up}</span>
                    <h3>{c['name']}</h3>
                    <span class="city-nearby-arrow">→</span>
                </a>""" for c in near)
        title = f"{svc['name']} Near <span class=\"text-accent\">{city['name']}</span>"
    else:
        cards = "\n".join(
            f"""                <a href="{c['slug']}-{c['st']}.html" class="city-nearby-card">
                    <span class="city-nearby-state">{st_up}</span>
                    <h3>{c['name']}</h3>
                    <span class="city-nearby-arrow">→</span>
                </a>""" for c in near)
        title = f"Other Cities in <span class=\"text-accent\">{state}</span>"
    return f"""
    <section class="section section-city-nearby">
        <div class="container">
            <div class="section-header">
                <span class="section-label">NEARBY SERVICE AREAS</span>
                <h2 class="section-title">{title}</h2>
            </div>
            <div class="city-nearby-grid">
{cards}
            </div>
        </div>
    </section>"""


def breadcrumb_schema(items):
    lis = ",\n".join(
        f"""        {{
          "@type": "ListItem",
          "position": {i + 1},
          "name": "{name}",
          "item": "{url}"
        }}""" for i, (name, url) in enumerate(items))
    return f"""    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
{lis}
      ]
    }}"""


def esc(s):
    return s.replace('"', '\\"')


# --------------------------------------------------------------------------
# page builders
# --------------------------------------------------------------------------

def build_service_city_page(svc, city, cities_by_state):
    state, state_slug = STATES[city["st"]]
    st_up = city["st"].upper()
    name = city["name"]
    fname = f"{city['slug']}-{city['st']}.html"
    canon = f"locations/{svc['slug']}/{fname}"
    title = f"{svc['name']} in {name}, {st_up} | Edge Enterprise LLC"
    desc = (f"Edge Enterprise LLC provides {svc['short']} in {name}, {st_up} ({city['county']} County). "
            f"Family-owned, 25+ years of experience, 1,000+ units framed. Licensed & insured in {state}. Free estimates.")
    snow, wind, frost = specs_for(city)
    dt = drive_time(city)

    intro1 = pick([
        f"Edge Enterprise LLC brings {svc['short']} to {name} backed by 25+ years of framing experience and more than 1,000 multi-family units built across the Upper Midwest. {region_line(city)}",
        f"Looking for {svc['short']} in {name}? Edge Enterprise LLC is a family-owned contractor with 25+ years in the trade and over 1,000 framed units in its portfolio. {region_line(city)}",
        f"{region_line(city)} Edge Enterprise LLC serves {name} with {svc['short']} built on 25+ years of experience and a portfolio that includes some of the region's largest multi-family frames.",
    ], city["slug"], svc["slug"], "i1")
    intro2 = f"{travel_line(city)} {code_line(city['st'])} Typical design values for the {name} area — ground snow load around {snow}, design wind speeds of {wind}, and frost depths near {frost} — are baked into how we detail and build here; final values are always confirmed with the local building official."

    faq_html, faq_schema_items = [], []
    for q, a in svc["faq"]:
        qf = q.format(city=name, state=state, county=city["county"])
        af = a.format(city=name, state=state, county=city["county"])
        faq_html.append(f"""                <div class="city-why-card">
                    <h3>{qf}</h3>
                    <p>{af}</p>
                </div>""")
        faq_schema_items.append(f"""        {{
          "@type": "Question",
          "name": "{esc(qf)}",
          "acceptedAnswer": {{ "@type": "Answer", "text": "{esc(af)}" }}
        }}""")

    cards_html = "\n".join(f"""                <div class="city-why-card">
                    <div class="city-why-num">0{i + 1}</div>
                    <h3>{t}</h3>
                    <p>{b}</p>
                </div>""" for i, (t, b) in enumerate(svc["cards"]))

    other_svcs = "\n".join(
        f"""                <a class="city-service-pill" href="../{s['slug']}/{fname}">{s['name']}</a>"""
        for s in SERVICES if s["slug"] != svc["slug"])

    schema = f"""    [{{
      "@context": "https://schema.org",
      "@type": "GeneralContractor",
      "name": "Edge Enterprise LLC",
      "description": "{esc(desc)}",
      "url": "{BASE}/{canon}",
      "image": "{BASE}/logo.png",
      "areaServed": {{
        "@type": "City",
        "name": "{name}",
        "containedInPlace": {{ "@type": "AdministrativeArea", "name": "{state}" }}
      }},
      "address": {{ "@type": "PostalAddress", "addressLocality": "Long Prairie", "addressRegion": "MN", "addressCountry": "US" }},
      "makesOffer": {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "{svc['name']}", "areaServed": "{name}, {st_up}" }} }}
    }},
{breadcrumb_schema([("Home", BASE + "/"), (state, f"{BASE}/locations/{state_slug}.html"), (f"{name}, {st_up}", f"{BASE}/locations/{fname}"), (svc['name'], f"{BASE}/{canon}")])},
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
{",".join(faq_schema_items)}
      ]
    }}]"""

    html = head_block(title, desc, canon, 2, schema) + nav_block(2) + f"""
    <section class="city-hero">
        <div class="city-hero-bg"></div>
        <div class="container">
            <div class="city-hero-inner">
                <span class="section-label">{state} · {st_up}</span>
                <h1 class="city-hero-title">{svc['name']} in <span class="text-accent">{name}</span></h1>
                <p class="city-hero-sub">{svc['desc']}</p>
                <div class="city-hero-meta">
                    <span><strong>County:</strong> {city['county']}</span>
                    <span class="city-hero-divider"></span>
                    <span><strong>Population:</strong> {city['pop']:,}</span>
                    <span class="city-hero-divider"></span>
                    <span><strong>From Edge HQ:</strong> {dt}</span>
                </div>
                <div class="city-hero-ctas">
                    <a href="../../index.html#contact" class="btn btn-primary">
                        <span>Get a Free Estimate</span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </a>
                    <a href="../{fname}" class="btn btn-ghost"><span>All Services in {name}</span></a>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-city-context">
        <div class="container">
            <div class="city-context-grid">
                <div class="city-context-main">
                    <span class="section-label">LOCAL MARKET</span>
                    <h2 class="section-title">{svc['name']} in <span class="text-accent">{name}, {st_up}</span></h2>
                    <div class="city-context-body">
                        <p>{intro1}</p><p>{intro2}</p>
                    </div>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>{name} Framing Specs</h3>
                        <ul>
                            <li><strong>Typical ground snow load</strong><span>{snow}</span></li>
                            <li><strong>Typical design wind</strong><span>{wind}</span></li>
                            <li><strong>Typical frost depth</strong><span>{frost}</span></li>
                            <li><strong>County</strong><span>{city['county']}</span></li>
                            <li><strong>Drive from Edge HQ</strong><span>{dt}</span></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>

    <section class="section section-city-why">
        <div class="container">
            <div class="section-header">
                <span class="section-label">WHY EDGE ENTERPRISE</span>
                <h2 class="section-title">{svc['name']} Done <span class="text-accent">Right</span></h2>
            </div>
            <div class="city-why-grid">
{cards_html}
            </div>
        </div>
    </section>

    <section class="section section-city-services">
        <div class="container">
            <div class="section-header">
                <span class="section-label">MORE SERVICES IN {name.upper()}</span>
                <h2 class="section-title">Other Services We Offer in <span class="text-accent">{name}</span></h2>
            </div>
            <div class="city-services-grid">
{other_svcs}
            </div>
        </div>
    </section>

    <section class="section section-city-why">
        <div class="container">
            <div class="section-header">
                <span class="section-label">FAQ</span>
                <h2 class="section-title">{svc['name']} in {name} — <span class="text-accent">Questions We Hear</span></h2>
            </div>
            <div class="city-why-grid">
{chr(10).join(faq_html)}
            </div>
        </div>
    </section>
""" + nearby_block(city, CITIES_BY_STATE, 2, svc) + cta_block(2, name, svc["short"]) + footer_block(2)
    return canon, html


def build_city_hub_page(city, cities_by_state):
    state, state_slug = STATES[city["st"]]
    st_up = city["st"].upper()
    name = city["name"]
    fname = f"{city['slug']}-{city['st']}.html"
    canon = f"locations/{fname}"
    title = f"Framing Contractor in {name}, {st_up} | Edge Enterprise LLC"
    desc = (f"Edge Enterprise LLC provides commercial framing, wood and steel framing, multi-family construction, and "
            f"finished carpentry in {name}, {st_up}. Family-owned, 25+ years experience, headquartered in Long Prairie, MN.")
    snow, wind, frost = specs_for(city)
    dt = drive_time(city)

    p1 = f"{region_line(city)} Edge Enterprise LLC serves {name} and the wider {city['county']} County area with full-scope structural framing — commercial, multi-family, custom residential, and finished carpentry — backed by 25+ years in the trade and more than 1,000 framed units across the Upper Midwest."
    p2 = f"{travel_line(city)} {code_line(city['st'])} Typical design values around {name} — ground snow loads near {snow}, design wind speeds of {wind}, and frost depths around {frost} — shape how we detail every frame; exact values are confirmed with the local building official before we cut the first plate."

    svc_pills = "\n".join(
        f"""                <a class="city-service-pill" href="{s['slug']}/{fname}">{s['name']}</a>"""
        for s in SERVICES)

    why = [
        ("Family-owned, crew-operated", f"Edge Enterprise isn't a broker that resells your frame to whoever's cheapest this month. Our own crews frame every {name} project, run by people whose last name is on the company."),
        ("Built for this climate", f"{state} framing means real snow loads, real wind, and real winters. We detail and sequence for the actual conditions in {city['county']} County — not a generic southern spec."),
        ("1,000+ units of proof", "45th Street Apartments, ENVY, EOLA, Oxbow Heights, the Lake Superior Glamping retreat and more — built with trusted GC partners like Comeland Builders, Gast Construction, and Miller Architects & Builders. Our track record is the best evidence of how we'll treat your project."),
    ]
    why_html = "\n".join(f"""                <div class="city-why-card">
                    <div class="city-why-num">0{i + 1}</div>
                    <h3>{t}</h3>
                    <p>{b}</p>
                </div>""" for i, (t, b) in enumerate(why))

    schema = f"""    [{{
      "@context": "https://schema.org",
      "@type": "GeneralContractor",
      "name": "Edge Enterprise LLC – {name}, {st_up}",
      "description": "{esc(desc)}",
      "url": "{BASE}/{canon}",
      "image": "{BASE}/logo.png",
      "areaServed": {{
        "@type": "City",
        "name": "{name}",
        "containedInPlace": {{ "@type": "AdministrativeArea", "name": "{state}" }}
      }},
      "address": {{ "@type": "PostalAddress", "addressLocality": "Long Prairie", "addressRegion": "MN", "addressCountry": "US" }}
    }},
{breadcrumb_schema([("Home", BASE + "/"), (state, f"{BASE}/locations/{state_slug}.html"), (f"{name}, {st_up}", f"{BASE}/{canon}")])}]"""

    html = head_block(title, desc, canon, 1, schema) + nav_block(1) + f"""
    <section class="city-hero">
        <div class="city-hero-bg"></div>
        <div class="container">
            <div class="city-hero-inner">
                <span class="section-label">{state} · {st_up}</span>
                <h1 class="city-hero-title">Framing Contractor in <span class="text-accent">{name}</span></h1>
                <p class="city-hero-sub">Commercial, multi-family, and custom residential framing — plus finished carpentry — for {name} and {city['county']} County.</p>
                <div class="city-hero-meta">
                    <span><strong>County:</strong> {city['county']}</span>
                    <span class="city-hero-divider"></span>
                    <span><strong>Population:</strong> {city['pop']:,}</span>
                    <span class="city-hero-divider"></span>
                    <span><strong>From Edge HQ:</strong> {dt}</span>
                </div>
                <div class="city-hero-ctas">
                    <a href="../index.html#contact" class="btn btn-primary">
                        <span>Get a Free Estimate</span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </a>
                    <a href="../index.html#projects" class="btn btn-ghost"><span>See Our Work</span></a>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-city-context">
        <div class="container">
            <div class="city-context-grid">
                <div class="city-context-main">
                    <span class="section-label">LOCAL MARKET</span>
                    <h2 class="section-title">{name} <span class="text-accent">Construction Market</span></h2>
                    <div class="city-context-body">
                        <p>{p1}</p><p>{p2}</p>
                    </div>
                </div>
                <aside class="city-context-side">
                    <div class="city-spec-card">
                        <h3>{name} Framing Specs</h3>
                        <ul>
                            <li><strong>Typical ground snow load</strong><span>{snow}</span></li>
                            <li><strong>Typical design wind</strong><span>{wind}</span></li>
                            <li><strong>Typical frost depth</strong><span>{frost}</span></li>
                            <li><strong>County</strong><span>{city['county']}</span></li>
                            <li><strong>Drive from Edge HQ</strong><span>{dt}</span></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>

    <section class="section section-city-services">
        <div class="container">
            <div class="section-header">
                <span class="section-label">SERVICES IN {name.upper()}</span>
                <h2 class="section-title">Framing Services <span class="text-accent">We Offer</span></h2>
                <p class="section-subtitle">Every service below has a dedicated {name} page with local specs, FAQs, and details.</p>
            </div>
            <div class="city-services-grid">
{svc_pills}
            </div>
        </div>
    </section>

    <section class="section section-city-why">
        <div class="container">
            <div class="section-header">
                <span class="section-label">WHY EDGE ENTERPRISE</span>
                <h2 class="section-title">Why Choose Us For Your <span class="text-accent">{name} Project</span></h2>
            </div>
            <div class="city-why-grid">
{why_html}
            </div>
        </div>
    </section>
""" + nearby_block(city, CITIES_BY_STATE, 1) + cta_block(1, name) + footer_block(1)
    return canon, html


def build_state_hub(st, cities_by_state):
    state, state_slug = STATES[st]
    st_up = st.upper()
    canon = f"locations/{state_slug}.html"
    cities = sorted(cities_by_state[st], key=lambda c: -c["pop"])
    title = f"Framing Contractor in {state} | {len(cities)} Cities Served | Edge Enterprise LLC"
    desc = (f"Edge Enterprise LLC provides commercial, multi-family, and residential framing across {state} — "
            f"serving {len(cities)} cities including {', '.join(c['name'] for c in cities[:4])}. Licensed & insured.")
    city_cards = "\n".join(
        f"""                <a href="{c['slug']}-{c['st']}.html" class="city-nearby-card">
                    <span class="city-nearby-state">{st_up}</span>
                    <h3>{c['name']}</h3>
                    <span class="city-nearby-arrow">→</span>
                </a>""" for c in cities)
    svc_pills = "\n".join(
        f"""                <a class="city-service-pill" href="{s['slug']}/index.html">{s['name']}</a>"""
        for s in SERVICES)
    blurb = {
        "mn": "Minnesota is home — Edge Enterprise is headquartered in Long Prairie, in the middle of the state, which puts nearly every Minnesota market within a comfortable mobilization radius. From Twin Cities multi-family to lake-country custom homes, this is where our crews have framed the longest.",
        "nd": "North Dakota is Edge Enterprise's second home — our satellite presence in Horace and a deep Fargo-metro track record (45th Street, EOLA, Oxbow Heights and more) make the Red River Valley one of our strongest markets, with statewide coverage from Fargo to Williston.",
        "wi": "Wisconsin's construction market runs deep — from Twin Cities-adjacent St. Croix County to Madison, Milwaukee, and the Fox Valley. Edge Enterprise serves the state with the same full-scope framing packages we run in Minnesota, under Wisconsin's UDC and commercial code framework.",
        "mt": "Montana is Edge Enterprise's newest service territory — and its fastest-growing. From Bozeman and the Gallatin Valley boom to Flathead-country custom builds, we bring Upper-Midwest production discipline to mountain-West framing, including site-specific snow-load and seismic detailing.",
    }[st]
    schema = breadcrumb_schema([("Home", BASE + "/"), (state, f"{BASE}/{canon}")])
    html = head_block(title, desc, canon, 1, "[" + schema + "]") + nav_block(1) + f"""
    <section class="city-hero">
        <div class="city-hero-bg"></div>
        <div class="container">
            <div class="city-hero-inner">
                <span class="section-label">SERVICE AREA · {st_up}</span>
                <h1 class="city-hero-title">Framing Across <span class="text-accent">{state}</span></h1>
                <p class="city-hero-sub">{blurb}</p>
                <div class="city-hero-ctas">
                    <a href="../index.html#contact" class="btn btn-primary">
                        <span>Get a Free Estimate</span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-city-services">
        <div class="container">
            <div class="section-header">
                <span class="section-label">SERVICES</span>
                <h2 class="section-title">What We Build in <span class="text-accent">{state}</span></h2>
            </div>
            <div class="city-services-grid">
{svc_pills}
            </div>
        </div>
    </section>

    <section class="section section-city-nearby">
        <div class="container">
            <div class="section-header">
                <span class="section-label">CITIES WE SERVE</span>
                <h2 class="section-title">{len(cities)} {state} <span class="text-accent">Cities</span></h2>
            </div>
            <div class="city-nearby-grid">
{city_cards}
            </div>
        </div>
    </section>
""" + cta_block(1, state) + footer_block(1)
    return canon, html


def build_service_hub(svc, cities_by_state):
    canon = f"locations/{svc['slug']}/index.html"
    title = f"{svc['name']} — MN, ND, WI & MT | Edge Enterprise LLC"
    desc = f"{svc['desc']} Serving {len(CITIES)} cities across Minnesota, North Dakota, Wisconsin, and Montana."
    sections = []
    for st in ("mn", "nd", "wi", "mt"):
        state = STATES[st][0]
        cities = sorted(cities_by_state[st], key=lambda c: -c["pop"])
        cards = "\n".join(
            f"""                <a href="{c['slug']}-{c['st']}.html" class="city-nearby-card">
                    <span class="city-nearby-state">{st.upper()}</span>
                    <h3>{c['name']}</h3>
                    <span class="city-nearby-arrow">→</span>
                </a>""" for c in cities)
        sections.append(f"""
    <section class="section section-city-nearby">
        <div class="container">
            <div class="section-header">
                <span class="section-label">{state.upper()}</span>
                <h2 class="section-title">{svc['name']} in <span class="text-accent">{state}</span></h2>
            </div>
            <div class="city-nearby-grid">
{cards}
            </div>
        </div>
    </section>""")
    cards_html = "\n".join(f"""                <div class="city-why-card">
                    <div class="city-why-num">0{i + 1}</div>
                    <h3>{t}</h3>
                    <p>{b}</p>
                </div>""" for i, (t, b) in enumerate(svc["cards"]))
    schema = breadcrumb_schema([("Home", BASE + "/"), (svc["name"], f"{BASE}/{canon}")])
    html = head_block(title, desc, canon, 2, "[" + schema + "]") + nav_block(2) + f"""
    <section class="city-hero">
        <div class="city-hero-bg"></div>
        <div class="container">
            <div class="city-hero-inner">
                <span class="section-label">SERVICE</span>
                <h1 class="city-hero-title"><span class="text-accent">{svc['name']}</span> Across the Upper Midwest &amp; Mountain West</h1>
                <p class="city-hero-sub">{svc['desc']} Choose your city below for local specs, FAQs, and details.</p>
                <div class="city-hero-ctas">
                    <a href="../../index.html#contact" class="btn btn-primary">
                        <span>Get a Free Estimate</span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-city-why">
        <div class="container">
            <div class="section-header">
                <span class="section-label">WHY EDGE ENTERPRISE</span>
                <h2 class="section-title">{svc['name']} Done <span class="text-accent">Right</span></h2>
            </div>
            <div class="city-why-grid">
{cards_html}
            </div>
        </div>
    </section>
""" + "".join(sections) + cta_block(2, "Your City", svc["short"]) + footer_block(2)
    return canon, html


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

CITY_DICTS = [
    {"name": n, "st": st, "county": co, "pop": p, "lat": la, "lon": lo, "slug": slugify(n)}
    for (n, st, co, p, la, lo) in CITIES
]
CITIES_BY_STATE = {st: [c for c in CITY_DICTS if c["st"] == st] for st in STATES}


HANDWRITTEN_HUBS = {
    "appleton-wi.html", "billings-mt.html", "bismarck-nd.html", "bloomington-mn.html",
    "bozeman-mt.html", "duluth-mn.html", "eau-claire-wi.html", "fargo-nd.html",
    "grand-forks-nd.html", "great-falls-mt.html", "green-bay-wi.html", "helena-mt.html",
    "kalispell-mt.html", "madison-wi.html", "milwaukee-wi.html", "minneapolis-mn.html",
    "minot-nd.html", "missoula-mt.html", "rochester-mn.html", "st-cloud-mn.html",
    "st-paul-mn.html", "west-fargo-nd.html",
}


def main():
    pages = []  # (canon_path, priority)
    existing_hubs = HANDWRITTEN_HUBS

    # service x city pages
    for svc in SERVICES:
        d = os.path.join(LOC, svc["slug"])
        os.makedirs(d, exist_ok=True)
        for city in CITY_DICTS:
            canon, html = build_service_city_page(svc, city, CITIES_BY_STATE)
            with open(os.path.join(ROOT, canon), "w") as f:
                f.write(html)
            pages.append((canon, "0.7"))
        canon, html = build_service_hub(svc, CITIES_BY_STATE)
        with open(os.path.join(ROOT, canon), "w") as f:
            f.write(html)
        pages.append((canon, "0.8"))

    # city hubs (never overwrite hand-written ones)
    generated_hubs = 0
    for city in CITY_DICTS:
        fname = f"{city['slug']}-{city['st']}.html"
        if fname in existing_hubs:
            pages.append((f"locations/{fname}", "0.8"))
            continue
        canon, html = build_city_hub_page(city, CITIES_BY_STATE)
        with open(os.path.join(ROOT, canon), "w") as f:
            f.write(html)
        pages.append((canon, "0.8"))
        generated_hubs += 1

    # state hubs
    for st in STATES:
        canon, html = build_state_hub(st, CITIES_BY_STATE)
        with open(os.path.join(ROOT, canon), "w") as f:
            f.write(html)
        pages.append((canon, "0.9"))

    # patch hand-written city hubs: turn static service pills into links
    patched = 0
    for city in CITY_DICTS:
        fname = f"{city['slug']}-{city['st']}.html"
        path = os.path.join(LOC, fname)
        if fname not in existing_hubs or not os.path.exists(path):
            continue
        with open(path) as f:
            html = f.read()
        if 'class="city-service-pill" href=' in html:
            continue  # already patched
        pill_map = {
            "Commercial Framing": "commercial-framing", "Wood Framing": "wood-framing",
            "Steel Framing": "steel-framing", "Multi-Family Framing": "multi-family-framing",
            "Subcontracting": "framing-subcontractor", "Custom Builds": "custom-home-framing",
            "Finished Carpentry": "finished-carpentry",
        }
        orig = html
        for label, slug in pill_map.items():
            html = html.replace(
                f'<div class="city-service-pill">{label}</div>',
                f'<a class="city-service-pill" href="{slug}/{fname}">{label}</a>')
        if html != orig:
            with open(path, "w") as f:
                f.write(html)
            patched += 1

    # sitemap
    core = [("", "1.0"), ("index.html", "1.0")]
    urls = []
    seen = set()
    for path, pr in core + sorted(pages):
        if path in seen:
            continue
        seen.add(path)
        loc = f"{BASE}/{path}" if path else f"{BASE}/"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{pr}</priority>
  </url>""")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "\n".join(urls) + "\n</urlset>\n")

    total = len(SERVICES) * len(CITY_DICTS)
    print(f"cities: {len(CITY_DICTS)}  services: {len(SERVICES)}")
    print(f"service-city pages: {total}")
    print(f"city hubs generated: {generated_hubs} (kept {len(CITY_DICTS) - generated_hubs} hand-written, patched {patched})")
    print(f"service hubs: {len(SERVICES)}  state hubs: {len(STATES)}")
    print(f"sitemap URLs: {len(urls)}")


if __name__ == "__main__":
    main()
