from django.core.management.base import BaseCommand

from design_studio.models import DesignProject

PROJECTS = [
    # ─────────────────────────────────────────────────────────
    # BEGINNER (1–3)
    # ─────────────────────────────────────────────────────────
    {
        'title': 'Brewmosa Café — Specialty Coffee Shop Landing Page',
        'tags': 'café, local-business, beginner',
        'description': """\
DIFFICULTY: Beginner
SITE TYPE: Single Page

CLIENT BACKGROUND
Brewmosa is a specialty coffee shop in Indiranagar, Bangalore. They are launching a second outlet and need a warm, inviting landing page to drive table reservations and walk-ins. Known for single-origin pour-overs, avocado toasts, and a cozy plant-filled ambience.

TARGET AUDIENCE
Working professionals aged 22–35, college students and remote workers, coffee enthusiasts who appreciate artisan brews.

BRAND & DESIGN DIRECTION
Warm, earthy palette — terracotta, off-white, warm brown, sage green. Modern serif heading paired with clean sans-serif body. Feel: cozy, artisan, approachable. Avoid bright or neon colors. Think lazy Sunday morning.

REQUIRED SECTIONS
1. Hero — Full-width photo banner, tagline "Where Every Cup Tells a Story", two CTAs: "Reserve a Table" (primary) and "View Menu" (secondary scroll link).
2. About — 2–3 sentences about the café's origin story, one image, founded year.
3. Signature Menu — 6 items with image placeholder, name, short description, price (pour-over ₹180, cold brew ₹220, avocado toast ₹320, etc.).
4. Ambience Gallery — 4–6 image placeholders in a grid or masonry layout showing café interiors.
5. Location & Hours — Embed map placeholder, full address, opening hours (Mon–Fri 7am–9pm, Sat–Sun 8am–10pm).
6. Footer — Instagram/Facebook links, address, "© 2024 Brewmosa".

CTA GOAL
Primary action: WhatsApp or reservation form click. Secondary: menu scroll engagement.

DESIGN NOTES
Use soft drop shadows, rounded corners on cards. No harsh lines. The page should feel like stepping into a warm room.
""",
    },
    {
        'title': 'FitLife Studio — Personal Trainer Lead Generation Page',
        'tags': 'fitness, personal-trainer, lead-gen, beginner',
        'description': """\
DIFFICULTY: Beginner
SITE TYPE: Single Page

CLIENT BACKGROUND
FitLife Studio is a boutique personal training studio in Mumbai run by certified trainer Rahul Mehta. He has 8 years of experience, specialises in weight loss and muscle building, and works with 20+ clients per week. He's transitioning from referral-only to online discovery.

TARGET AUDIENCE
Working professionals aged 28–45 who are too busy for big gyms, people wanting personalised and accountable training, and corporate clients looking for in-office or home sessions.

BRAND & DESIGN DIRECTION
Bold, energetic palette — dark charcoal, electric blue, white. Heavy fonts for headlines. Feel: motivating, professional, results-driven. Use strong contrast. This is not a yoga studio — it should feel powerful.

REQUIRED SECTIONS
1. Hero — Dark full-width background, headline "Transform Your Body in 90 Days — Guaranteed", short sub-headline, CTA button "Book Free Consultation". Optional: a stat strip below the hero (200+ Clients | 8 Years Experience | 94% Success Rate).
2. Pain Points — 3 cards describing common struggles: "No Time", "Not Seeing Results", "Wrong Guidance" — each with a short empathetic line.
3. About Rahul — Trainer photo, credentials (ACE Certified, NSCA, etc.), 3–4 sentence bio.
4. Services / Packages — 3 cards: Starter (3x/week), Elite (5x/week), Pro (Daily + nutrition). Each with features listed and price/month.
5. Transformation Results — Before/after image grid, 4 placeholders. Caption each with goal achieved.
6. Testimonials — 3–4 client quotes with name, photo placeholder, and result ("Lost 14kg in 12 weeks").
7. FAQ — 4 questions: How quickly will I see results? Do you offer home sessions? What if I miss a session? Is nutrition guidance included?
8. Bottom CTA Banner — Full-width coloured section "Ready to Start? Your First Session is Free" + button.

CTA GOAL
"Book Free Consultation" → contact form or calendar booking placeholder. Lead capture: name + phone.

DESIGN NOTES
Use bold typography for numbers and stats. The "pain points" section should feel like you're reading the user's mind. Pricing section must be clear and easy to compare.
""",
    },
    {
        'title': 'Pawsome Grooming — Pet Salon Appointment Page',
        'tags': 'pets, grooming, local-business, beginner',
        'description': """\
DIFFICULTY: Beginner
SITE TYPE: Single Page

CLIENT BACKGROUND
Pawsome Grooming is a premium pet grooming salon in Pune offering bath, blow-dry, haircut, nail trimming, ear cleaning, and spa treatments for dogs and cats. They want a cheerful, trust-building page to drive appointment bookings and establish credibility in a growing market.

TARGET AUDIENCE
Pet owners aged 25–45, dog and cat owners who prioritise quality over price, first-time pet owners looking for professional guidance.

BRAND & DESIGN DIRECTION
Cheerful and playful — light pastel backgrounds (mint green, soft lavender, peach). Friendly, rounded UI elements — rounded cards, soft borders. Lots of cute pet imagery using placeholders. Feel: safe, fun, and genuinely caring. Avoid anything clinical.

REQUIRED SECTIONS
1. Hero — Smiling dog photo or illustration, headline "Your Pet Deserves the Best Day Ever", CTA "Book an Appointment".
2. Services — 6 service cards with icon, name, short description, and price: Bath & Blow-dry (₹499), Haircut (₹699), Nail Trim (₹199), Ear Cleaning (₹199), Full Grooming Package (₹999), Spa Treatment (₹1299).
3. Why Pawsome — 4 trust points with icons: Certified Groomers, Stress-Free Environment, Cruelty-Free Products, Free Pick-up & Drop (within 5km).
4. How It Works — 3 simple steps: Book Online → We Pick Up Your Pet → Get Them Back Fresh & Happy.
5. Reviews — 3 pet owner reviews in Google-review card style, with star rating, pet name, and photo placeholder.
6. Appointment Booking Form — Pet name, owner name, phone, pet type (dog/cat), breed, service selection (checkboxes), preferred date.
7. Footer — Address, phone, Instagram gallery feed placeholder, "© 2024 Pawsome Grooming".

CTA GOAL
Direct appointment booking via the form. Reduce friction — 6 fields max.

DESIGN NOTES
Each service card should feel delightful. Use rounded badges for "Most Popular" on the grooming package. The "How It Works" section should feel reassuring — pet owners are anxious about leaving their pets with strangers.
""",
    },

    # ─────────────────────────────────────────────────────────
    # MEDIUM (4–7)
    # ─────────────────────────────────────────────────────────
    {
        'title': 'TaskFlow — SaaS Project Management Tool Launch Page',
        'tags': 'saas, b2b, product-launch, medium',
        'description': """\
DIFFICULTY: Medium
SITE TYPE: Single Page

CLIENT BACKGROUND
TaskFlow is a new SaaS project management tool targeting small teams and freelancers — think a simpler Notion/Asana hybrid. Built by a 3-person team. Free plan available; Pro plan at ₹999/month. Key differentiator: AI-powered task prioritisation + beautiful UX. Goal: 1,000 beta users in 3 months.

TARGET AUDIENCE
Freelancers and indie hackers, small startup teams of 2–15 people, and project managers tired of bloated tools like Jira.

BRAND & DESIGN DIRECTION
Modern SaaS aesthetic — white background, deep navy (#0A1628), soft purple accent (#7C3AED). Product screenshots prominently featured. Clean whitespace, confident typography (Inter or similar). Feel: polished, modern, trustworthy, and fast.

REQUIRED SECTIONS
1. Sticky Header — Logo left, nav links (Features / Pricing / Testimonials), "Start Free" CTA button right.
2. Hero — Punchy headline "Ship Projects Faster with AI-Powered Task Management", 2-line sub-copy, product dashboard mockup/placeholder, two CTAs: "Get Early Access — Free" and "Watch 2-min Demo".
3. Social Proof Strip — 6 company logos or "Loved by teams at [Company A, B, C]" + 4.9/5 stars from Product Hunt/G2.
4. Problem → Solution Split — Left: "The old way" (chaotic bullet list: missed deadlines, endless meetings, spreadsheet chaos). Right: "The TaskFlow way" (clean list with checkmarks).
5. Key Features — 3–4 feature blocks each with: icon, title, one-sentence description, and a product screenshot placeholder.
6. How It Works — 3 steps: Create a Project → Assign Tasks → AI Prioritises Your Day.
7. Pricing Table — 3 tiers: Free (₹0, 3 projects, 1 user), Pro (₹999/mo, unlimited, AI features), Team (₹2499/mo, 10 seats, admin controls). Include a feature comparison table.
8. Testimonials — 3 beta user quotes with photo placeholder, name, and title (e.g., "Freelance Designer", "Startup Founder").
9. FAQ — 5 questions: Is there a free plan? Can I import from Trello? Is my data secure? Do I need a credit card? Can I cancel anytime?
10. Final CTA Section — "Join 1,200+ teams already using TaskFlow" + email input + "Start Free" button.

CTA GOAL
Email capture for free account creation. Primary metric: signups from the hero CTA.

DESIGN NOTES
The hero section must communicate what TaskFlow does in under 5 seconds. A visitor should NOT have to read to understand. Pricing must be scannable — use a highlight or badge on the "Pro" tier. The FAQ should address the #1 objection: "Is this just another project tool?"
""",
    },
    {
        'title': 'NestWise Realty — Luxury Villa Pre-Launch Lead Page',
        'tags': 'real-estate, lead-gen, luxury, medium',
        'description': """\
DIFFICULTY: Medium
SITE TYPE: Single Page

CLIENT BACKGROUND
NestWise Realty is a premium real estate consultancy in Hyderabad launching "NestWise The Pinnacle" — a gated villa community with 200+ units. Price range: ₹1.2Cr – ₹3.5Cr. RERA approved. This page is a pre-launch lead capture page. Every lead is worth ₹15,000–₹50,000 in commission to the developer.

TARGET AUDIENCE
Families with household income of ₹30L+ per year, NRIs looking to invest in Indian real estate, and upgrade buyers moving from apartments to villas. These are high-intent, quality buyers — not browsers.

BRAND & DESIGN DIRECTION
Premium and aspirational — deep midnight blue (#0D1B2A), gold accent (#C9A84C), white. Luxury residential photography as placeholders. Trust signals throughout: RERA number, developer track record, award badges. Feel: exclusive, secure, aspirational. Avoid budget real estate clichés.

REQUIRED SECTIONS
1. Hero — Full-screen property image background, headline "Live Above the Ordinary", tagline "200+ Premium Villas | Gated Community | Hyderabad", and a lead capture form on the right side of the hero with fields: Name, Phone, Email, Budget Range (dropdown: ₹1Cr–₹2Cr / ₹2Cr–₹3.5Cr / ₹3.5Cr+), Unit Type (3BHK Villa / 4BHK Villa / Penthouse). CTA: "Request a Callback".
2. Project Highlights — 4 stat boxes: 200+ Villas, 5 Acres Landscaped, 40+ Amenities, RERA Approved (show RERA number).
3. Unit Types & Pricing — 3 cards: 3BHK Villa (2200 sqft, starting ₹1.2Cr), 4BHK Villa (3100 sqft, starting ₹1.9Cr), 4BHK Penthouse (4200 sqft, starting ₹2.8Cr). Each with floor plan image placeholder and a "Download Brochure" link.
4. Amenities Grid — 12 amenities with icons: Infinity Pool, Clubhouse, EV Charging Bays, 24/7 Security, Children's Play Area, Gymnasium, Co-working Lounge, Amphitheatre, Jogging Track, Smart Home Ready, Solar Power Backup, Pet-friendly Zone.
5. Location Advantages — Embedded map placeholder + 5 location benefits: 15 mins to Hitech City, 10 mins to Gachibowli, Metro Station nearby, International School 2km, Star Hospital 3km.
6. Developer Track Record — "NestWise Realty: 12 Years | 4,200+ Homes Delivered | 98% on-time possession". Brief paragraph + photo of a completed project.
7. Site Visit CTA — Full-width banner: "See It to Believe It — Schedule a Free Site Visit" + "Book Site Visit" button.
8. Second Lead Form — Same form as hero, at the bottom. A visitor who scrolled all the way needs a second chance to convert.

CTA GOAL
Lead capture: Name + Phone minimum. Callback promise within 2 hours during business hours. This is a high-value B2C sale — every lead matters.

DESIGN NOTES
The enquiry form MUST appear early (hero) and late (bottom). Real estate pages lose 60% of potential leads if the form is only at the bottom. Use gold accents sparingly — too much looks cheap. Trust signals (RERA, awards) should appear near CTAs.
""",
    },
    {
        'title': 'SkillBridge — Digital Marketing Mastery Course Page',
        'tags': 'edtech, course, conversion, medium',
        'description': """\
DIFFICULTY: Medium
SITE TYPE: Single Page

CLIENT BACKGROUND
SkillBridge is launching "The Complete Digital Marketing Mastery Course" — a 40-hour online program covering SEO, Google Ads, Meta Ads, Content Marketing, Email Marketing, and Google Analytics. Price: ₹4,999 (regular ₹8,999). Launch discount ends in 72 hours. This is a direct-sales page — every visitor should convert or leave their email.

TARGET AUDIENCE
Fresh graduates looking for job-ready digital skills, marketing professionals wanting to upskill or switch roles, and small business owners who want to run their own ad campaigns.

BRAND & DESIGN DIRECTION
Clean and educational — white background, vibrant orange (#FF6B35), dark grey (#1A1A2E). Large, outcome-focused typography. Promo video thumbnail above the fold. Feel: professional, credible, motivating, and urgent.

REQUIRED SECTIONS
1. Hero — Video thumbnail on left (play button overlay), right side: headline "Become a Certified Digital Marketer in 40 Hours", 5 bullet benefits (get hired faster, run profitable ads, master SEO, etc.), price block showing ₹8,999 struck out and ₹4,999 highlighted, countdown timer "Offer ends in [X] hours", CTA "Enroll Now at ₹4,999".
2. What You'll Learn — 8 outcome-focused bullets: "Run Google Search Ads profitably from Day 1", "Rank on Page 1 of Google in 60 days", etc. — results-oriented language, not syllabus topics.
3. Course Curriculum — Accordion with 6 modules: Module 1: SEO Fundamentals (5 topics), Module 2: Google Ads (6 topics), Module 3: Meta & Instagram Ads (5 topics), Module 4: Content Marketing (4 topics), Module 5: Email Marketing (4 topics), Module 6: Analytics & Reporting (4 topics). Each module shows time duration.
4. Instructor Bio — Photo, name "Priya Sharma", credentials (7 years, ex-Google, trained 3,000+ students), and a one-liner quote.
5. Student Success Stories — 3 mini case studies: "Pradeep got hired at ₹6.5 LPA after this course", "Sunita scaled her salon's revenue 3x using Meta Ads", "Arjun freelances and earns ₹80K/month now".
6. What's Included — Feature list with icons: 40+ hours of HD video, Lifetime access + future updates, 6 live Q&A sessions/month, 4 hands-on projects, Course completion certificate, Private community access, 1-year placement support.
7. Pricing Block — One option (₹4,999) with all features listed, and an "₹8,999" original price struck through. Add a "30-day money-back guarantee" badge prominently.
8. Countdown Timer — "Enroll before [date] to get the early-bird price + bonus Meta Ads module (worth ₹1,999)". Use a visible digital countdown.
9. FAQ — 6 questions: Who is this course for? Do I need any prior experience? Is the certificate recognised? What if I have questions? Is there a refund policy? Can I pay in instalments?
10. Final CTA — "Join 3,200+ students who've transformed their careers" + "Enroll Now" button + money-back badge.

CTA GOAL
Direct purchase at ₹4,999. The page must create urgency (timer, limited seats, price increase) while building trust (instructor credibility, testimonials, money-back guarantee).

DESIGN NOTES
Place the countdown timer near the price block AND in the sticky header or a sticky bottom bar. The testimonials section should feel like real people, not marketing copy — use casual, specific language. Every section should nudge toward purchase.
""",
    },
    {
        'title': 'CloudBite — Healthy Food Delivery Brand Page',
        'tags': 'food, delivery, d2c, health, medium',
        'description': """\
DIFFICULTY: Medium
SITE TYPE: Single Page

CLIENT BACKGROUND
CloudBite is a cloud kitchen brand in Chennai specialising in healthy, calorie-tracked meal bowls — think Salad Days or Eat.Fit. All meals are prepared fresh daily with no preservatives. Delivery within 45 minutes. Target: 500 daily orders within 6 months of launch.

TARGET AUDIENCE
Health-conscious professionals aged 25–40, gym-goers and fitness enthusiasts tracking macros, and people trying to maintain their diet while eating out frequently.

BRAND & DESIGN DIRECTION
Fresh and appetising — white base, emerald green (#1A6B3C), warm cream (#FFF8F0), pops of coral for CTAs. Food photography-forward — every section needs a strong food image. Clean, mobile-first layout (80% of orders come from mobile). Feel: fresh, energetic, trustworthy.

REQUIRED SECTIONS
1. Hero — Full-width food photography, headline "Healthy. Tasty. Delivered in 45 Mins", location input field ("Enter your area to check delivery"), CTA "Order Now". Sub-text: "500+ calories saved. Zero compromise on taste."
2. Today's Specials — 3 featured bowls with large image, bowl name, short description, calorie count, macros (P/C/F), price, and "Add to Cart" button.
3. Menu Categories — Visual category tabs/grid: Protein Bowls, Vegan, Keto-Friendly, High-Carb (for athletes), Low-Cal (<400 kcal), Chef's Special. Clicking a category shows 3–4 sample items.
4. Why CloudBite — 4 value propositions with icons: Fresh Daily (prepared same day, never frozen), Calorie Counted (macro info on every item), Delivered Hot (insulated packaging, 45-min SLA), Chef-Grade Ingredients (no preservatives, no MSG).
5. How It Works — 3 steps: Choose Your Meal → Place Your Order → Delivered Fresh to You.
6. Nutrition Philosophy — "We believe healthy food shouldn't taste like cardboard." Short paragraph about sourcing, no artificial additives, and showing a simple ingredient label placeholder.
7. Customer Reviews — 4 reviews with star rating (4.7+), customer name, location, and specific meal they loved.
8. Subscription Plans — "Subscribe & Save 20%" — 3 plan cards: 5-day Weekday Plan (₹999/week), 7-day Full Week Plan (₹1,299/week), Monthly Meal Prep Plan (₹3,999/month). Benefits: priority delivery, locked-in pricing, free diet consultation.
9. App Download Section — Phone mockup placeholder, "Order faster on the app", App Store and Play Store badge buttons.

CTA GOAL
First order placement. Secondary: subscription plan sign-up. Impulse purchases driven by food imagery.

DESIGN NOTES
The menu items must look delicious — use high-quality placeholder images from food-specific sources. Calorie and macro data builds trust with health-conscious users — don't hide it. The subscription section should feel like a financial win, not a commitment.
""",
    },

    # ─────────────────────────────────────────────────────────
    # ADVANCED (8–10)
    # ─────────────────────────────────────────────────────────
    {
        'title': 'Zephyr S1 — Electric Scooter Launch Microsite',
        'tags': 'automotive, ev, product-launch, multi-page, advanced',
        'description': """\
DIFFICULTY: Advanced
SITE TYPE: Multi-Page (Home | Features | Design)
NOTE: This is a multi-page project. Use the Pages panel in the builder to create three pages: Home, Features, and Design. Link them in the navigation.

CLIENT BACKGROUND
Zephyr Motors is launching India's first solar-assisted electric scooter — the "Zephyr S1". Founded by ex-Ola Electric and TVS engineers. Launch price: ₹89,999. Key specs: 150km range, 4-hour full charge, 0–60kmph in 5.2 seconds, solar-assist panel adds 15–20km of daily range. Target: 10,000 pre-bookings before launch. Pre-booking deposit: ₹999 (fully refundable).

TARGET AUDIENCE
Urban professionals aged 28–45 in Tier-1 cities, eco-conscious early adopters willing to pay a premium, and daily commuters spending ₹5,000–₹8,000/month on fuel who can justify the investment.

BRAND & DESIGN DIRECTION
Premium dark theme — matte black (#0D0D0D), electric blue (#0066FF), silver chrome (#C0C0C0), white text. Full-screen cinematic hero sections. Think Tesla.com or Rivian.com. Every section should feel like it belongs in a product film. Feel: futuristic, premium, aspirational, engineer-built.

PAGE 1: HOME
1. Sticky Nav — Logo (Zephyr), links to Features and Design pages, CTA "Pre-Book at ₹999".
2. Cinematic Hero — Full-screen dark background with scooter render placeholder. Minimal text: "The Future of Urban Mobility". Sub-line: "150km Range | Solar Assist | Pre-book at ₹999". Two CTAs: "Pre-Book Now" and "Explore Features".
3. Key Specs Strip — 4 stats in high contrast: 150km Range | 5.2s 0–60 | Solar Assist | RTO-Exempt.
4. Feature Highlights — 3 full-width alternating sections (image left, text right, then flip): Solar Intelligence (how the panel works), Responsive Performance (acceleration, handling), and Connected Ride (app, GPS, OTA updates).
5. Pre-Booking Form — Dark card: "Be Among the First 10,000" — Name, Phone, City (dropdown of 10 metros), Colour Preference (Midnight Black / Storm Blue / Arctic White / Lava Red), CTA "Secure My Zephyr S1 — ₹999".
6. Pre-booking Counter — "8,247 pre-bookings and counting" (social proof).
7. Press & Recognition — 3–4 press logo placeholders with quotes: "India's Tesla Moment" — [Publication].
8. Footer — Links to all pages, social icons, legal note, "© 2024 Zephyr Motors Pvt. Ltd."

PAGE 2: FEATURES
1. Nav (consistent with Home).
2. Solar Technology — Full-width section explaining the solar assist panel with a diagram placeholder. Key stat: "Generate up to 20km of free daily range".
3. Battery & Range — Visual range comparison: Zephyr S1 (150km) vs competitor averages (80km). Charging breakdown: 0–80% in 2.5 hours, full charge in 4 hours.
4. Ride Intelligence — Smart features: regenerative braking, hill-hold assist, theft alert, live GPS, OTA firmware updates.
5. App Preview — Phone mockup showing Zephyr app: route planning, battery health, service booking, community.
6. Tech Specifications — Clean table: Motor (3kW BLDC), Battery (3.5kWh Li-NMC), Top Speed (80kmph), Warranty (3 years / 30,000km), Weight (112kg).

PAGE 3: DESIGN
1. Nav (consistent).
2. Colour Configurator — 4 large colour swatch buttons: Midnight Black, Storm Blue, Arctic White, Lava Red. Clicking should highlight the swatch (JS). Show a scooter silhouette placeholder that changes context text to the selected colour's name.
3. Design Language — 3 detail shot placeholders: LED headlight strip, alloy wheel, handlebar panel. Each with a 2-line design philosophy caption.
4. Ergonomics — Side profile diagram placeholder with annotations: seat height 790mm, leg room, storage under seat (28L).
5. Pre-booking CTA — Bottom strip with "Choose Your Colour and Pre-Book" + form or button.

CTA GOAL
₹999 pre-booking deposit. This is a high-intent purchase page. Every section should build desire and reduce hesitation. The refundable nature of the deposit removes financial risk — use it prominently.

DESIGN NOTES
Dark backgrounds with electric blue accents. Typography should be bold and minimal. Never clutter — Tesla's homepage uses extreme whitespace. The solar feature is the hero differentiator — dedicate significant visual real estate to explaining it simply. The pre-booking counter adds urgency.
""",
    },
    {
        'title': 'Finspark — Neobank App Landing Page',
        'tags': 'fintech, neobank, app-launch, trust, advanced',
        'description': """\
DIFFICULTY: Advanced
SITE TYPE: Single Page

CLIENT BACKGROUND
Finspark is a neobank targeting Gen-Z and young millennials (18–28). It's a savings + investments + debit card app. Zero balance account, 4% interest on savings, instant UPI, 1-click mutual fund investments, and a Visa debit card with 1% cashback. RBI licensed through IDFC Bank as a banking partner. Available on iOS and Android. 5 lakh users in 18 months.

TARGET AUDIENCE
College students and first-jobbers aged 18–28, people new to investing and savings, and those frustrated by clunky traditional bank UX. This is a generation that opens apps before filling out paperwork.

BRAND & DESIGN DIRECTION
Bold and youthful — deep indigo/purple (#2D1B69), neon mint (#00F5C4), white, soft lavender (#E8E0FF). Phone mockups are central to every section. Trust signals must be visible — RBI logo, partner bank logo, security badges. Feel: trustworthy yet exciting, modern, Gen-Z energy. Think Zepto or CRED aesthetic.

REQUIRED SECTIONS
1. Sticky Nav — Finspark logo, links (Features / How It Works / Security / Download), "Download App" CTA button in accent colour.
2. Hero — Split layout: left side — headline "Banking That Actually Gets You", 3 bullet benefits (Zero balance | 4% on savings | 1% cashback), App Store + Play Store download buttons, and "4.8★ on App Store"; right side — phone mockup showing the app dashboard (placeholder).
3. Social Proof Strip — "5L+ Users | ₹200Cr+ Deposits Managed | RBI Licensed | 4.8★ App Store Rating".
4. Features Grid — 6 feature cards with icon, title, one-line description: Zero Balance Account (no minimum balance, ever), 4% Savings Rate (2× the national average), Smart Budgets (auto-categorise your spending), 1-Click Investments (start SIPs from ₹100), Instant UPI & Payments, Cashback Visa Card (1% on all spends).
5. How It Works — 4 steps with phone screen placeholder per step: Download App → Enter PAN + Aadhaar → Video KYC in 3 mins → Start Banking Immediately.
6. Savings Calculator — Interactive section: "How much could your money grow?" — slider for monthly savings amount (₹1,000–₹50,000). Show projected balance at 1 year, 5 years, 10 years at 4% vs 2.7% (savings account average). This is a JS-driven component — design the layout, even if the calculation is approximate.
7. Security Section — "Your Money is Completely Safe" — 4 trust badges with explanation: RBI Licensed (via IDFC Bank), DICGC Insured up to ₹5L, 256-bit Encryption, Biometric Authentication. This section must feel weighty and serious, not dismissive.
8. User Reviews — 5 reviews with profile photo placeholder, name, age, city, and a one-liner: "Opened my first investment at 20 — thanks Finspark", "Finally a bank that doesn't charge me for existing".
9. App Download Section — Full-width dark background, phone mockup, headline "Download Finspark. Start in 3 Minutes.", App Store and Play Store badge buttons, QR code placeholder.
10. Footer — Links, "Banking services provided by IDFC First Bank", RBI disclosure text, privacy policy, "© 2024 Finspark Technologies Pvt. Ltd."

CTA GOAL
App download (App Store / Play Store). Every section should reduce the single biggest objection to neobanks: "Is my money actually safe?"

DESIGN NOTES
Financial products have a trust problem with Gen-Z. Every section should have at least one trust signal. The savings calculator is a key engagement tool — make it visually prominent. The hero must immediately communicate that this is a real, licensed bank — not a startup experimenting with your money. Use the RBI logo appropriately.
""",
    },
    {
        'title': 'Lumina Wellness — Corporate Wellness Platform B2B Page',
        'tags': 'saas, b2b, wellness, hr-tech, multi-page, advanced',
        'description': """\
DIFFICULTY: Advanced
SITE TYPE: Multi-Page (Home — For HR Teams | For Employees)
NOTE: This is a multi-page project. Use the Pages panel in the builder to create two pages. The Home/HR page is the primary sales page. The "For Employees" page is a secondary, softer page for internal sharing.

CLIENT BACKGROUND
Lumina is a corporate wellness SaaS platform that companies subscribe to for their employees. It combines mental health (therapy sessions with licensed counsellors), physical health (video workout plans), and nutrition (personalised meal plans). Pricing: ₹299/employee/month. Currently 150+ companies using Lumina. Backed by a Series A (₹42Cr). Integrates with Slack and Microsoft Teams.

TARGET AUDIENCE (PRIMARY — PAGE 1)
HR Managers, CHROs, and Heads of People at companies with 50–5,000 employees. These are B2B buyers who evaluate ROI, have procurement processes, and need to justify the expense to finance teams. They care about: attrition reduction, productivity, compliance with employee welfare policies, and ease of rollout.

TARGET AUDIENCE (SECONDARY — PAGE 2)
Employees of companies evaluating or already using Lumina. The tone is warmer and more personal here.

BRAND & DESIGN DIRECTION
Clean and professional with warmth — sage green (#4CAF7D), white, deep navy (#0A2540). Corporate yet human — not clinical or pharmaceutical. Data and ROI-driven (HR buyers need numbers). Feel: trustworthy, enterprise-grade, compassionate.

PAGE 1: HOME (HR-FOCUSED MARKETING PAGE)
1. Sticky Nav — Lumina logo, links (Solutions / Pricing / Case Studies / Resources), "Book a Demo" CTA button.
2. Hero — Bold headline "Reduce Burnout. Boost Productivity. Retain Your Best People." Sub-copy: "Lumina gives your employees on-demand access to therapy, fitness, and nutrition — all in one app." Two CTAs: "Book a Free Demo" (primary) and "See How It Works" (scroll). Company logos using Lumina below the hero (6 logo placeholders).
3. The Problem — "Employee burnout is costing you more than you think." Stats section: 65% of Indian employees report moderate-to-high burnout (SHRM 2024), Average cost of replacing one employee: ₹4.2 lakh, Companies with wellness programmes see 28% lower attrition. Each stat in a large number + context format.
4. Solutions Tabs — 3 tabs: Mental Health (therapy sessions, self-help content, crisis support), Physical Health (video workouts, step challenges, health screenings), Nutrition (personalised meal plans, nutritionist consultations, calorie tracking). Each tab shows 4 features with icons.
5. How It Works for Companies — 4 steps: Sign Up & Set Budget → Employees Download App → They Book Sessions → You Get Reports. Clean step illustration placeholders.
6. ROI Calculator — "Calculate your savings with Lumina." Input: number of employees (slider 50–5000). Output: Estimated annual attrition cost saved, estimated sick-day reduction, ROI in months. Design this as a prominent interactive section even if the calculation is approximate.
7. Case Studies — 2 case studies in card format: "TechCorp (1,200 employees): Reduced attrition by 34% in 12 months using Lumina's therapy programme." and "RetailChain (3,400 employees): 22% drop in sick leaves, ₹1.8Cr saved annually." Each with company placeholder logo, challenge, solution, and result metric.
8. Integrations — "Lumina works with your existing tools." Logos of: Slack, Microsoft Teams, Workday, Darwinbox, GreytHR, Google Workspace, Zoho People.
9. Pricing — 3 tiers: Starter (₹199/employee/month, up to 100 employees, mental health only), Growth (₹299/employee/month, all three pillars, up to 500 employees), Enterprise (Custom pricing, 500+ employees, dedicated CSM, custom integrations). Annual billing discount of 20%.
10. Trust & Compliance — "Your employees' data is protected." Badges: DPDP Act compliant, ISO 27001, HIPAA-aligned, End-to-end encryption, Therapists verified by RCI. Brief explanation paragraph.
11. Final CTA — "Your team deserves better. Let's talk." — Name, Company, Number of Employees (dropdown), "Book a Demo" button. Promise: "Our team will reach out within 4 business hours."

PAGE 2: FOR EMPLOYEES
1. Nav — Consistent but simplified. "Download App" CTA instead of "Book Demo".
2. Hero — Warm tone: headline "Your Company is Taking Care of You." Sub-copy: "Lumina gives you private, confidential access to therapists, fitness coaches, and nutritionists — fully paid by your employer." CTA: "Download the App" + "Sign Up with Company Email".
3. What's Included — 3 feature cards with icons: Therapy (licensed counsellors, private sessions, 24/7 chat), Fitness (guided workouts, yoga, step challenges), Nutrition (meal plans, nutritionist chat, calorie tracker).
4. It's Completely Private — "Your employer sees only anonymised, aggregated data — never your individual sessions or health records." Trust statement with a privacy badge.
5. How to Get Started — 3 steps: Download the Lumina app → Sign up with your work email → Book your first session (free).
6. App Screens — 3–4 phone screen placeholders showing different parts of the app.
7. Footer — Privacy policy, terms, App Store / Play Store links.

CTA GOAL
Page 1: Demo booking with lead form (company name + headcount). Page 2: App download + sign-up.

DESIGN NOTES
Page 1 must feel enterprise-grade — this is a ₹15L–₹1.5Cr annual contract for larger companies. Every claim needs a number behind it. The ROI calculator is the most powerful section — make it impossible to miss. Page 2 must feel personal, warm, and low-pressure — employees are often sceptical about company wellness programmes. Address the "Is it really private?" concern explicitly and prominently.
""",
    },
]


class Command(BaseCommand):
    help = 'Load 10 sample design studio projects (beginner → advanced)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete ALL existing DesignProject records before loading',
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update description/tags even if a project with the same title already exists',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count, _ = DesignProject.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {count} existing project(s).'))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for data in PROJECTS:
            existing = DesignProject.objects.filter(title=data['title']).first()

            if existing:
                if options['update']:
                    existing.description = data['description']
                    existing.tags = data['tags']
                    existing.is_active = True
                    existing.save(update_fields=['description', 'tags', 'is_active', 'updated_at'])
                    self.stdout.write(f'  Updated : {data["title"]}')
                    updated_count += 1
                else:
                    self.stdout.write(f'  Skipped : {data["title"]} (already exists, use --update to overwrite)')
                    skipped_count += 1
            else:
                DesignProject.objects.create(
                    title=data['title'],
                    description=data['description'],
                    tags=data['tags'],
                    is_active=True,
                )
                self.stdout.write(f'  Created : {data["title"]}')
                created_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done — {created_count} created, {updated_count} updated, {skipped_count} skipped.'
        ))
        self.stdout.write('')
        self.stdout.write('To export as a fixture for production:')
        self.stdout.write(self.style.HTTP_INFO(
            '  python manage.py dumpdata design_studio.DesignProject --indent 2 --natural-foreign '
            '> design_studio/fixtures/design_projects.json'
        ))
        self.stdout.write('Then on production run:')
        self.stdout.write(self.style.HTTP_INFO(
            '  python manage.py loaddata design_studio/fixtures/design_projects.json'
        ))
