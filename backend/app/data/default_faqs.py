"""
Default FAQ dataset for the engineering college knowledge base.
These are ingested into ChromaDB during the initial setup.

Each entry has a question, answer, and category for metadata filtering.
"""

DEFAULT_FAQS = [
    # ==========================================
    # ADMISSION
    # ==========================================
    {
        "question": "What documents are required for admission?",
        "answer": "For admission, you need to submit the following documents: 1) 10th Marksheet (original + 2 photocopies), 2) 12th Marksheet (original + 2 photocopies), 3) Entrance Exam Scorecard (CET/JEE/NEET as applicable), 4) Aadhaar Card, 5) Passport-size photographs (6 copies, white background), 6) Transfer Certificate from previous institution, 7) Migration Certificate (if from another university), 8) Caste/Category Certificate (if applicable — SC/ST/OBC/EWS), 9) Income Certificate (for fee concession/scholarship), 10) Gap Certificate (if applicable).",
        "category": "admission",
    },
    {
        "question": "What is the admission process for engineering?",
        "answer": "The admission process involves the following steps: 1) Apply online through the college admission portal. 2) Pay the application fee. 3) Upload required documents for verification. 4) Attend the document verification session (online or in-person). 5) Confirm your seat by paying the admission fee within the specified deadline. 6) Collect your admission letter and student ID. 7) Complete the onboarding checklist before the orientation day.",
        "category": "admission",
    },
    {
        "question": "What is the last date for admission?",
        "answer": "The admission deadlines vary by category and round. Generally, the first round of admissions closes by mid-July, the second round by early August, and spot admissions continue until September. Please check the official admission calendar on the college website or contact the admission helpdesk for exact dates for the current academic year.",
        "category": "admission",
    },
    {
        "question": "Can I change my branch after admission?",
        "answer": "Yes, branch change is possible after the first year based on the following criteria: 1) You must have completed all first-year courses without any backlogs. 2) Branch change is merit-based — your first-year CGPA will determine eligibility. 3) Availability of seats in the desired branch is required. 4) Applications for branch change open within the first 2 weeks of the second year. Contact the academic office for the exact process and form.",
        "category": "admission",
    },
    {
        "question": "What entrance exams are accepted for admission?",
        "answer": "The college accepts the following entrance exams for engineering admissions: 1) State CET (Common Entrance Test) — primary admission pathway. 2) JEE Main — for students from other states or those who prefer JEE scores. 3) Institute-level entrance exam (if applicable). For management quota seats, the college may have its own criteria. Contact the admissions office for specific cutoff scores and seat availability.",
        "category": "admission",
    },

    # ==========================================
    # FEE
    # ==========================================
    {
        "question": "What is the fee structure for engineering?",
        "answer": "The fee structure depends on your admission category: 1) Merit/Government Quota: Approximately ₹80,000 - ₹1,20,000 per year (varies by state regulation). 2) Management Quota: Approximately ₹1,50,000 - ₹2,50,000 per year. 3) NRI Quota: As per university norms. The fee includes tuition, development, laboratory, library, and examination charges. Hostel fees are separate. Exact amounts are available on the fee payment portal after admission confirmation.",
        "category": "fee",
    },
    {
        "question": "How can I pay the college fee?",
        "answer": "Fees can be paid through the following methods: 1) Online Payment Portal — login to the student portal and use UPI, Net Banking, Debit/Credit Card. 2) Demand Draft — drawn in favor of the college, payable at the local branch. 3) Bank Transfer (NEFT/RTGS) — using the college bank account details provided in the fee receipt. 4) Cash payment at the college fee counter (limited to specific dates). Always keep the payment receipt/transaction ID for reference.",
        "category": "fee",
    },
    {
        "question": "Is there a scholarship available?",
        "answer": "Yes, several scholarships are available: 1) Government Scholarships — for SC/ST/OBC/EWS categories (e.g., Post-Matric Scholarship, Minority Scholarship). 2) Merit Scholarships — for students with high entrance exam ranks or CGPA above 8.5. 3) College-level Financial Aid — for economically weaker students (apply with income certificate). 4) Private/Corporate Scholarships — check the placement cell for industry-sponsored scholarships. Apply through the scholarship portal within the first month of admission.",
        "category": "fee",
    },
    {
        "question": "Can I pay fees in installments?",
        "answer": "Yes, the college offers an installment facility for fee payment. You can split the annual fee into 2 installments: 1) First installment — 60% of the total fee, due at the time of admission. 2) Second installment — remaining 40%, due within 3 months of admission. To avail this, submit a written request to the accounts section along with your admission receipt. Late payment may attract a penalty of ₹50 per day.",
        "category": "fee",
    },
    {
        "question": "What is the hostel fee?",
        "answer": "Hostel fees are separate from tuition fees and typically range from ₹40,000 to ₹80,000 per year depending on the room type: 1) Triple sharing — ₹40,000/year. 2) Double sharing — ₹55,000/year. 3) Single room — ₹75,000/year (limited availability). This includes accommodation, mess charges (basic meal plan), Wi-Fi, and common area maintenance. Additional charges may apply for AC rooms or premium facilities.",
        "category": "fee",
    },

    # ==========================================
    # HOSTEL
    # ==========================================
    {
        "question": "How do I apply for hostel accommodation?",
        "answer": "To apply for hostel accommodation: 1) Login to the student portal after admission confirmation. 2) Navigate to 'Hostel Application' section. 3) Fill in the application form with your room preference and dietary requirements. 4) Upload a passport-size photo and parent's consent letter. 5) Pay the hostel fee through the payment portal. 6) Hostel allotment is on a first-come, first-served basis. You will receive your room number and reporting date via email.",
        "category": "hostel",
    },
    {
        "question": "What are the hostel rules?",
        "answer": "Key hostel rules include: 1) Entry/Exit — Main gate closes at 9:00 PM; late entry requires warden's permission. 2) Visitors — Visitors allowed only in the common area during visiting hours (4-6 PM on weekends). 3) No alcohol, smoking, or prohibited substances on campus. 4) Noise — Maintain silence after 10:00 PM. 5) Mess — Meal timings are fixed (Breakfast: 7-9 AM, Lunch: 12-2 PM, Dinner: 7-9 PM). 6) Ragging is strictly prohibited — zero tolerance policy. 7) Room changes require warden approval.",
        "category": "hostel",
    },
    {
        "question": "What facilities are available in the hostel?",
        "answer": "Hostel facilities include: 1) Furnished rooms with bed, study table, chair, and wardrobe. 2) 24/7 Wi-Fi connectivity. 3) Common study room and reading hall. 4) Mess/Dining hall with vegetarian and non-vegetarian meal options. 5) Indoor recreation room (TT table, carrom, TV). 6) Laundry service (paid). 7) 24/7 security and CCTV surveillance. 8) Hot water (limited hours: 6-8 AM). 9) Parking area for two-wheelers. 10) First-aid and on-campus medical facility.",
        "category": "hostel",
    },
    {
        "question": "Can I get a hostel room change?",
        "answer": "Room changes are possible under certain circumstances: 1) Submit a written request to the hostel warden with a valid reason. 2) Room changes are processed at the beginning of each semester (not mid-semester). 3) Medical reasons or safety concerns are given priority. 4) Mutual exchange between two willing students is the easiest option — both must submit a joint request. The hostel office typically processes requests within 1 week of the semester start.",
        "category": "hostel",
    },

    # ==========================================
    # ACADEMIC
    # ==========================================
    {
        "question": "What is the academic calendar?",
        "answer": "The typical academic calendar follows: 1) Odd Semester (July - December): Classes start in the first week of August, mid-semester exams in October, end-semester exams in December. 2) Even Semester (January - June): Classes start in the second week of January, mid-semester exams in March, end-semester exams in May/June. 3) Summer break: June-July. 4) Winter break: Last week of December - first week of January. Detailed academic calendar is published on the college website before each semester.",
        "category": "academic",
    },
    {
        "question": "What is the attendance requirement?",
        "answer": "The minimum attendance requirement is 75% in each subject. Consequences of low attendance: 1) Below 75% — you may be detained from appearing in end-semester exams. 2) Below 65% — you will be issued a warning letter, and parents will be notified. 3) Medical leave can be counted if supported by a valid medical certificate submitted within 3 days. 4) On-Duty (OD) for college events/fests can compensate up to 5% if approved by the HOD. Track your attendance regularly through the LMS portal.",
        "category": "academic",
    },
    {
        "question": "How does the grading system work?",
        "answer": "The college follows a relative grading system based on CGPA (Cumulative Grade Point Average) on a 10-point scale: O (Outstanding) = 10, A+ = 9, A = 8, B+ = 7, B = 6, C = 5, P (Pass) = 4, F (Fail) = 0. Your SGPA (Semester GPA) is calculated each semester, and your CGPA is the weighted average across all semesters. You need a minimum CGPA of 4.0 to graduate. Grades are based on continuous evaluation (internal marks: 40%) and end-semester exam (60%).",
        "category": "academic",
    },
    {
        "question": "How can I register for elective courses?",
        "answer": "Elective course registration process: 1) The list of available electives is published on the LMS portal 2 weeks before the semester starts. 2) Login to the student portal → Academic → Elective Registration. 3) Select your preferred electives (usually 1-2 per semester starting from 3rd year). 4) Electives are allotted on a first-come-first-served basis with limited seats per course. 5) Registration window is open for 1 week. 6) If your preferred elective is full, you will be assigned your second choice.",
        "category": "academic",
    },

    # ==========================================
    # LMS (Learning Management System)
    # ==========================================
    {
        "question": "How do I access the LMS portal?",
        "answer": "To access the Learning Management System: 1) Go to the LMS URL provided during orientation (typically lms.collegename.ac.in). 2) Your login credentials are: Username = your admission number/enrollment ID, Password = your date of birth (DDMMYYYY) for first login. 3) You MUST change your password on first login. 4) The LMS is accessible on both desktop and mobile browsers. 5) If you face login issues, contact the IT helpdesk at it-support@college.ac.in or visit the computer center in Room B-201.",
        "category": "lms",
    },
    {
        "question": "What can I do on the LMS portal?",
        "answer": "The LMS portal provides the following features: 1) View course materials — lecture notes, slides, and reference PDFs uploaded by faculty. 2) Submit assignments — upload your assignment files before the deadline. 3) View grades and attendance — check your marks and attendance percentage. 4) Discussion forums — participate in course-specific discussions. 5) Notifications — receive announcements from faculty and administration. 6) Timetable — view your weekly class schedule. 7) Exam schedule — check upcoming exam dates and seating arrangements.",
        "category": "lms",
    },
    {
        "question": "I forgot my LMS password. How do I reset it?",
        "answer": "To reset your LMS password: 1) Go to the LMS login page and click 'Forgot Password'. 2) Enter your registered email (college email ID). 3) You will receive a password reset link via email within 5 minutes. 4) If you don't receive the email, check your spam folder. 5) If the reset link doesn't work, visit the IT helpdesk in the computer center (Room B-201) with your student ID card for manual reset. 6) Support hours: Monday-Friday, 9 AM - 5 PM.",
        "category": "lms",
    },

    # ==========================================
    # EXAM
    # ==========================================
    {
        "question": "What is the exam pattern?",
        "answer": "The examination pattern includes: 1) Internal Assessment (40% weightage) — 2 class tests, assignments, and lab work evaluated throughout the semester. 2) End Semester Exam (60% weightage) — 3-hour written exam covering the full syllabus. 3) Practical/Lab exams are conducted separately with internal + external examiner. 4) You need a minimum of 40% in both internal and external components separately to pass a subject. 5) Exam seating arrangement is published 2 days before on the notice board and LMS.",
        "category": "exam",
    },
    {
        "question": "What happens if I fail a subject?",
        "answer": "If you fail a subject: 1) You can appear for a supplementary (backlog) exam in the next semester's exam cycle. 2) You can carry up to 4 backlogs and still be promoted to the next year. 3) More than 4 backlogs may result in a year-back (repeating the year). 4) Supplementary exam fee is ₹500 per subject. 5) There is no limit on the number of attempts, but all backlogs must be cleared before the final year to be eligible for graduation. 6) Apply for supplementary exams through the exam section.",
        "category": "exam",
    },

    # ==========================================
    # PLACEMENT
    # ==========================================
    {
        "question": "How does campus placement work?",
        "answer": "Campus placement process: 1) Placement season typically runs from August to March of the final year. 2) Register on the placement portal with your updated resume by July. 3) Companies visit campus for pre-placement talks, followed by online tests, group discussions, and interviews. 4) Eligibility: Minimum 60% (6.0 CGPA) with no active backlogs. 5) Once placed, you cannot appear for other companies (one-offer policy). 6) The placement cell also organizes resume workshops, mock interviews, and aptitude training from the 3rd year. 7) Average placement package ranges from ₹4-8 LPA depending on the branch.",
        "category": "placement",
    },
    {
        "question": "When should I start preparing for placements?",
        "answer": "Ideally, start preparing from the 2nd year: 1) 2nd Year — Focus on DSA (Data Structures & Algorithms) and one programming language (C++/Java/Python). Practice on LeetCode/HackerRank. 2) 3rd Year — Build projects, learn frameworks, contribute to open source. Participate in hackathons. 3) Pre-placement (July of final year) — Polish your resume, practice aptitude tests, and attend mock interviews organized by the placement cell. 4) The placement cell conducts a 3-month training program from May-July covering aptitude, coding, and soft skills.",
        "category": "placement",
    },

    # ==========================================
    # GENERAL
    # ==========================================
    {
        "question": "Where is the college located?",
        "answer": "The college is located in the main campus. For exact address and directions, please refer to the college website or Google Maps. The campus is well-connected by public transport. Nearest bus stop is at the main gate, and the nearest railway station is approximately 2-3 km from campus. Auto-rickshaws and ride-sharing services are readily available.",
        "category": "general",
    },
    {
        "question": "Who should I contact for help?",
        "answer": "Contact information for different departments: 1) Admission queries — admission@college.ac.in or call the admission helpdesk. 2) Fee-related — accounts@college.ac.in or visit the accounts section. 3) Hostel issues — Report to your floor warden or email hostel@college.ac.in. 4) Academic queries — Contact your class coordinator or HOD. 5) IT/LMS support — it-support@college.ac.in or computer center (Room B-201). 6) General helpdesk — Visit the main office or call the college reception. 7) For emergency — Campus security: available 24/7.",
        "category": "general",
    },
    {
        "question": "What extracurricular activities are available?",
        "answer": "The college offers a wide range of extracurricular activities: 1) Technical clubs — Coding Club, Robotics Club, AI/ML Club, Cybersecurity Club. 2) Cultural clubs — Music, Dance, Drama, Photography, Art. 3) Sports — Cricket, Football, Basketball, Badminton, Table Tennis, Athletics (with dedicated sports grounds). 4) Annual fest — Technical fest (TechFest) in February and Cultural fest in March. 5) NSS/NCC — For community service and discipline training. 6) Entrepreneurship Cell — For startup enthusiasts. Club registrations open during the first month of each academic year.",
        "category": "general",
    },
    {
        "question": "What is the college timings?",
        "answer": "College timings: 1) Regular classes: 9:00 AM to 4:30 PM (Monday to Friday). 2) Saturday: 9:00 AM to 1:00 PM (only for labs/tutorials/extra classes). 3) Library: 8:00 AM to 8:00 PM (Monday to Saturday). 4) Computer labs: 9:00 AM to 6:00 PM. 5) Sports grounds: 6:00 AM to 8:00 AM and 4:30 PM to 7:00 PM. 6) Administrative offices: 10:00 AM to 5:00 PM (Monday to Friday). 7) Canteen: 8:00 AM to 7:00 PM.",
        "category": "general",
    },
    {
        "question": "Is there a dress code?",
        "answer": "The college has a semi-formal dress code: 1) Regular days — Formal or semi-formal attire. Jeans with collared shirts/t-shirts are acceptable. 2) Shorts, sleeveless tops, and slippers are not allowed in classrooms or labs. 3) Lab sessions — Closed-toe shoes are mandatory for safety. 4) Sports — Proper sportswear during sports activities. 5) ID card must be worn visibly at all times on campus. 6) On special occasions (fests, cultural events), casual/ethnic wear is permitted. The dress code is enforced by class coordinators.",
        "category": "general",
    },
]
