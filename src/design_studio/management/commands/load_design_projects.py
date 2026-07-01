from django.core.management.base import BaseCommand

from design_studio.models import DesignProject

THUMBNAILS = {
    'Brewmosa Cafe - Specialty Coffee Shop Landing Page':
        'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&h=340&q=80',
    'FitLife Studio - Personal Trainer Lead Generation Page':
        'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&h=340&q=80',
    'Pawsome Grooming - Pet Salon Appointment Page':
        'https://images.unsplash.com/photo-1587300003388-59208cc962cb?auto=format&fit=crop&w=600&h=340&q=80',
    'TaskFlow - SaaS Project Management Tool Launch Page':
        'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&h=340&q=80',
    'NestWise Realty - Luxury Villa Pre-Launch Lead Page':
        'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&h=340&q=80',
    'SkillBridge - Digital Marketing Mastery Course Page':
        'https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?auto=format&fit=crop&w=600&h=340&q=80',
    'CloudBite - Healthy Food Delivery Brand Page':
        'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&h=340&q=80',
    'Zephyr S1 - Electric Scooter Launch Microsite':
        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=600&h=340&q=80',
    'Finspark - Neobank App Landing Page':
        'https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=600&h=340&q=80',
    'Lumina Wellness - Corporate Wellness Platform B2B Page':
        'https://images.unsplash.com/photo-1545205597-3d9d02c29597?auto=format&fit=crop&w=600&h=340&q=80',
}

PROJECTS = [
    # BEGINNER (1-3)
    {
        'title': 'Brewmosa Cafe - Specialty Coffee Shop Landing Page',
        'tags': 'cafe, local-business, beginner',
        'description': """<h3>Difficulty</h3>
<p>Beginner | Single Page</p>

<h3>Client Background</h3>
<p>Brewmosa is a specialty coffee shop in Indiranagar, Bangalore. They are launching a second outlet and need a warm, inviting landing page to drive table reservations and walk-ins. Known for single-origin pour-overs, avocado toasts, and a cozy plant-filled ambience.</p>

<h3>Target Audience</h3>
<ul>
  <li>Working professionals aged 22-35</li>
  <li>College students and remote workers</li>
  <li>Coffee enthusiasts who appreciate artisan brews</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Warm, earthy palette: terracotta, off-white, warm brown, sage green. Modern serif heading paired with clean sans-serif body. Feel: cozy, artisan, approachable. Avoid bright or neon colors. Think lazy Sunday morning.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Hero</strong> - Full-width photo banner, tagline "Where Every Cup Tells a Story", two CTAs: "Reserve a Table" (primary) and "View Menu" (secondary scroll link).</li>
  <li><strong>About</strong> - 2-3 sentences about the cafe's origin story, one image, founded year.</li>
  <li><strong>Signature Menu</strong> - 6 items with image placeholder, name, short description, price (pour-over 180, cold brew 220, avocado toast 320, etc.).</li>
  <li><strong>Ambience Gallery</strong> - 4-6 image placeholders in a grid or masonry layout showing cafe interiors.</li>
  <li><strong>Location and Hours</strong> - Embed map placeholder, full address, opening hours (Mon-Fri 7am-9pm, Sat-Sun 8am-10pm).</li>
  <li><strong>Footer</strong> - Instagram/Facebook links, address, "2024 Brewmosa".</li>
</ol>

<h3>CTA Goal</h3>
<p>Primary action: WhatsApp or reservation form click. Secondary: menu scroll engagement.</p>

<h3>Design Notes</h3>
<p>Use soft drop shadows, rounded corners on cards. No harsh lines. The page should feel like stepping into a warm room.</p>""",
    },
    {
        'title': 'FitLife Studio - Personal Trainer Lead Generation Page',
        'tags': 'fitness, personal-trainer, lead-gen, beginner',
        'description': """<h3>Difficulty</h3>
<p>Beginner | Single Page</p>

<h3>Client Background</h3>
<p>FitLife Studio is a boutique personal training studio in Mumbai run by certified trainer Rahul Mehta. He has 8 years of experience, specialises in weight loss and muscle building, and works with 20+ clients per week. He's transitioning from referral-only to online discovery.</p>

<h3>Target Audience</h3>
<ul>
  <li>Working professionals aged 28-45 who are too busy for big gyms</li>
  <li>People wanting personalised and accountable training</li>
  <li>Corporate clients looking for in-office or home sessions</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Bold, energetic palette: dark charcoal, electric blue, white. Heavy fonts for headlines. Feel: motivating, professional, results-driven. Use strong contrast. This is not a yoga studio - it should feel powerful.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Hero</strong> - Dark full-width background, headline "Transform Your Body in 90 Days - Guaranteed", short sub-headline, CTA "Book Free Consultation". Stat strip below hero: 200+ Clients | 8 Years Experience | 94% Success Rate.</li>
  <li><strong>Pain Points</strong> - 3 cards: "No Time", "Not Seeing Results", "Wrong Guidance" - each with a short empathetic line.</li>
  <li><strong>About Rahul</strong> - Trainer photo, credentials (ACE Certified, NSCA, etc.), 3-4 sentence bio.</li>
  <li><strong>Services / Packages</strong> - 3 cards: Starter (3x/week), Elite (5x/week), Pro (Daily + nutrition). Each with features listed and price/month.</li>
  <li><strong>Transformation Results</strong> - Before/after image grid, 4 placeholders with goal achieved caption.</li>
  <li><strong>Testimonials</strong> - 3-4 client quotes with name, photo placeholder, and result ("Lost 14kg in 12 weeks").</li>
  <li><strong>FAQ</strong> - 4 questions: How quickly will I see results? Do you offer home sessions? What if I miss a session? Is nutrition guidance included?</li>
  <li><strong>Bottom CTA Banner</strong> - Full-width coloured section "Ready to Start? Your First Session is Free" + button.</li>
</ol>

<h3>CTA Goal</h3>
<p>Book Free Consultation - contact form or calendar booking placeholder. Lead capture: name + phone.</p>

<h3>Design Notes</h3>
<p>Use bold typography for numbers and stats. The "pain points" section should feel like you're reading the user's mind. Pricing section must be clear and easy to compare.</p>""",
    },
    {
        'title': 'Pawsome Grooming - Pet Salon Appointment Page',
        'tags': 'pets, grooming, local-business, beginner',
        'description': """<h3>Difficulty</h3>
<p>Beginner | Single Page</p>

<h3>Client Background</h3>
<p>Pawsome Grooming is a premium pet grooming salon in Pune offering bath, blow-dry, haircut, nail trimming, ear cleaning, and spa treatments for dogs and cats. They want a cheerful, trust-building page to drive appointment bookings.</p>

<h3>Target Audience</h3>
<ul>
  <li>Pet owners aged 25-45</li>
  <li>Dog and cat owners who prioritise quality over price</li>
  <li>First-time pet owners looking for professional guidance</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Cheerful and playful: light pastel backgrounds (mint green, soft lavender, peach). Friendly, rounded UI elements. Lots of cute pet imagery using placeholders. Feel: safe, fun, and genuinely caring. Avoid anything clinical.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Hero</strong> - Smiling dog photo, headline "Your Pet Deserves the Best Day Ever", CTA "Book an Appointment".</li>
  <li><strong>Services</strong> - 6 service cards with icon, name, short description, and price: Bath and Blow-dry (499), Haircut (699), Nail Trim (199), Ear Cleaning (199), Full Grooming Package (999), Spa Treatment (1299).</li>
  <li><strong>Why Pawsome</strong> - 4 trust points with icons: Certified Groomers, Stress-Free Environment, Cruelty-Free Products, Free Pick-up and Drop (within 5km).</li>
  <li><strong>How It Works</strong> - 3 steps: Book Online, We Pick Up Your Pet, Get Them Back Fresh and Happy.</li>
  <li><strong>Reviews</strong> - 3 pet owner reviews in Google-review card style with star rating, pet name, and photo placeholder.</li>
  <li><strong>Appointment Booking Form</strong> - Pet name, owner name, phone, pet type (dog/cat), breed, service selection (checkboxes), preferred date.</li>
  <li><strong>Footer</strong> - Address, phone, Instagram gallery feed placeholder.</li>
</ol>

<h3>CTA Goal</h3>
<p>Direct appointment booking via the form. Reduce friction - 6 fields max.</p>

<h3>Design Notes</h3>
<p>Each service card should feel delightful. Use rounded badges for "Most Popular" on the grooming package. The "How It Works" section should feel reassuring - pet owners are anxious about leaving their pets with strangers.</p>""",
    },

    # MEDIUM (4-7)
    {
        'title': 'TaskFlow - SaaS Project Management Tool Launch Page',
        'tags': 'saas, b2b, product-launch, medium',
        'description': """<h3>Difficulty</h3>
<p>Medium | Single Page</p>

<h3>Client Background</h3>
<p>TaskFlow is a new SaaS project management tool targeting small teams and freelancers - a simpler Notion/Asana hybrid. Built by a 3-person team. Free plan available; Pro plan at 999/month. Key differentiator: AI-powered task prioritisation and beautiful UX. Goal: 1,000 beta users in 3 months.</p>

<h3>Target Audience</h3>
<ul>
  <li>Freelancers and indie hackers</li>
  <li>Small startup teams of 2-15 people</li>
  <li>Project managers tired of bloated tools like Jira</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Modern SaaS aesthetic: white background, deep navy (#0A1628), soft purple accent (#7C3AED). Product screenshots prominently featured. Clean whitespace, confident typography (Inter or similar). Feel: polished, modern, trustworthy, and fast.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Sticky Header</strong> - Logo left, nav links (Features / Pricing / Testimonials), "Start Free" CTA button right.</li>
  <li><strong>Hero</strong> - Headline "Ship Projects Faster with AI-Powered Task Management", product dashboard mockup, two CTAs: "Get Early Access - Free" and "Watch 2-min Demo".</li>
  <li><strong>Social Proof Strip</strong> - 6 company logos + 4.9/5 stars from Product Hunt/G2.</li>
  <li><strong>Problem to Solution Split</strong> - Left: "The old way" (chaotic list: missed deadlines, endless meetings). Right: "The TaskFlow way" (clean checkmarks).</li>
  <li><strong>Key Features</strong> - 3-4 feature blocks each with icon, title, one-sentence description, and product screenshot placeholder.</li>
  <li><strong>How It Works</strong> - 3 steps: Create a Project, Assign Tasks, AI Prioritises Your Day.</li>
  <li><strong>Pricing Table</strong> - 3 tiers: Free (0, 3 projects, 1 user), Pro (999/mo, unlimited, AI features), Team (2499/mo, 10 seats, admin controls). Include feature comparison table.</li>
  <li><strong>Testimonials</strong> - 3 beta user quotes with photo placeholder, name, and title.</li>
  <li><strong>FAQ</strong> - 5 questions: Is there a free plan? Can I import from Trello? Is my data secure? Do I need a credit card? Can I cancel anytime?</li>
  <li><strong>Final CTA Section</strong> - "Join 1,200+ teams already using TaskFlow" + email input + "Start Free" button.</li>
</ol>

<h3>CTA Goal</h3>
<p>Email capture for free account creation. Primary metric: signups from the hero CTA.</p>

<h3>Design Notes</h3>
<p>The hero section must communicate what TaskFlow does in under 5 seconds. Pricing must be scannable - use a highlight or badge on the "Pro" tier. The FAQ should address the #1 objection: "Is this just another project tool?"</p>""",
    },
    {
        'title': 'NestWise Realty - Luxury Villa Pre-Launch Lead Page',
        'tags': 'real-estate, lead-gen, luxury, medium',
        'description': """<h3>Difficulty</h3>
<p>Medium | Single Page</p>

<h3>Client Background</h3>
<p>NestWise Realty is a premium real estate consultancy in Hyderabad launching "NestWise The Pinnacle" - a gated villa community with 200+ units. Price range: 1.2Cr to 3.5Cr. RERA approved. This is a pre-launch lead capture page. Every lead is worth 15,000 to 50,000 in commission.</p>

<h3>Target Audience</h3>
<ul>
  <li>Families with household income of 30L+ per year</li>
  <li>NRIs looking to invest in Indian real estate</li>
  <li>Upgrade buyers moving from apartments to villas</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Premium and aspirational: deep midnight blue (#0D1B2A), gold accent (#C9A84C), white. Luxury residential photography as placeholders. Trust signals throughout: RERA number, developer track record, award badges. Feel: exclusive, secure, aspirational.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Hero</strong> - Full-screen property image background, headline "Live Above the Ordinary", tagline "200+ Premium Villas | Gated Community | Hyderabad". Lead capture form on the right: Name, Phone, Email, Budget Range (dropdown), Unit Type. CTA: "Request a Callback".</li>
  <li><strong>Project Highlights</strong> - 4 stat boxes: 200+ Villas, 5 Acres Landscaped, 40+ Amenities, RERA Approved.</li>
  <li><strong>Unit Types and Pricing</strong> - 3 cards: 3BHK Villa (2200 sqft, starting 1.2Cr), 4BHK Villa (3100 sqft, starting 1.9Cr), 4BHK Penthouse (4200 sqft, starting 2.8Cr). Each with floor plan image placeholder and "Download Brochure" link.</li>
  <li><strong>Amenities Grid</strong> - 12 amenities with icons: Infinity Pool, Clubhouse, EV Charging Bays, 24/7 Security, Children's Play Area, Gymnasium, Co-working Lounge, Amphitheatre, Jogging Track, Smart Home Ready, Solar Power Backup, Pet-friendly Zone.</li>
  <li><strong>Location Advantages</strong> - Embedded map placeholder + 5 location benefits: 15 mins to Hitech City, 10 mins to Gachibowli, Metro Station nearby, International School 2km, Star Hospital 3km.</li>
  <li><strong>Developer Track Record</strong> - "NestWise Realty: 12 Years | 4,200+ Homes Delivered | 98% on-time possession". Brief paragraph + completed project photo.</li>
  <li><strong>Site Visit CTA</strong> - Full-width banner: "See It to Believe It - Schedule a Free Site Visit" + "Book Site Visit" button.</li>
  <li><strong>Second Lead Form</strong> - Same form as hero, at the bottom. A visitor who scrolled all the way needs a second chance to convert.</li>
</ol>

<h3>CTA Goal</h3>
<p>Lead capture: Name + Phone minimum. Callback promise within 2 hours during business hours.</p>

<h3>Design Notes</h3>
<p>The enquiry form MUST appear early (hero) and late (bottom). Use gold accents sparingly. Trust signals (RERA, awards) should appear near CTAs.</p>""",
    },
    {
        'title': 'SkillBridge - Digital Marketing Mastery Course Page',
        'tags': 'edtech, course, conversion, medium',
        'description': """<h3>Difficulty</h3>
<p>Medium | Single Page</p>

<h3>Client Background</h3>
<p>SkillBridge is launching "The Complete Digital Marketing Mastery Course" - a 40-hour online program covering SEO, Google Ads, Meta Ads, Content Marketing, Email Marketing, and Google Analytics. Price: 4,999 (regular 8,999). Launch discount ends in 72 hours.</p>

<h3>Target Audience</h3>
<ul>
  <li>Fresh graduates looking for job-ready digital skills</li>
  <li>Marketing professionals wanting to upskill or switch roles</li>
  <li>Small business owners who want to run their own ad campaigns</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Clean and educational: white background, vibrant orange (#FF6B35), dark grey (#1A1A2E). Large, outcome-focused typography. Promo video thumbnail above the fold. Feel: professional, credible, motivating, and urgent.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Hero</strong> - Video thumbnail on left (play button overlay), right side: headline "Become a Certified Digital Marketer in 40 Hours", 5 bullet benefits, price block showing 8,999 struck out and 4,999 highlighted, countdown timer, CTA "Enroll Now at 4,999".</li>
  <li><strong>What You'll Learn</strong> - 8 outcome-focused bullets: results-oriented language, not syllabus topics.</li>
  <li><strong>Course Curriculum</strong> - Accordion with 6 modules: SEO Fundamentals, Google Ads, Meta and Instagram Ads, Content Marketing, Email Marketing, Analytics and Reporting. Each module shows duration.</li>
  <li><strong>Instructor Bio</strong> - Photo, name "Priya Sharma", credentials (7 years, ex-Google, trained 3,000+ students), and a one-liner quote.</li>
  <li><strong>Student Success Stories</strong> - 3 mini case studies: "Pradeep got hired at 6.5 LPA after this course", "Sunita scaled her salon's revenue 3x using Meta Ads", "Arjun freelances and earns 80K/month now".</li>
  <li><strong>What's Included</strong> - Feature list: 40+ hours of HD video, Lifetime access, 6 live Q&A sessions/month, 4 hands-on projects, Certificate, Private community access, 1-year placement support.</li>
  <li><strong>Pricing Block</strong> - One option (4,999) with all features listed, original price struck through. Add a "30-day money-back guarantee" badge prominently.</li>
  <li><strong>Countdown Timer</strong> - "Enroll before [date] to get the early-bird price + bonus Meta Ads module (worth 1,999)". Use a visible digital countdown.</li>
  <li><strong>FAQ</strong> - 6 questions: Who is this course for? Do I need any prior experience? Is the certificate recognised? What if I have questions? Is there a refund policy? Can I pay in instalments?</li>
  <li><strong>Final CTA</strong> - "Join 3,200+ students who've transformed their careers" + "Enroll Now" button + money-back badge.</li>
</ol>

<h3>CTA Goal</h3>
<p>Direct purchase at 4,999. The page must create urgency (timer, limited seats, price increase) while building trust (instructor credibility, testimonials, money-back guarantee).</p>

<h3>Design Notes</h3>
<p>Place the countdown timer near the price block AND in the sticky header or a sticky bottom bar. Testimonials should feel like real people, not marketing copy. Every section should nudge toward purchase.</p>""",
    },
    {
        'title': 'CloudBite - Healthy Food Delivery Brand Page',
        'tags': 'food, delivery, d2c, health, medium',
        'description': """<h3>Difficulty</h3>
<p>Medium | Single Page</p>

<h3>Client Background</h3>
<p>CloudBite is a cloud kitchen brand in Chennai specialising in healthy, calorie-tracked meal bowls. All meals are prepared fresh daily with no preservatives. Delivery within 45 minutes. Target: 500 daily orders within 6 months of launch.</p>

<h3>Target Audience</h3>
<ul>
  <li>Health-conscious professionals aged 25-40</li>
  <li>Gym-goers and fitness enthusiasts tracking macros</li>
  <li>People trying to maintain their diet while eating out frequently</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Fresh and appetising: white base, emerald green (#1A6B3C), warm cream (#FFF8F0), pops of coral for CTAs. Food photography-forward. Clean, mobile-first layout (80% of orders come from mobile). Feel: fresh, energetic, trustworthy.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Hero</strong> - Full-width food photography, headline "Healthy. Tasty. Delivered in 45 Mins", location input field ("Enter your area to check delivery"), CTA "Order Now".</li>
  <li><strong>Today's Specials</strong> - 3 featured bowls with large image, bowl name, short description, calorie count, macros (P/C/F), price, and "Add to Cart" button.</li>
  <li><strong>Menu Categories</strong> - Visual category tabs/grid: Protein Bowls, Vegan, Keto-Friendly, High-Carb (for athletes), Low-Cal (under 400 kcal), Chef's Special.</li>
  <li><strong>Why CloudBite</strong> - 4 value propositions: Fresh Daily (prepared same day, never frozen), Calorie Counted, Delivered Hot (insulated packaging, 45-min SLA), Chef-Grade Ingredients.</li>
  <li><strong>How It Works</strong> - 3 steps: Choose Your Meal, Place Your Order, Delivered Fresh to You.</li>
  <li><strong>Nutrition Philosophy</strong> - "We believe healthy food shouldn't taste like cardboard." Short paragraph about sourcing with ingredient label placeholder.</li>
  <li><strong>Customer Reviews</strong> - 4 reviews with star rating (4.7+), customer name, location, and specific meal they loved.</li>
  <li><strong>Subscription Plans</strong> - "Subscribe and Save 20%" - 3 plan cards: 5-day Weekday Plan (999/week), 7-day Full Week Plan (1,299/week), Monthly Meal Prep Plan (3,999/month).</li>
  <li><strong>App Download Section</strong> - Phone mockup placeholder, App Store and Play Store badge buttons.</li>
</ol>

<h3>CTA Goal</h3>
<p>First order placement. Secondary: subscription plan sign-up. Impulse purchases driven by food imagery.</p>

<h3>Design Notes</h3>
<p>The menu items must look delicious. Calorie and macro data builds trust with health-conscious users. The subscription section should feel like a financial win, not a commitment.</p>""",
    },

    # ADVANCED (8-10)
    {
        'title': 'Zephyr S1 - Electric Scooter Launch Microsite',
        'tags': 'automotive, ev, product-launch, multi-page, advanced',
        'description': """<h3>Difficulty</h3>
<p>Advanced | Multi-Page (Home, Features, Design)</p>
<p><strong>Note:</strong> This is a multi-page project. Use the Pages panel in the builder to create three pages: Home, Features, and Design. Link them in the navigation.</p>

<h3>Client Background</h3>
<p>Zephyr Motors is launching India's first solar-assisted electric scooter - the "Zephyr S1". Founded by ex-Ola Electric and TVS engineers. Launch price: 89,999. Key specs: 150km range, 4-hour full charge, 0-60kmph in 5.2 seconds, solar-assist panel adds 15-20km of daily range. Target: 10,000 pre-bookings. Pre-booking deposit: 999 (fully refundable).</p>

<h3>Target Audience</h3>
<ul>
  <li>Urban professionals aged 28-45 in Tier-1 cities</li>
  <li>Eco-conscious early adopters willing to pay a premium</li>
  <li>Daily commuters spending 5,000-8,000/month on fuel</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Premium dark theme: matte black (#0D0D0D), electric blue (#0066FF), silver chrome (#C0C0C0), white text. Full-screen cinematic hero sections. Think Tesla.com or Rivian.com. Feel: futuristic, premium, aspirational, engineer-built.</p>

<h3>Page 1: Home</h3>
<ol>
  <li><strong>Sticky Nav</strong> - Logo (Zephyr), links to Features and Design pages, CTA "Pre-Book at 999".</li>
  <li><strong>Cinematic Hero</strong> - Full-screen dark background with scooter render placeholder. Minimal text: "The Future of Urban Mobility". Sub-line: "150km Range | Solar Assist | Pre-book at 999". Two CTAs: "Pre-Book Now" and "Explore Features".</li>
  <li><strong>Key Specs Strip</strong> - 4 stats in high contrast: 150km Range, 5.2s 0-60, Solar Assist, RTO-Exempt.</li>
  <li><strong>Feature Highlights</strong> - 3 full-width alternating sections: Solar Intelligence, Responsive Performance, and Connected Ride.</li>
  <li><strong>Pre-Booking Form</strong> - Dark card: "Be Among the First 10,000" - Name, Phone, City (dropdown of 10 metros), Colour Preference, CTA "Secure My Zephyr S1 - 999".</li>
  <li><strong>Pre-booking Counter</strong> - "8,247 pre-bookings and counting" (social proof).</li>
  <li><strong>Press and Recognition</strong> - 3-4 press logo placeholders with quotes: "India's Tesla Moment" - [Publication].</li>
  <li><strong>Footer</strong> - Links to all pages, social icons, legal note.</li>
</ol>

<h3>Page 2: Features</h3>
<ol>
  <li>Solar Technology section with diagram placeholder. Key stat: "Generate up to 20km of free daily range".</li>
  <li>Battery and Range visual comparison: Zephyr S1 (150km) vs competitor averages (80km).</li>
  <li>Ride Intelligence: regenerative braking, hill-hold assist, theft alert, live GPS, OTA firmware updates.</li>
  <li>App Preview with phone mockup.</li>
  <li>Tech Specifications table: Motor, Battery, Top Speed, Warranty, Weight.</li>
</ol>

<h3>Page 3: Design</h3>
<ol>
  <li>Colour Configurator - 4 large colour swatch buttons: Midnight Black, Storm Blue, Arctic White, Lava Red. Clicking should highlight the swatch (JS).</li>
  <li>Design Language - 3 detail shot placeholders with 2-line design philosophy captions.</li>
  <li>Ergonomics - Side profile diagram placeholder with annotations: seat height 790mm, leg room, storage under seat (28L).</li>
  <li>Pre-booking CTA at bottom.</li>
</ol>

<h3>CTA Goal</h3>
<p>999 pre-booking deposit. The refundable nature of the deposit removes financial risk - use it prominently.</p>

<h3>Design Notes</h3>
<p>Dark backgrounds with electric blue accents. Typography should be bold and minimal. The solar feature is the hero differentiator - dedicate significant visual real estate to explaining it simply. The pre-booking counter adds urgency.</p>""",
    },
    {
        'title': 'Finspark - Neobank App Landing Page',
        'tags': 'fintech, neobank, app-launch, trust, advanced',
        'description': """<h3>Difficulty</h3>
<p>Advanced | Single Page</p>

<h3>Client Background</h3>
<p>Finspark is a neobank targeting Gen-Z and young millennials (18-28). Savings + investments + debit card app. Zero balance account, 4% interest on savings, instant UPI, 1-click mutual fund investments, and a Visa debit card with 1% cashback. RBI licensed through IDFC Bank as a banking partner. Available on iOS and Android. 5 lakh users in 18 months.</p>

<h3>Target Audience</h3>
<ul>
  <li>College students and first-jobbers aged 18-28</li>
  <li>People new to investing and savings</li>
  <li>Those frustrated by clunky traditional bank UX</li>
</ul>

<h3>Brand and Design Direction</h3>
<p>Bold and youthful: deep indigo/purple (#2D1B69), neon mint (#00F5C4), white, soft lavender (#E8E0FF). Phone mockups are central to every section. Trust signals must be visible: RBI logo, partner bank logo, security badges. Feel: trustworthy yet exciting, modern, Gen-Z energy. Think Zepto or CRED aesthetic.</p>

<h3>Required Sections</h3>
<ol>
  <li><strong>Sticky Nav</strong> - Finspark logo, links (Features / How It Works / Security / Download), "Download App" CTA button.</li>
  <li><strong>Hero</strong> - Split layout: left side with headline "Banking That Actually Gets You", 3 bullet benefits, App Store + Play Store download buttons, "4.8 stars on App Store"; right side with phone mockup placeholder.</li>
  <li><strong>Social Proof Strip</strong> - "5L+ Users | 200Cr+ Deposits Managed | RBI Licensed | 4.8 App Store Rating".</li>
  <li><strong>Features Grid</strong> - 6 feature cards: Zero Balance Account, 4% Savings Rate (2x the national average), Smart Budgets (auto-categorise spending), 1-Click Investments (start SIPs from 100), Instant UPI and Payments, Cashback Visa Card (1% on all spends).</li>
  <li><strong>How It Works</strong> - 4 steps with phone screen placeholder per step: Download App, Enter PAN + Aadhaar, Video KYC in 3 mins, Start Banking Immediately.</li>
  <li><strong>Savings Calculator</strong> - Interactive section: "How much could your money grow?" Slider for monthly savings amount (1,000-50,000). Show projected balance at 1 year, 5 years, 10 years at 4% vs 2.7%. This is a JS-driven component.</li>
  <li><strong>Security Section</strong> - "Your Money is Completely Safe" - 4 trust badges: RBI Licensed (via IDFC Bank), DICGC Insured up to 5L, 256-bit Encryption, Biometric Authentication.</li>
  <li><strong>User Reviews</strong> - 5 reviews with profile photo placeholder, name, age, city, and a one-liner.</li>
  <li><strong>App Download Section</strong> - Full-width dark background, phone mockup, headline "Download Finspark. Start in 3 Minutes.", App Store and Play Store badge buttons, QR code placeholder.</li>
  <li><strong>Footer</strong> - Links, "Banking services provided by IDFC First Bank", RBI disclosure text, privacy policy.</li>
</ol>

<h3>CTA Goal</h3>
<p>App download (App Store / Play Store). Every section should reduce the single biggest objection to neobanks: "Is my money actually safe?"</p>

<h3>Design Notes</h3>
<p>Financial products have a trust problem with Gen-Z. Every section should have at least one trust signal. The savings calculator is a key engagement tool - make it visually prominent. The hero must immediately communicate that this is a real, licensed bank.</p>""",
    },
    {
        'title': 'Lumina Wellness - Corporate Wellness Platform B2B Page',
        'tags': 'saas, b2b, wellness, hr-tech, multi-page, advanced',
        'description': """<h3>Difficulty</h3>
<p>Advanced | Multi-Page (Home / For HR Teams, For Employees)</p>
<p><strong>Note:</strong> This is a multi-page project. Use the Pages panel in the builder to create two pages. The Home/HR page is the primary sales page. The "For Employees" page is a secondary, softer page for internal sharing.</p>

<h3>Client Background</h3>
<p>Lumina is a corporate wellness SaaS platform. It combines mental health (therapy sessions with licensed counsellors), physical health (video workout plans), and nutrition (personalised meal plans). Pricing: 299/employee/month. Currently 150+ companies using Lumina. Backed by a Series A (42Cr). Integrates with Slack and Microsoft Teams.</p>

<h3>Target Audience (Page 1 - HR)</h3>
<ul>
  <li>HR Managers, CHROs, and Heads of People at companies with 50-5,000 employees</li>
  <li>B2B buyers who evaluate ROI and have procurement processes</li>
  <li>Care about: attrition reduction, productivity, employee welfare compliance, ease of rollout</li>
</ul>

<h3>Target Audience (Page 2 - Employees)</h3>
<p>Employees of companies evaluating or already using Lumina. The tone is warmer and more personal here.</p>

<h3>Brand and Design Direction</h3>
<p>Clean and professional with warmth: sage green (#4CAF7D), white, deep navy (#0A2540). Corporate yet human - not clinical or pharmaceutical. Data and ROI-driven (HR buyers need numbers). Feel: trustworthy, enterprise-grade, compassionate.</p>

<h3>Page 1: Home (HR-Focused Marketing Page)</h3>
<ol>
  <li><strong>Sticky Nav</strong> - Lumina logo, links (Solutions / Pricing / Case Studies / Resources), "Book a Demo" CTA button.</li>
  <li><strong>Hero</strong> - Headline "Reduce Burnout. Boost Productivity. Retain Your Best People." Sub-copy about on-demand therapy, fitness, and nutrition. Two CTAs: "Book a Free Demo" and "See How It Works". Company logos using Lumina below.</li>
  <li><strong>The Problem</strong> - "Employee burnout is costing you more than you think." Stats: 65% of Indian employees report moderate-to-high burnout, Average cost of replacing one employee: 4.2 lakh, Companies with wellness programmes see 28% lower attrition.</li>
  <li><strong>Solutions Tabs</strong> - 3 tabs: Mental Health, Physical Health, Nutrition. Each tab shows 4 features with icons.</li>
  <li><strong>How It Works for Companies</strong> - 4 steps: Sign Up and Set Budget, Employees Download App, They Book Sessions, You Get Reports.</li>
  <li><strong>ROI Calculator</strong> - Input: number of employees (slider 50-5000). Output: Estimated annual attrition cost saved, estimated sick-day reduction, ROI in months.</li>
  <li><strong>Case Studies</strong> - 2 case studies: "TechCorp (1,200 employees): Reduced attrition by 34% in 12 months." and "RetailChain (3,400 employees): 22% drop in sick leaves, 1.8Cr saved annually."</li>
  <li><strong>Integrations</strong> - "Lumina works with your existing tools." Logos of: Slack, Microsoft Teams, Workday, Darwinbox, GreytHR, Google Workspace, Zoho People.</li>
  <li><strong>Pricing</strong> - 3 tiers: Starter (199/employee/month, up to 100 employees, mental health only), Growth (299/employee/month, all three pillars, up to 500 employees), Enterprise (Custom pricing, 500+ employees, dedicated CSM).</li>
  <li><strong>Trust and Compliance</strong> - Badges: DPDP Act compliant, ISO 27001, HIPAA-aligned, End-to-end encryption, Therapists verified by RCI.</li>
  <li><strong>Final CTA</strong> - Name, Company, Number of Employees (dropdown), "Book a Demo" button. Promise: "Our team will reach out within 4 business hours."</li>
</ol>

<h3>Page 2: For Employees</h3>
<ol>
  <li><strong>Nav</strong> - Consistent but simplified. "Download App" CTA instead of "Book Demo".</li>
  <li><strong>Hero</strong> - Warm tone: "Your Company is Taking Care of You." Sub-copy: "Lumina gives you private, confidential access to therapists, fitness coaches, and nutritionists - fully paid by your employer." CTA: "Download the App".</li>
  <li><strong>What's Included</strong> - 3 feature cards: Therapy, Fitness, Nutrition.</li>
  <li><strong>It's Completely Private</strong> - "Your employer sees only anonymised, aggregated data - never your individual sessions or health records."</li>
  <li><strong>How to Get Started</strong> - 3 steps: Download the Lumina app, Sign up with your work email, Book your first session (free).</li>
  <li><strong>App Screens</strong> - 3-4 phone screen placeholders.</li>
  <li><strong>Footer</strong> - Privacy policy, terms, App Store / Play Store links.</li>
</ol>

<h3>CTA Goal</h3>
<p>Page 1: Demo booking with lead form (company name + headcount). Page 2: App download and sign-up.</p>

<h3>Design Notes</h3>
<p>Page 1 must feel enterprise-grade. Every claim needs a number behind it. The ROI calculator is the most powerful section - make it impossible to miss. Page 2 must feel personal, warm, and low-pressure. Address the "Is it really private?" concern explicitly and prominently.</p>""",
    },
]


class Command(BaseCommand):
    help = 'Load 10 sample design studio projects (beginner to advanced)'

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
            thumbnail = THUMBNAILS.get(data['title'], '')
            existing = DesignProject.objects.filter(title=data['title']).first()

            if existing:
                if options['update']:
                    existing.description = data['description']
                    existing.tags = data['tags']
                    existing.thumbnail_url = thumbnail
                    existing.is_active = True
                    existing.save(update_fields=['description', 'tags', 'thumbnail_url', 'is_active', 'updated_at'])
                    self.stdout.write(f'  Updated : {data["title"]}')
                    updated_count += 1
                else:
                    # Always sync thumbnail even without --update
                    if not existing.thumbnail_url and thumbnail:
                        existing.thumbnail_url = thumbnail
                        existing.save(update_fields=['thumbnail_url'])
                    self.stdout.write(f'  Skipped : {data["title"]} (already exists, use --update to overwrite)')
                    skipped_count += 1
            else:
                DesignProject.objects.create(
                    title=data['title'],
                    description=data['description'],
                    tags=data['tags'],
                    thumbnail_url=thumbnail,
                    is_active=True,
                )
                self.stdout.write(f'  Created : {data["title"]}')
                created_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done - {created_count} created, {updated_count} updated, {skipped_count} skipped.'
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
