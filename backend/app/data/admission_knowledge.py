"""
Comprehensive Engineering College Admission Knowledge Base.
Covers CET, JEE, CAP rounds, spot rounds, counseling, eligibility,
documents, fees, scholarships, hostel, academics, placements,
mentor system, and college workflows.

Each entry has question, answer, and category for ChromaDB ingestion.
"""

ADMISSION_KNOWLEDGE_BASE = [
    # ==========================================
    # CET ADMISSION PROCESS
    # ==========================================
    {
        "question": "How does CET admission work?",
        "answer": "CET (Common Entrance Test) admission process: 1) Register for the state CET exam conducted by the competent authority between January-March. 2) CET score determines your merit rank. 3) Participate in CAP (Centralized Admission Process) rounds held in June-July. 4) Fill in your branch and college preferences online. 5) Based on your rank and preferences, you'll be allotted a seat. 6) Confirm your seat by reporting to the allotted college with original documents within the deadline. 7) CET admissions typically cover 60-70% of total seats in government and government-aided engineering colleges.",
        "category": "admission",
    },
    {
        "question": "When is the CET exam conducted?",
        "answer": "CET exam schedule: 1) Application forms released: January-February. 2) Last date to apply: March. 3) Exam date: Typically April-May. 4) Result declaration: May-June. 5) CAP rounds: June-July. 6) College reporting: July-August. The exact dates vary each year. Check the official CET website for the current year's schedule. Late applications are generally not accepted, so apply before the deadline.",
        "category": "admission",
    },
    {
        "question": "What is the CET exam pattern?",
        "answer": "CET exam pattern: 1) Total marks: 200 (Physics 70, Chemistry 70, Mathematics 60). 2) Duration: 3 hours. 3) Question type: Multiple Choice Questions (MCQs). 4) Marking scheme: +1 for each correct answer, no negative marking. 5) The syllabus is based on the state board 12th standard curriculum (Physics, Chemistry, Mathematics). 6) Some states also offer Biology as an option for pharmacy/agriculture courses. 7) The exam is conducted online (computer-based test) at designated centers across the state.",
        "category": "admission",
    },
    {
        "question": "How is the CET merit list prepared?",
        "answer": "CET merit list preparation: 1) The merit list is based on your percentile score in CET. 2) Tie-breaking: if two students have the same score, the elder student gets priority, then higher marks in 12th Mathematics, then Physics, then Chemistry. 3) Separate merit lists are prepared for each category (General, OBC, SC, ST, EWS). 4) The merit list is published on the official CET portal. 5) You can check your rank using your application number and date of birth. 6) The final merit list is used for all CAP rounds.",
        "category": "admission",
    },
    {
        "question": "What is CET cutoff score for engineering?",
        "answer": "CET cutoff scores vary yearly by: 1) Number of applicants. 2) Exam difficulty. 3) Category (General/OBC/SC/ST/EWS). 4) Branch popularity (CS has highest cutoff). 5) College reputation. Typical ranges: Top colleges CS/IT: 95-99 percentile. Mid colleges core branches: 80-95 percentile. Lower cutoff: 50-80 percentile. Category-wise relaxation applies as per government norms. Previous year cutoffs are available on the CET website for reference.",
        "category": "admission",
    },
    {
        "question": "How many attempts are allowed for CET?",
        "answer": "CET attempt rules: 1) CET is conducted once per year. 2) There is no limit on the number of attempts — you can appear every year. 3) However, for engineering admission, your latest CET score is considered. 4) If you appear in multiple years, the best score among valid attempts may be considered (check state policy). 5) CET score is valid for 1 academic year only — you must take admission in the same year. 6) Droppers and repeaters can appear for CET without any penalty.",
        "category": "admission",
    },
    {
        "question": "Can I get admission without CET score?",
        "answer": "Admission without CET score: 1) Management quota seats don't require CET — admission based on 12th marks. 2) Some private colleges accept JEE Main scores directly. 3) NRI quota has separate criteria. 4) Diploma holders can get lateral entry (direct 2nd year). 5) Institute-level entrance exams may be accepted. 6) However, management quota fees are higher (1.5-2.5x government quota). 7) Eligibility: minimum 45% in PCM (40% for reserved categories) in 12th is still required.",
        "category": "admission",
    },

    # ==========================================
    # JEE ADMISSION
    # ==========================================
    {
        "question": "Can I take admission through JEE Main score?",
        "answer": "Yes, JEE Main scores are accepted: 1) JEE Main is the national-level engineering entrance exam by NTA. 2) State CET authorities may accept JEE Main for 5-10% supernumerary quota seats. 3) Some private and autonomous colleges accept JEE Main scores directly. 4) JEE Advanced is only for IIT admissions. 5) For state colleges, JEE Main provides an alternative to CET. 6) You need to participate in separate counseling if using JEE scores. 7) JEE Main is conducted twice a year (January and April). 8) Best of the two attempts is considered for ranking.",
        "category": "admission",
    },
    {
        "question": "What is the difference between CET and JEE?",
        "answer": "Key differences: 1) CET is state-level, JEE Main is national. 2) CET follows state board 12th syllabus, JEE follows CBSE/NCERT. 3) CET is generally easier than JEE Main. 4) CET scores valid only within the state, JEE Main scores accepted nationally. 5) CET uses CAP rounds, JEE uses JoSAA/CSAB counseling. 6) Many students appear for both exams. 7) CET focuses on state board curriculum, JEE tests deeper conceptual understanding. 8) JEE Main is required for NITs, IIITs, and GFTIs; CET is for state engineering colleges.",
        "category": "admission",
    },
    {
        "question": "What is JoSAA counseling?",
        "answer": "JoSAA (Joint Seat Allocation Authority) counseling: 1) Centralized counseling for NITs, IIITs, GFTIs based on JEE Main rank. 2) Separate counseling for IITs based on JEE Advanced rank. 3) Multiple rounds of seat allocation based on preferences and merit. 4) You must register online, fill preferences, and freeze/float choices. 5) Seat acceptance requires fee payment and document upload. 6) Reporting to allotted institute for final verification. 7) JoSAA usually has 6-7 rounds in June-July.",
        "category": "admission",
    },
    {
        "question": "What is CSAB counseling?",
        "answer": "CSAB (Central Seat Allocation Board) counseling: 1) Conducted after JoSAA rounds for remaining vacant seats. 2) For NITs, IIITs, and GFTIs that still have vacancies. 3) Separate registration and choice filling. 4) Usually 1-2 special rounds in July-August. 5) Eligibility: Candidates who participated in JoSAA but didn't get a seat. 6) CSAB also conducts special rounds for SC/ST candidates under the central seat reservation.",
        "category": "admission",
    },
    {
        "question": "What is JEE Main cutoff for NITs?",
        "answer": "JEE Main cutoff for NITs varies by: 1) NIT ranking (Top NITs: Trichy, Surathkal, Warangal, Calicut have highest cutoffs). 2) Branch (CSE/IT highest, then ECE, then core branches). 3) Category (General/OBC/SC/ST/EWS). 4) Home state quota vs other state quota. Typical ranges: Top NIT CSE: 98-99.9 percentile. Mid NIT CSE: 95-98 percentile. Core branches top NITs: 90-95 percentile. Lower NITs: 80-90 percentile.",
        "category": "admission",
    },

    # ==========================================
    # CAP ROUNDS
    # ==========================================
    {
        "question": "What are CAP rounds in admission?",
        "answer": "CAP (Centralized Admission Process) rounds: 1) Typically 3-4 rounds conducted after CET results. 2) Round 1: Initial seat allotment based on merit and preferences. 3) Round 2: Upgradation — if you get a better option, you're automatically upgraded. 4) Round 3: Final round for remaining seats. 5) After CAP, spot rounds fill vacant seats. 6) You must report with original documents within the deadline to confirm your seat. 7) Failure to report results in seat forfeiture. 8) Each round has a specific schedule published on the admission portal.",
        "category": "admission",
    },
    {
        "question": "How do I fill CAP preferences?",
        "answer": "CAP preference filling: 1) Login to the CAP portal after merit list publication. 2) You can select up to 300+ college and branch combinations. 3) Order matters — your top preference should be first. 4) You can edit preferences multiple times before the deadline. 5) Use the 'Mock Allotment' feature to see likely outcomes before final submission. 6) Consult previous year cutoffs and college rankings. 7) Include backup options (lower preference colleges) in case you don't get a top choice. 8) Once submitted, preferences cannot be changed after the deadline.",
        "category": "admission",
    },
    {
        "question": "Can I change my CAP preferences after submission?",
        "answer": "Yes, you can edit CAP preferences multiple times before the final deadline: 1) Login to CAP portal and go to 'Edit Preferences'. 2) Reorder, add, or remove college-branch combinations. 3) Save after each change — unsaved changes are lost. 4) Preferences can be edited unlimited times before the deadline. 5) The last saved version is considered for seat allotment. 6) After the deadline, preferences are frozen and cannot be changed. 7) Use the mock allotment feature to see how different preference orders affect your chances.",
        "category": "admission",
    },
    {
        "question": "What happens if I don't get a seat in CAP round 1?",
        "answer": "If you don't get a seat in Round 1: 1) You are automatically considered for subsequent rounds — no need to reapply. 2) Round 2 and 3 allocate seats based on remaining vacancies. 3) You can modify your preferences between rounds based on available seats. 4) If seats become available in your preferred choices due to others vacating, you may get upgraded. 5) After all CAP rounds, spot rounds are conducted for remaining vacancies. 6) You can also try for management quota if you still don't get a seat. 7) Document verification is only needed after you accept a seat.",
        "category": "admission",
    },
    {
        "question": "How do I freeze or float my CAP seat?",
        "answer": "After each CAP round, you have options: 1) FREEZE: Accept the allotted seat and exit the process — no further rounds. 2) FLOAT: Keep the allotted seat as backup but continue for better options in later rounds. 3) SLIDE: Accept the seat but only consider upgradation within the same college (different branch). 4) If you FLOAT and get a better option, you are automatically upgraded. 5) If you FLOAT and don't get upgraded, you keep the original seat. 6) Failure to select any option by the deadline = seat forfeited. 7) Once FREEZED, you cannot participate in further rounds.",
        "category": "admission",
    },
    {
        "question": "What documents are needed for CAP round reporting?",
        "answer": "Documents required for CAP round reporting: 1) CAP allotment letter (downloaded from portal). 2) CET/Entrance exam scorecard. 3) 10th marksheet and passing certificate. 4) 12th marksheet and passing certificate. 5) Domicile certificate (for state quota). 6) Category certificate (SC/ST/OBC/EWS) if applicable. 7) Non-Creamy Layer certificate for OBC. 8) Income certificate (if claiming fee concession). 9) School leaving certificate/Transfer certificate. 10) Migration certificate (if from another board). 11) Gap certificate (if applicable). 12) 6 passport-size photographs. 13) Aadhaar card. 14) Anti-ragging affidavit. Keep 2-3 sets of self-attested photocopies of ALL documents.",
        "category": "admission",
    },

    # ==========================================
    # SPOT ROUNDS
    # ==========================================
    {
        "question": "What are spot rounds in engineering admission?",
        "answer": "Spot rounds are conducted after all CAP rounds are complete: 1) Purpose: Fill remaining vacant seats in colleges. 2) Usually 1-2 spot rounds in August-September. 3) Eligibility: Students who participated in CAP but didn't get a seat, or didn't confirm their seat. 4) Spot rounds are faster — allotment happens within 1-2 days. 5) You may need to visit the college in person for spot round admission. 6) Document verification is done on the spot. 7) Spot rounds are first-come-first-served in some cases. 8) Fee payment is immediate upon allotment. 9) Spot round seats are typically from cancellations or unfilled quota.",
        "category": "admission",
    },
    {
        "question": "How is spot round different from CAP?",
        "answer": "Key differences between CAP and spot rounds: 1) CAP rounds are online and centralized; spot rounds may be conducted at the college level. 2) CAP has 3-4 scheduled rounds; spot rounds are fewer and faster. 3) CAP allows float/slide options; spot rounds are usually final — no further changes. 4) CAP seats include government quota; spot rounds are mostly management quota or unfilled seats. 5) In spot rounds, you may need to be physically present at the college. 6) CAP cutoffs are higher; spot round cutoffs may be lower. 7) CAP follows strict merit order; spot rounds may use first-come-first-served for some seats.",
        "category": "admission",
    },
    {
        "question": "What is the last date to get admission through spot round?",
        "answer": "Spot round deadlines: 1) Usually conducted in August-September before the academic year starts. 2) The final cutoff date is typically September 30th as per AICTE guidelines. 3) Some colleges may extend spot admissions to October for very few vacant seats. 4) After the AICTE deadline, no new admissions are permitted for that academic year. 5) Spot rounds are announced on the college website and admission portal. 6) Late fee may apply for admissions after the regular deadline. 7) It is advisable to complete admission before September 15th to avoid last-minute issues.",
        "category": "admission",
    },

    # ==========================================
    # COUNSELING PROCESS
    # ==========================================
    {
        "question": "How does the counseling process work after CET results?",
        "answer": "CET counseling process step by step: 1) CET results announced (May-June). 2) Merit list published based on percentile scores. 3) Online registration for CAP rounds on the official portal. 4) Fill college and branch preferences (up to 300+ combinations). 5) Lock preferences before the deadline. 6) Mock allotment released for reference — you can adjust preferences based on this. 7) CAP Round 1: Seat allotment — check result on portal. 8) Float/Slide/Freeze your seat after Round 1. 9) CAP Round 2: Upgradation if better option available. 10) CAP Round 3: Final round for remaining seats. 11) Report to allotted college with original documents for verification. 12) Pay fees and confirm admission. 13) Spot rounds after CAP for any remaining vacant seats.",
        "category": "admission",
    },
    {
        "question": "What is the fee for CAP counseling registration?",
        "answer": "CAP counseling registration fee: 1) General category: Approximately ₹800-1500 depending on the state. 2) OBC category: Approximately ₹600-1200. 3) SC/ST category: Approximately ₹400-800 (often reduced or waived). 4) The fee is non-refundable. 5) Payment is online through the CAP portal (Net Banking, UPI, Card). 6) The registration fee is separate from college admission fees. 7) Keep the payment receipt for future reference.",
        "category": "admission",
    },
    {
        "question": "Can I change my category during counseling?",
        "answer": "Category change during counseling: 1) Category claimed during CET application and registration is considered final. 2) You cannot change your category during CAP counseling. 3) If you made a mistake, you must contact the CET cell with supporting documents. 4) Category changes are only allowed before the merit list is published. 5) After merit list publication, category is frozen for that admission cycle. 6) Submitting false category claims = immediate disqualification and legal action. 7) Always submit valid category certificates at the time of CET registration itself.",
        "category": "admission",
    },

    # ==========================================
    # ELIGIBILITY
    # ==========================================
    {
        "question": "What is the minimum percentage required for engineering admission?",
        "answer": "Minimum eligibility for engineering: 1) CET quota: Minimum 45% aggregate in PCM in 12th (40% for reserved categories). 2) Management quota: Same minimum but more flexibility. 3) Must have passed 12th with Physics, Chemistry, and Mathematics as core subjects. 4) Diploma holders can get lateral entry to 2nd year with minimum 60% in diploma. 5) For JEE-based admissions: Minimum 75% in 12th (65% for SC/ST) or top 20 percentile in respective board. 6) International students need equivalency from AIU. 7) Some colleges also accept students from other state boards if they meet the eligibility. 8) Aggregate is calculated as average of PCM marks, not overall percentage.",
        "category": "admission",
    },
    {
        "question": "What are the PCM requirements for engineering?",
        "answer": "PCM (Physics, Chemistry, Mathematics) requirements: 1) All three must be compulsory subjects in 12th. 2) You need to pass each individually (minimum passing marks in theory + practical combined). 3) Aggregate of PCM marks should be minimum 45% for general (40% for reserved). 4) Some colleges also consider the overall 12th percentage, but PCM aggregate is mandatory. 5) If you studied Biology instead of Mathematics in 12th, you are not eligible for B.E./B.Tech. 6) Candidates with vocational subjects instead of PCM are generally not eligible. 7) Mathematics is mandatory — without it, engineering admission is not possible.",
        "category": "admission",
    },
    {
        "question": "What is the eligibility for SC/ST students?",
        "answer": "SC/ST eligibility: 1) Minimum 40% aggregate in PCM in 12th (relaxation of 5% from general category). 2) Caste certificate issued by competent authority is mandatory for claiming reservation. 3) SC candidates get approximately 13% reservation, ST candidates get 7%. 4) No upper age limit for SC/ST candidates. 5) Fee concession and scholarships are available through post-matric scholarship scheme. 6) SC/ST students also get relaxation in CET/JEE cutoff scores. 7) The caste certificate should be in the student's name and issued by SDM/Tehsildar. 8) SC/ST students from other states are eligible for central quota but not state quota.",
        "category": "admission",
    },
    {
        "question": "What is the eligibility for OBC students?",
        "answer": "OBC eligibility: 1) Minimum 40% aggregate in PCM in 12th. 2) OBC Non-Creamy Layer (NCL) certificate is mandatory for reservation benefits. 3) The NCL certificate must be renewed annually (income below ₹8 lakh per year). 4) OBC reservation is typically 19% in state engineering colleges. 5) OBC candidates from creamy layer can still apply under general category. 6) The OBC certificate should be issued within the last 1 year for admission purposes. 7) OBC-NCL certificate is different from OBC certificate — make sure you have the correct one. 8) The certificate should clearly mention the caste and that it belongs to the central/state OBC list.",
        "category": "admission",
    },
    {
        "question": "What is the eligibility for EWS students?",
        "answer": "EWS (Economically Weaker Section) eligibility: 1) Minimum 45% in PCM in 12th (same as general). 2) Family income should be below ₹8 lakh per annum. 3) EWS certificate issued by competent authority (Tehsildar/District Magistrate). 4) 10% reservation in engineering colleges. 5) EWS benefits are for candidates not covered under SC/ST/OBC reservation. 6) Family should not own more than specified assets: 5 acres agricultural land, 1000 sq ft residential plot, or 2000 sq ft residential property. 7) EWS certificate valid for 1 year from date of issue. 8) Income includes all sources: salary, business, agriculture, and other earnings.",
        "category": "admission",
    },
    {
        "question": "What is lateral entry in engineering?",
        "answer": "Lateral entry allows diploma holders to join B.E./B.Tech directly in the 2nd year (3rd semester): 1) Eligibility: Minimum 60% in 3-year engineering diploma from a recognized board. 2) Admission through lateral entry CET or direct merit. 3) You skip the 1st year and join directly in 2nd year. 4) Total duration is 3 years instead of 4. 5) Available for all engineering branches (subject to seat availability). 6) Lateral entry students have separate merit list and quota (approximately 10-20% of total seats). 7) Diploma should be in the same or related branch as the BE/BTech program. 8) Lateral entry students are not eligible for TFWS or certain scholarships meant for first-year entries.",
        "category": "admission",
    },
    {
        "question": "Can I get engineering admission after 12th commerce?",
        "answer": "No, engineering admission requires 12th with PCM (Physics, Chemistry, Mathematics). Commerce students without PCM are not eligible. However: 1) You can appear for 12th supplementary exams in PCM subjects as a private candidate (NIOS board allows this). 2) You can pursue a 3-year diploma in engineering after 10th (without 12th) and then lateral entry to B.E. 3) Alternative: BCA/B.Sc. in Computer Science/IT if you have Mathematics in 12th. 4) Some universities offer B.Sc. in emerging technologies (Data Science, AI, ML) that accept commerce backgrounds with Mathematics. 5) BBA or BMS are good alternatives for commerce students interested in management roles in tech companies.",
        "category": "admission",
    },
    {
        "question": "What is the age limit for engineering admission?",
        "answer": "Age limit for engineering: 1) CET: No upper age limit as per Supreme Court directives. 2) JEE Main: No age limit for appearing. 3) Management quota: No age limit. 4) Lateral entry: No age limit. 5) However, for scholarships and certain reserved categories, age may be a factor. 6) For NRI quota, some colleges may have age guidelines but generally no strict limit. 7) Diploma courses (after 10th) typically require minimum 15 years of age. 8) There is no maximum age for higher education as per UGC/AICTE regulations.",
        "category": "admission",
    },
    {
        "question": "Can a student from CBSE/ICSE board apply for state CET?",
        "answer": "Yes, absolutely: 1) CET is open to all state board, CBSE, ICSE, and other recognized board students. 2) The CET syllabus is based on the state board 12th curriculum but covers common PCM topics. 3) CBSE/ICSE students should cross-check the CET syllabus as it may differ slightly from NCERT. 4) Domicile requirement: You typically need state domicile to claim state quota seats through CET. 5) CBSE/ICSE students without state domicile can still apply for management quota. 6) Most state CET authorities publish a syllabus comparison for different boards. 7) If you moved to the state mid-education, check the domicile eligibility criteria carefully.",
        "category": "admission",
    },

    # ==========================================
    # DOCUMENTS
    # ==========================================
    {
        "question": "What documents are required for engineering admission?",
        "answer": "Complete document checklist for engineering admission:\n\nMandatory Documents:\n1) 10th Marksheet and Passing Certificate (original + 2 photocopies)\n2) 12th Marksheet and Passing Certificate (original + 2 photocopies)\n3) CET or JEE Scorecard (if applicable)\n4) Domicile Certificate (proof of state residency)\n5) Aadhaar Card\n6) Passport-size photographs (6 copies, white background)\n7) School Leaving Certificate / Transfer Certificate (TC)\n8) Migration Certificate (if from different board/university)\n\nCategory-Specific Documents:\n9) Category Certificate (SC/ST/OBC/EWS if applicable)\n10) Non-Creamy Layer Certificate for OBC (updated within 1 year)\n11) Income Certificate (for fee concession/scholarship)\n12) Gap Certificate (if there is an academic gap of 1+ year, on stamp paper)\n13) Physical fitness certificate from government doctor\n14) Anti-ragging affidavit (affirmed before notary)\n\nKeep 3 sets of self-attested photocopies of each document for physical verification.",
        "category": "admission",
    },
    {
        "question": "What is a domicile certificate and how do I get it?",
        "answer": "Domicile certificate proves state residency: 1) Issued by the state revenue department (Tehsildar/District Collector). 2) Required for claiming state quota seats in engineering colleges. 3) Minimum residency period: typically 5-15 years in the state (varies by state). 4) Documents needed: Proof of residence (ration card, voter ID, electricity bill), birth certificate, school leaving certificate showing years of education in the state. 5) Children of central government employees transferred to the state may also qualify after 1-3 years. 6) The certificate is usually valid for lifetime. 7) Apply at your nearest SDM/Tehsildar office or online through the state e-district portal. 8) Processing time: 15-30 days, so apply well before the admission process starts.",
        "category": "admission",
    },
    {
        "question": "How do I get an income certificate?",
        "answer": "Income certificate process: 1) Issued by Tehsildar or SDM office. 2) Required for fee concession, EWS quota, scholarship eligibility. 3) Documents needed: Income proof of parents (salary slips, IT returns, Form 16, bank statements, or affidavit if self-employed). 4) Family income includes income of parents/guardians from all sources. 5) EWS income threshold: Below ₹8 lakh per annum. 6) Certificate valid for 1 year from issue date. 7) Apply online through the state e-seva portal or visit the Tehsildar office. 8) Renew annually for continuous scholarship/fee concession benefits.",
        "category": "admission",
    },
    {
        "question": "What is a caste/category certificate?",
        "answer": "Category certificate for reservation: 1) SC/ST certificate issued by Sub-Divisional Magistrate (SDM) or Tehsildar. 2) OBC certificate issued by Tehsildar with non-creamy layer clause. 3) EWS certificate issued by SDM/Tehsildar (valid for 1 year). 4) Certificates must be in the prescribed government format. 5) The certificate should be in the student's name (not parent's). 6) For SC/ST, the caste should be listed in the state's scheduled caste/tribe list. 7) Submit original certificate during document verification along with 2-3 self-attested copies. 8) The certificate must have been issued within the validity period (usually 1 year).",
        "category": "admission",
    },
    {
        "question": "What is a non-creamy layer certificate?",
        "answer": "Non-Creamy Layer (NCL) certificate for OBC students: 1) Proves that the OBC student's family income is below ₹8 lakh per annum. 2) Required to claim OBC reservation benefits in admissions and jobs. 3) Issued by Tehsildar or SDM. 4) Valid for 1 year from date of issue — must be renewed annually. 5) Also considers assets: children of government servants in Group A/Class I positions are considered creamy layer regardless of income. 6) If either parent is a Group A officer, the candidate is creamy layer and cannot claim OBC reservation. 7) Without NCL certificate, OBC candidates are treated as General category. 8) The certificate format is specified by the central/state government and must be strictly followed.",
        "category": "admission",
    },
    {
        "question": "What is a transfer certificate and migration certificate?",
        "answer": "Transfer Certificate (TC): 1) Issued by the school/college you last attended. 2) Confirms that you left the institution after completing studies. 3) Required for admission to a new institution. 4) Contains details of your conduct and academic performance. 5) Applied for at the school office after 12th results.\n\nMigration Certificate: 1) Issued by the board/university when moving from one board/university to another. 2) Required if your 12th is from a different board than the college's university. 3) Obtained from the respective board office after 12th results. 4) Usually takes 1-2 weeks to process. 5) Both documents are essential for the document verification process during admission.\n\nNote: If you lost your TC/Migration certificate, you can get a duplicate from your school/board by paying a nominal fee.",
        "category": "admission",
    },
    {
        "question": "What is a gap certificate and when is it needed?",
        "answer": "Gap certificate is needed if there is an academic gap of 1 year or more: 1) Declares that you were not enrolled in any academic institution during the gap period. 2) Required when the gap between 12th and engineering admission is more than 1 year. 3) Prepared on stamp paper (₹100-500 depending on state). 4) Should include: period of gap, reason for gap (medical, preparation, family issues, etc.), declaration of no other academic enrollment. 5) Attested by a notary public. 6) If gap was due to employment, provide a work experience certificate. 7) The format is usually available on the college website or admission portal. 8) Some colleges may not require gap certificate for gaps less than 1 year.",
        "category": "admission",
    },
    {
        "question": "What documents are needed for hostel admission?",
        "answer": "Hostel admission documents: 1) Hostel application form (filled online on student portal). 2) Admission confirmation letter from the college. 3) Aadhaar Card and address proof. 4) Passport-size photographs (4 copies). 5) Parent/Guardian consent letter (on stamp paper if required by the hostel). 6) Medical fitness certificate from a registered medical practitioner. 7) Anti-ragging affidavit (affirmed before notary — format available on portal). 8) Undertaking for following hostel rules (signed by parent and student). 9) Hostel fee payment receipt. 10) Original documents for verification at the time of check-in. 11) COVID-19 vaccination certificate (recommended). 12) Local guardian declaration (if applicable for out-of-state students).",
        "category": "hostel",
    },
    {
        "question": "What is the document verification process during admission?",
        "answer": "Document verification process: 1) After CAP seat allotment, visit the allotted college or facilitation center within the deadline. 2) Carry ALL original documents as listed in the admission checklist. 3) Carry 2-3 sets of self-attested photocopies of each document. 4) College officials will verify originals against photocopies and approve. 5) Biometric verification (fingerprint scanning) may be done. 6) All documents are scanned into the college system. 7) If documents are found fake or insufficient, admission is immediately canceled and legal action may be taken. 8) After successful verification, you'll receive a verification receipt/acknowledgment. 9) Keep this receipt safe — you'll need it for future reference. 10) In case of discrepancy, you may be given 7-15 days to submit the correct document.",
        "category": "admission",
    },
    {
        "question": "Can I upload scanned copies of documents for initial verification?",
        "answer": "Yes, scanned copies are accepted for online application and initial verification: 1) Accepted formats: PDF, JPG, JPEG, PNG only. 2) Maximum file size: 500 KB per document (some portals allow up to 1 MB). 3) Files must be clearly legible — no blurred, angled, or partial scans. 4) Color scans are preferred over black and white. 5) Each document should be in a separate file, clearly named (e.g., 10th_Marksheet.pdf). 6) Self-attest all documents before scanning (sign across the copy). 7) Original documents will be verified later during physical reporting to the college. 8) Keep multiple sets of photocopies ready for physical verification. 9) Low-quality scans may lead to rejection — use a scanner rather than phone camera if possible. 10) If a document is in a regional language, get a translated copy attested.",
        "category": "admission",
    },
    {
        "question": "What is the format for scanned documents?",
        "answer": "Scanned document format guidelines: 1) PDF format is preferred for multi-page documents. 2) JPG/JPEG for single-page documents with good quality (300 DPI minimum). 3) PNG for documents requiring transparency or sharp text. 4) Maximum file size: 500 KB to 1 MB per document depending on the portal. 5) Scanning resolution: 200-300 DPI is sufficient. 6) File naming convention: DocumentType_StudentName (e.g., CETScorecard_RahulSharma.pdf). 7) Color mode: Black and white for text documents, color for certificates with seals/signatures. 8) Ensure all four corners of the document are visible in the scan. 9) No watermarks or editing on scanned copies. 10) Documents larger than the limit can be compressed using online PDF compressors.",
        "category": "admission",
    },
    {
        "question": "What is an anti-ragging affidavit and where do I get it?",
        "answer": "Anti-ragging affidavit: 1) Mandatory document required by all students during admission as per Supreme Court guidelines. 2) Two affidavits needed: one by the student, one by parent/guardian. 3) Format available on the college website or admission portal. 4) Must be printed on stamp paper (₹10-100 depending on state). 5) Attested by a notary public or first-class magistrate. 6) Content: Declaration that you will not engage in ragging and will report any ragging incidents. 7) Submit original affidavit during document verification. 8) Without valid anti-ragging affidavits, hostel allotment and final admission may be delayed. 9) The college also conducts an anti-ragging orientation session during induction.",
        "category": "admission",
    },

    # ==========================================
    # FEES & PAYMENT
    # ==========================================
    {
        "question": "What is the fee structure for engineering?",
        "answer": "Fee structure by category (approximate, per year):\n\nGovernment/Merit Quota:\n• Tuition fee: ₹30,000 - ₹80,000\n• Development fee: ₹5,000 - ₹15,000\n• Lab/library fee: ₹3,000 - ₹8,000\n• Exam fee: ₹2,000 - ₹5,000\n• Total: ₹40,000 - ₹1,20,000\n\nManagement Quota:\n• Total: ₹1,50,000 - ₹2,50,000 per year\n\nNRI Quota:\n• Total: $3,000 - $5,000 (₹2-5 lakh) per year\n\nAdditional one-time fees:\n• Admission fee: ₹5,000 - ₹10,000\n• Eligibility fee: ₹1,000 - ₹2,000\n• Caution deposit: ₹5,000 - ₹10,000 (refundable)\n• Student welfare fund: ₹1,000 - ₹3,000\n\nHostel fee separate: ₹40,000 - ₹80,000 per year.\nFee amounts vary by state, college, and year of admission.",
        "category": "fee",
    },
    {
        "question": "How can I pay the college fee?",
        "answer": "Payment methods for college fee:\n\n1) Online Portal (Recommended): Login to student portal, go to 'Fee Payment', pay via UPI, Net Banking, Debit Card, or Credit Card. Instant confirmation.\n\n2) Demand Draft: Draw DD in favor of 'The Principal/Finance Officer, [College Name]', payable at the college city's bank branch. Submit at the accounts section.\n\n3) Bank Transfer (NEFT/RTGS): Use the college bank account details from the fee receipt or portal. Save the transaction reference number.\n\n4) QR Code Scan: Many colleges now offer direct UPI payment by scanning the QR code displayed on the fee portal.\n\n5) Cash Payment: At the college fee counter (limited dates — check the schedule). Get a signed receipt.\n\nAlways save the payment receipt/transaction ID — you'll need it for future reference.",
        "category": "fee",
    },
    {
        "question": "Can I pay fees in installments?",
        "answer": "Yes, installment options: 1) Annual fee can be split into 2 installments. 2) First installment: 60% of total fee, due at admission confirmation. 3) Second installment: 40% due within 3 months of admission. 4) Submit a written installment request to the accounts section. 5) Late payment penalty: ₹50-100 per day of delay. 6) Default on second installment for more than 30 days may lead to course cancellation. 7) Some colleges offer a third installment for economically weaker students with special approval from the principal. 8) Hostel fees are usually paid in full at the start of the academic year (not in installments). 9) Installment facility is available for government/merit quota only in most cases.",
        "category": "fee",
    },
    {
        "question": "What is the hostel fee?",
        "answer": "Hostel fees by room type (approximate, per year):\n\n1) Triple sharing: ₹40,000 - ₹50,000/year\n2) Double sharing: ₹55,000 - ₹70,000/year\n3) Single room: ₹75,000 - ₹1,00,000/year (limited availability)\n\nIncludes:\n• Accommodation charges\n• Mess fees (basic meal plan — breakfast, lunch, dinner)\n• Wi-Fi and internet charges\n• Common area maintenance\n• Security and housekeeping\n\nAdditional charges:\n• AC rooms: +₹15,000-20,000/year\n• Laundry service: ₹2,000-5,000/year (optional)\n• Caution deposit: ₹5,000-10,000 (refundable at course completion)\n\nNote: Mess fees are sometimes charged separately from accommodation. Some colleges charge semester-wise (half yearly) instead of annual.",
        "category": "fee",
    },
    {
        "question": "Is there a fee concession for economically weaker students?",
        "answer": "Yes, fee concessions available:\n\n1) Tuition Fee Waiver Scheme (TFWS): 5% supernumerary seats, 100% tuition fee waiver for entire course. Eligibility: Top 1% merit list students.\n\n2) EWS Fee Concession: 25-50% fee reduction based on family income. Requires valid EWS certificate.\n\n3) SC/ST Students: Full fee reimbursement through state post-matric scholarship scheme. Tuition fee + other fees paid by the government.\n\n4) OBC Students: 50-100% fee reimbursement depending on state government policy.\n\n5) College Financial Aid: Need-based assistance from the college welfare fund for emergency cases.\n\n6) Merit Scholarships: 100% fee waiver for CET top rankers (state toppers) in some colleges.\n\nApply through the scholarship portal within the first month of admission. Late applications are generally not considered.",
        "category": "fee",
    },
    {
        "question": "What is the development fee and other charges in college?",
        "answer": "Additional charges in college fee structure:\n\n1) Development Fee: ₹5,000-15,000/year — for campus infrastructure development.\n2) Laboratory Fee: ₹2,000-5,000/year — for lab equipment maintenance.\n3) Library Fee: ₹1,000-3,000/year — for library access and digital resources.\n4) Examination Fee: ₹2,000-5,000/year — covers conduct of exams and assessment.\n5) Sports Fee: ₹500-1,500/year — for sports facilities and equipment.\n6) Medical Fee: ₹500-1,000/year — for basic health services on campus.\n7) Student Activity Fee: ₹1,000-3,000/year — for clubs, fests, cultural events.\n8) Caution Deposit: ₹5,000-10,000 (one-time, refundable at course completion).\n9) Eligibility Fee: ₹1,000-2,000 (one-time) — for university registration.\n10) Student ID Card Fee: ₹200-500 (one-time).",
        "category": "fee",
    },
    {
        "question": "What is the refund policy for admission fees?",
        "answer": "Admission fee refund policy (as per AICTE/UGC guidelines):\n\n1) Withdrawal before seat allotment: Full fee refund minus a processing fee (₹1,000-2,000).\n2) Withdrawal after seat allotment but before reporting: 80-90% refund of tuition fee.\n3) Withdrawal after reporting but before classes start: 50-70% refund of tuition fee.\n4) Withdrawal after classes start: No refund of tuition fee.\n5) Caution deposit: Fully refundable regardless of withdrawal time (minus any deductions for damages).\n6) Hostel fee: Pro-rata refund if withdrawn within 15 days of check-in.\n7) Refund processing time: 30-60 days after application.\n8) Submit a written refund application to the accounts section with original fee receipts.",
        "category": "fee",
    },

    # ==========================================
    # SCHOLARSHIPS
    # ==========================================
    {
        "question": "What scholarships are available for engineering students?",
        "answer": "Available scholarships for engineering students:\n\nGovernment Scholarships:\n1) Post-Matric Scholarship for SC/ST/OBC/EWS — full fee reimbursement + maintenance allowance.\n2) National Scholarship (NSP) — merit-based for top 12th performers.\n3) State Government Merit Scholarships — varies by state.\n\nCollege Scholarships:\n4) Merit-cum-Means Scholarship — for general category with family income below ₹2.5 lakh.\n5) CET Topper Scholarship — 100% fee waiver for CET rank holders.\n6) Sports Quota Scholarship — for national-level sportspersons.\n\nPrivate/Corporate Scholarships:\n7) Tata Trust Scholarship\n8) Aditya Birla Scholarship\n9) Narotam Sekhsaria Scholarship\n10) L'Oréal-UNESCO For Women in Science\n11) Google Generation Scholarship\n\nApply through the National Scholarship Portal (scholarships.gov.in) or the state scholarship portal. Deadlines are typically August-October.",
        "category": "fee",
    },
    {
        "question": "How do I apply for a scholarship?",
        "answer": "Scholarship application process:\n\n1) Visit the scholarship portal: National (scholarships.gov.in) or State e-Scholarship portal.\n2) Register using Aadhaar number and bank account details (bank account must be Aadhaar-linked).\n3) Fill in personal details: name, DOB, gender, category, address.\n4) Fill academic details: institute name, course, year, previous year marks.\n5) Fill family details: parental income, occupation, number of siblings.\n6) Upload required documents:\n   - Income certificate\n   - Category certificate (SC/ST/OBC/EWS)\n   - Previous year marksheet\n   - Bank passbook (first page)\n   - Aadhaar card\n   - Passport-size photo\n7) Submit before the deadline.\n8) Application is verified by the institute (first level) → then by sanctioning authority.\n9) Scholarship amount is credited directly to bank account via DBT (Direct Benefit Transfer).\n10) Renewal required every year with minimum 60% attendance and passing all subjects.",
        "category": "fee",
    },
    {
        "question": "When is the scholarship application deadline?",
        "answer": "Scholarship deadlines (typical):\n\n1) State Post-Matric Scholarships: August-September each year.\n2) National Scholarships (NSP): September-October.\n3) College-level Merit Scholarships: Within first 2 weeks of admission.\n4) Private/Corporate Scholarships: Vary widely (typically July-November).\n5) TFWS: Considered automatically during admission — no separate application.\n\nImportant Notes:\n• Late applications are generally rejected — no extension is granted.\n• Start preparing documents (income certificate, bank account, category certificates) before the admission process begins.\n• Some scholarships have limited seats — apply on the first day of the portal opening.\n• For renewal scholarships, apply early in the academic session (July-August).\n• Keep checking the scholarship portal regularly for updates and notifications.",
        "category": "fee",
    },
    {
        "question": "Can I get a scholarship if my family income is above ₹8 lakh?",
        "answer": "Scholarships for family income above ₹8 lakh: 1) You may not be eligible for income-based scholarships (EWS, Post-Matric for certain categories). 2) However, merit-based scholarships are available regardless of income: CET topper scholarships, college merit scholarships for CGPA above 8.5. 3) Private scholarships like Tata, Narotam Sekhsaria consider both merit and need but may have higher income limits. 4) Sports quota scholarships are based on achievement, not income. 5) Research fellowships (starting from 3rd year) are merit-based. 6) Some corporate scholarships (Google, Microsoft) focus on diversity rather than income. 7) Education loans are available from banks at subsidized interest rates.",
        "category": "fee",
    },

    # ==========================================
    # RESERVATION RULES
    # ==========================================
    {
        "question": "How does reservation work in engineering admissions?",
        "answer": "Reservation breakdown in state engineering colleges (typical):\n\n• General/Open: 50% of seats\n• OBC (Non-Creamy Layer): 19%\n• SC (Scheduled Caste): 13%\n• ST (Scheduled Tribe): 7%\n• EWS (Economically Weaker Section): 10%\n• PWD (Persons with Disability): 3% horizontal reservation across all categories\n• Kashmiri Migrants: 1% supernumerary\n• Defense Quota: 5% in some states\n\nKey Rules:\n• Category benefits cannot be combined — you must choose one.\n• If a reserved category seat is vacant, it goes to the open (general) category.\n• Horizontal reservations (PWD, women, defense) cut across vertical categories.\n• Percentages may vary slightly by state — check the official admission brochure.\n• Reservation is applicable only to government and government-aided college seats.",
        "category": "admission",
    },
    {
        "question": "What is PWD reservation in engineering?",
        "answer": "PWD (Person with Disability) reservation: 1) 3% horizontal reservation across all categories (General, OBC, SC, ST, EWS). 2) Minimum 40% disability as certified by a government medical board. 3) Types covered: Locomotor disability, visual impairment, hearing impairment, speech disability, mental illness, multiple disabilities. 4) PWD certificate from a government hospital or medical board is required. 5) Special amenities: wheelchair ramps, scribe for exams, extra time (20 min/hour), large print materials. 6) PWD candidates also get fee concession in some states. 7) The reservation is applied across all categories. 8) PWD candidates have the option to write exams in their preferred format (Braille, scribe, computer).",
        "category": "admission",
    },
    {
        "question": "What is TFWS quota?",
        "answer": "TFWS (Tuition Fee Waiver Scheme): 1) 5% supernumerary seats in every engineering branch. 2) 100% tuition fee waiver for the entire course duration. 3) Eligibility: Top 1% of CET/JEE merit list students (not necessarily economically weak). 4) Applicable to both government and management quota seats in AICTE-approved colleges. 5) TFWS students are selected strictly on CET/JEE merit. 6) TFWS beneficiaries cannot change college or branch mid-course. 7) If a TFWS seat is vacated, it cannot be filled by another TFWS candidate. 8) TFWS is a central government scheme — eligible in all AICTE-approved colleges. 9) Other fees (lab, library, exam) may still need to be paid by the student.",
        "category": "admission",
    },
    {
        "question": "Is there a separate reservation for girls in engineering?",
        "answer": "Yes, most states have a women's reservation policy: 1) Typically 30% horizontal reservation for women in engineering colleges. 2) Applied across all categories (General, OBC, SC, ST). 3) If sufficient women candidates are not available, the seats go to male candidates in the same category. 4) Some states have supernumerary seats exclusively for women (above the sanctioned intake). 5) Women candidates also get fee concessions in some states (e.g., free tuition for girls in Tamil Nadu). 6) Separate hostels and facilities are provided for women students. 7) Some scholarships (e.g., Google Generation, L'Oréal) are exclusively for women in engineering.",
        "category": "admission",
    },

    # ==========================================
    # STUDENT DATA FIELDS
    # ==========================================
    {
        "question": "What personal information is needed for admission?",
        "answer": "Personal information needed for admission application:\n\n1) Full Name (as on 12th marksheet)\n2) Date of Birth\n3) Gender\n4) Nationality\n5) Aadhaar Number\n6) PAN Card (optional but recommended)\n7) Email Address (personal + college)\n8) Mobile Number\n9) WhatsApp Number (optional)\n10) Correspondence Address\n11) Permanent Address\n12) City, District, State, Pincode\n13) Parent/Guardian Name\n14) Parent/Guardian Occupation\n15) Parent/Guardian Annual Income\n16) Parent/Guardian Contact Number\n17) Parent/Guardian Email\n\nHave all this information ready before starting the admission application form.",
        "category": "admission",
    },
    {
        "question": "What academic information is needed for admission?",
        "answer": "Academic information required:\n\n10th Standard (SSC/Matric):\n• Board name (State Board, CBSE, ICSE, etc.)\n• School name and address\n• Year of passing\n• Roll number\n• Subject-wise marks (especially Mathematics and Science)\n• Total marks / Percentage / CGPA\n• Marksheet number\n\n12th Standard (HSC/Intermediate):\n• Board name\n• College/Junior College name\n• Year of passing\n• Roll number\n• PCM marks (Physics, Chemistry, Mathematics individually)\n• PCM aggregate percentage\n• Overall percentage\n• Marksheet number\n\nDiploma (if lateral entry):\n• Board/University name\n• College name\n• Branch name\n• Year of passing\n• Aggregate percentage\n\nEntrance Exam:\n• CET/JEE application number\n• CET/JEE roll number\n• CET percentile / JEE Main score\n• Rank in merit list\n• Year of exam",
        "category": "admission",
    },
    {
        "question": "What department/branch information is needed?",
        "answer": "Department preference information:\n\nAvailable Engineering Branches (choose in order of preference):\n1) Computer Engineering / Computer Science & Engineering (CSE)\n2) Information Technology (IT)\n3) Electronics & Telecommunication (E&TC / ECE)\n4) Mechanical Engineering\n5) Civil Engineering\n6) Electrical Engineering\n7) Artificial Intelligence & Data Science (AIDS)\n8) Artificial Intelligence & Machine Learning (AIML)\n9) Robotics & Automation\n10) Chemical Engineering\n11) Biotechnology\n12) Automobile Engineering\n13) Mechatronics\n14) Electronics & Instrumentation\n\nYou will be asked:\n• Your preferred branch (1st, 2nd, 3rd choice)\n• Whether you are willing to accept any branch if preferences are not available\n• Whether you are willing to accept a lower preference college for your preferred branch\n• Reason for choosing engineering/this branch (for statement of purpose)",
        "category": "admission",
    },

    # ==========================================
    # COLLEGE WORKFLOWS
    # ==========================================
    {
        "question": "How does the admission approval workflow work?",
        "answer": "Admission approval workflow in Saarthi:\n\nStep 1: Student fills admission application (AI Admission section)\nStep 2: Student uploads scanned documents (Documents section)\nStep 3: Application moves to 'Pending Review' status\nStep 4: Department Coordinator reviews the application:\n   - Verifies documents against checklist\n   - Checks eligibility (PCM marks, entrance score, category)\n   - Approves or rejects with reason\nStep 5: If approved, Admin does final verification:\n   - Confirms document authenticity\n   - Assigns enrollment number\n   - Sets admission status to 'Approved'\nStep 6: Student receives approval notification with admission letter\nStep 7: Faculty Mentor is assigned automatically based on department\nStep 8: Student completes onboarding tasks (fee payment, hostel, orientation)\nStep 9: Admission status updates to 'Enrolled' after all onboarding is complete\n\nEach step generates notifications for both the student and the relevant authority.",
        "category": "general",
    },
    {
        "question": "How does document verification workflow work?",
        "answer": "Document verification workflow in Saarthi:\n\n1) Student uploads documents through the Documents section.\n2) AI performs initial checks:\n   - File type and size validation\n   - Basic OCR to extract text\n   - Checks for minimum quality (blur detection, darkness)\n3) Status set to 'Uploaded' after successful upload.\n4) Status set to 'Processing' during AI verification.\n5) Verified by the system automatically if clear:\n   - Checks required keywords match document type\n   - Verifies text is extractable\n   - Sets confidence score\n6) If confidence is high (>85%): Auto-approve, status → 'Verified'.\n7) If confidence is medium (50-85%): Flag for Admin/Coordinator review.\n8) If confidence is low (<50%) or text not extractable: Status → 'Needs Resubmit'.\n9) Admin/Coordinator reviews flagged documents:\n   - Can Approve: status → 'Verified'\n   - Can Reject with reason: status → 'Rejected', student must re-upload\n10) Student is notified of any rejection with the reason.",
        "category": "general",
    },
    {
        "question": "How does the fee payment workflow work?",
        "answer": "Fee payment workflow:\n\n1) After admission approval, fee payment is enabled in the student portal.\n2) Student views the fee breakdown in the 'Fee Payment' section.\n3) Available payment modes: Online (UPI/Card/Net Banking), DD, NEFT.\n4) Student selects the preferred payment method and completes payment.\n5) Payment confirmation is sent instantly (online) or within 2-3 working days (DD/transfer verification).\n6) Fee receipt is generated and available for download.\n7) For installment payment: First 60% paid before admission confirmation. Remaining 40% within 3 months.\n8) Late payment: System auto-calculates late fee (₹50-100/day).\n9) After full payment, 'Fee Paid' status is updated, unlocking hostel application and other onboarding tasks.\n10) Scholarship adjustments: If eligible, scholarship amount is deducted from total fee before payment.",
        "category": "fee",
    },
    {
        "question": "How does seat allotment work?",
        "answer": "Seat allotment process (within Saarthi after CAP):\n\n1) Student's CET/JEE rank and CAP allotment result are recorded in the system.\n2) Based on CAP allotment, the student's college and branch are locked in the system.\n3) Student confirms acceptance by accepting the seat in CAP portal.\n4) System updates: branch → allotted branch, college → allotted college.\n5) Onboarding tasks are auto-generated based on branch and category.\n6) Document requirements are customized based on the student's category (SC/ST/OBC/General).\n7) Fee structure is updated based on quota type (government/management).\n8) Mentor is assigned based on department.\n9) If the student is in waiting list for upgradation, system tracks preference changes.\n10) Once seat is confirmed and fee is paid, the admission is locked.",
        "category": "admission",
    },
    {
        "question": "How does mentor assignment work?",
        "answer": "Mentor assignment process:\n\n1) After admission approval, the system checks the student's allotted department.\n2) Admin or Department Coordinator assigns a faculty mentor from the same department.\n3) Each mentor can handle 15-20 students (as per AICTE guidelines).\n4) Assignment considers:\n   - Mentor's current load (number of mentees)\n   - Mentor's expertise/specialization\n   - Student's branch and category (where applicable)\n5) Student receives notification with mentor name and contact details.\n6) Mentor receives notification with assigned student details.\n7) Mentor dashboard updates with the new student.\n8) The mentor and student can communicate through the in-platform messaging system.\n9) If a mentor change is needed (e.g., mentor leaves, student requests change), Admin can reassign.\n10) Mentor guides the student through academic, personal, and career-related matters throughout the course.",
        "category": "general",
    },
    {
        "question": "What is the student onboarding workflow?",
        "answer": "Complete student onboarding workflow:\n\nStep 1 — Application: Fill admission application, upload documents, submit.\nStep 2 — Verification: Documents verified, application approved by Admin/Coordinator.\nStep 3 — Fee Payment: Pay admission fee (first installment or full).\nStep 4 — Hostel Application (if needed): Apply for hostel, upload hostel docs, pay hostel fee.\nStep 5 — Mentor Assignment: Faculty mentor assigned, introduction meeting scheduled.\nStep 6 — ID Generation: Student ID card generated, college email created.\nStep 7 — LMS Access: LMS account activated, orientation to platform.\nStep 8 — Orientation: Attend orientation program (online or in-person).\nStep 9 — Class Registration: Register for first semester courses/electives.\nStep 10 — Full Onboarding: All tasks completed, status → 'Onboarding Complete'.\n\nSaarthi tracks each step and shows progress on the student dashboard. Pending steps are highlighted with action buttons.",
        "category": "general",
    },

    # ==========================================
    # AGENTIC AI FEATURES
    # ==========================================
    {
        "question": "How does AI document verification work?",
        "answer": "AI Document Verification in Saarthi:\n\n1) Student uploads a document through the Documents section.\n2) System performs OCR (Optical Character Recognition) to extract text from the document.\n3) AI checks:\n   - Does the document type match the upload category? (e.g., uploaded in 'Marksheet' category)\n   - Are key fields present? (name, marks, date, institution name)\n   - Is the document clearly legible? (quality check)\n   - Are there signs of tampering or editing?\n4) Confidence score is calculated based on these checks.\n5) High confidence (85%+): Auto-approved, document marked as 'Verified'.\n6) Medium confidence (50-85%): Flagged for manual review by Admin/Coordinator.\n7) Low confidence (<50%): Rejected with reason, student asked to re-upload.\n8) Admin can override AI verification at any time.\n9) All verification decisions are logged for audit purposes.\n10) OCR extracted text is stored with the document record for future reference.",
        "category": "general",
    },
    {
        "question": "What is admission risk detection?",
        "answer": "Admission risk detection identifies potential issues early:\n\nRisks detected by the system:\n1) Incomplete Applications: Missing mandatory fields after 7+ days → alert sent.\n2) Document Issues: Low-quality scans, wrong document type, expired certificates → flagged.\n3) Eligibility Warnings: PCM marks below cutoff for preferred branch → suggested alternatives.\n4) Deadline Risks: Approaching deadlines with pending tasks → reminder notifications.\n5) Category Certificate Issues: Expired OBC-NCL certificates, invalid caste certificates → flagged.\n6) Fee Payment Risks: Overdue fee payments → escalation notifications.\n7) Application Abandonment: No activity for 14+ days → follow-up email.\n8) Document Expiry: Certificates that may expire before the admission deadline.\n\nEach risk generates:\n• Dashboard alert for the student\n• Notification for the relevant authority (Admin/Coordinator)\n• Suggested action to mitigate the risk",
        "category": "admission",
    },
    {
        "question": "What is dropout prediction and how does it help?",
        "answer": "Dropout prediction uses admission data to identify at-risk students:\n\nFactors analyzed:\n1) Academic background (10th/12th marks, gap years)\n2) Entrance exam performance relative to peers\n3) Category and reservation status\n4) Admission round (CAP rounds vs. spot round admits show higher dropout risk)\n5) Branch preference (students in lower-preferred branches have higher risk)\n6) Distance from home (outstation students may face adjustment challenges)\n7) Fee payment method (installment payers vs. full payers)\n8) Communication patterns (low engagement with platform)\n\nHow it helps:\n• Early identification of students needing extra support\n• Allows mentors to proactively reach out to at-risk students\n• College can offer counseling, remedial classes, or financial aid\n• Helps reduce first-year attrition rate\n• Improves student retention and satisfaction",
        "category": "general",
    },
    {
        "question": "How does mentor recommendation work?",
        "answer": "Mentor recommendation system:\n\nWhen assigning a mentor to a student, the system considers:\n\n1) Department Match: Mentor from the same department as the student.\n2) Workload Balance: Mentor should have fewer than 20 mentees.\n3) Specialization Match: Mentor's teaching/research area aligns with student's interests (if known).\n4) Past Performance: Mentors whose students show higher retention and satisfaction scores.\n5) Language Match: Mentor who speaks the student's preferred language (if available).\n6) Availability: Mentor with available office hours compatible with the student's schedule.\n\nThe system:\n• Ranks available mentors by suitability score\n• Suggests top 3 mentors for Admin/Coordinator to choose from\n• Allows manual override by Admin\n• Learns from past assignments to improve future recommendations\n• Ensures no mentor is overloaded (max 20 students per mentor as per AICTE)",
        "category": "general",
    },
    {
        "question": "How do intelligent notifications work?",
        "answer": "Intelligent notification system in Saarthi:\n\nTypes of notifications:\n\n1) Task Reminders: When a task deadline is approaching (3 days before, 1 day before, on the day).\n2) Status Updates: Application approved, document verified, mentor assigned, fee received.\n3) Action Required: Document rejected → re-upload needed. Tasks overdue → complete immediately.\n4) Deadline Alerts: CAP round deadlines, fee payment due dates, scholarship deadlines.\n5) Welcome/Onboarding: New student welcome message, orientation schedule.\n6) Risk Alerts: Missing documents, incomplete application, low-quality upload.\n7) System Announcements: College-wide notices, holiday schedules, exam schedules.\n\nDelivery channels:\n• In-app notifications (bell icon on dashboard)\n• Email (to registered email)\n• SMS (to registered mobile, for urgent alerts only)\n\nFrequency control:\n• Students can customize notification preferences in profile settings.\n• Urgent notifications (deadline, rejection) are always sent.\n• Promotional/general notifications can be muted.",
        "category": "general",
    },
    {
        "question": "What is workflow automation in Saarthi?",
        "answer": "Workflow automation features in Saarthi:\n\nAutomated Processes:\n1) Document Verification: AI auto-verifies documents with high confidence → status updated without manual intervention.\n2) Mentor Assignment: Auto-assigns mentor based on department and workload when an admin is not available.\n3) Task Generation: Onboarding tasks auto-generated based on student category, branch, and admission round.\n4) Notifications: Auto-triggered based on events, deadlines, and status changes.\n5) Application Progression: Automatic status updates as students complete each onboarding stage.\n6) Fee Calculation: Fee structure auto-calculated based on quota, category, and branch.\n7) Scholarship Eligibility Check: Auto-checks eligibility based on category, income, and marks.\n8) Report Generation: Auto-generated daily/weekly reports for Admin dashboard.\n\nManual Intervention Required For:\n• Final admission approval\n• Document verification (low confidence cases)\n• Mentor reassignment requests\n• Fee concession/dispute resolution\n• Grievance handling\n\nAutomation reduces manual workload by approximately 60%, allowing staff to focus on exceptions and complex cases.",
        "category": "general",
    },

    # ==========================================
    # HOSTEL (IN-DEPTH)
    # ==========================================
    {
        "question": "How do I apply for hostel accommodation?",
        "answer": "Hostel application process (on Saarthi):\n\n1) Login to the student portal after admission confirmation.\n2) Navigate to 'Hostel Application' section.\n3) Fill in the application form:\n   - Room preference: Single/Double/Triple\n   - AC or Non-AC\n   - Meal preference: Vegetarian/Non-Vegetarian\n   - Floor preference (if applicable)\n   - Any medical conditions or special requirements\n4) Upload required documents:\n   - Passport-size photograph\n   - Parent/Guardian consent letter (download format from portal)\n   - Medical fitness certificate\n   - Anti-ragging affidavit\n5) Pay hostel fee through the payment portal.\n6) Submit the application.\n7) Hostel allotment is first-come, first-served.\n8) Room number and reporting date are communicated via email and dashboard notification.\n9) At check-in, present original documents for verification.\n10) Collect room keys, hostel ID card, and linen (if provided).",
        "category": "hostel",
    },
    {
        "question": "What are the hostel rules and regulations?",
        "answer": "Hostel rules and regulations:\n\n1) Entry/Exit: Main gate closes at 9:00 PM daily. Late entry requires prior warden's permission. Weekend curfew: 10:00 PM.\n2) Visitors: Allowed only in common/lobby area during visiting hours (Saturday-Sunday, 4-6 PM). Overnight guests not allowed.\n3) Prohibited Items: Alcohol, tobacco, drugs, weapons, electrical appliances (heaters, irons, induction cooktops).\n4) Noise Discipline: Maintain silence after 10:00 PM. No loud music or disturbances.\n5) Mess: Fixed meal timings — Breakfast 7-9 AM, Lunch 12-2 PM, Dinner 7-9 PM. Food cannot be taken to rooms.\n6) Ragging: STRICTLY PROHIBITED. Zero tolerance. Punishable by law (UGC regulations). Immediately report to warden/anti-ragging committee.\n7) Room Maintenance: Students are responsible for room cleanliness. Regular inspections by warden/housekeeping.\n8) Electricity: Fixed monthly units included in hostel fee. Extra usage charged at ₹8-10/unit.\n9) Vehicle Parking: Two-wheeler parking available with sticker. Four-wheeler requires special permission.\n10) Leave: Must fill hostel leave form for overnight absence. Parental consent required for leaves > 2 days.\n\nViolation of rules: First offense → warning. Second offense → fine (₹500-2000). Third offense → expulsion from hostel.",
        "category": "hostel",
    },
    {
        "question": "What facilities are available in the hostel?",
        "answer": "Complete hostel facilities:\n\nAccommodation:\n• Furnished rooms: cot, mattress, study table, chair, wardrobe, bookshelf\n• Ceiling fan, tube light, curtain blinds\n• Optional AC rooms (at additional cost)\n\nUtilities:\n• 24/7 Wi-Fi (100 Mbps, fiber optic)\n• Hot water (6-8 AM and 6-8 PM in winters)\n• Power backup (inverter/generator for common areas)\n• RO drinking water on each floor\n\nCommon Facilities:\n• Mess/Dining hall (seating capacity: 200+)\n• Indoor Recreation: Table tennis, carrom, chess, TV room\n• Library/Study room (open 24/7)\n• Gymnasium (basic equipment)\n• Common room with newspapers and magazines\n\nServices:\n• Laundry: Washing machine on each floor + paid laundry service\n• Medical: First-aid kit + tie-up with nearby hospital\n• Security: 24/7 security guards, CCTV cameras, biometric entry\n• Housekeeping: Daily common area cleaning, weekly room cleaning\n\nSports:\n• Basketball court\n• Badminton court\n• Volleyball court\n• Indoor gym equipment",
        "category": "hostel",
    },
    {
        "question": "Is hostel accommodation mandatory?",
        "answer": "Hostel accommodation policy:\n\n• NOT mandatory for day scholars who reside within a 30 km radius of the college.\n• Day scholars must apply for day scholar status during admission with proof of residence.\n• Students from outside the city/town are strongly encouraged (not forced) to stay in the hostel.\n• First-year students are given priority for hostel allotment.\n• Limited seats available — first-come, first-served basis.\n• Separate girls' hostel with stricter security measures.\n• Married/part-time students may get exemption with special permission from the warden.\n• Hostel rules and fees are uniform regardless of course/branch.\n• If you decline hostel and later need it, you'll be added to a waiting list.\n• Hostel allotment is for one academic year — must reapply each year.\n\nDay scholar requirement: Submit proof of residence, parent consent for commuting, and sign an undertaking.",
        "category": "hostel",
    },
    {
        "question": "Can I get a hostel room change?",
        "answer": "Room change process:\n\n1) Submit a written application to the hostel warden stating the reason.\n2) Room changes are only processed at the beginning of each semester (not mid-semester).\n3) Valid reasons: Medical issues (with doctor's certificate), safety concerns, compatibility issues.\n4) Mutual exchange between two willing students is the easiest process — both submit a joint request.\n5) Upgrading from triple/double to single depends on availability.\n6) Processing time: 1-2 weeks after semester start.\n7) Administrative fee: ₹500-1,000 for room change processing.\n8) Temporary room changes (less than 7 days) allowed with warden's permission.\n9) Unauthorized room changes are punished with a fine (₹1,000-2,000).\n10) Room change during exam season is generally not permitted.\n\nNote: Room changes are not allowed in the first month of joining (stabilization period).",
        "category": "hostel",
    },
    {
        "question": "What happens if I damage hostel property?",
        "answer": "Hostel property damage policy:\n\n1) Minor damages (bulb replacement, minor repairs): Fixed by the hostel maintenance team at no charge.\n2) Accidental damages: Report immediately to the warden. Cost of repair/replacement is billed to the student.\n3) Intentional/vandalism: Fine of ₹2,000-10,000 depending on severity + disciplinary action.\n4) Damage to common area property (TV, furniture, sports equipment): Cost shared by all residents of the floor/wing if the responsible person is not identified.\n5) Room damages during stay: Deducted from caution deposit at checkout.\n6) Fire/electrical damage: Cost may be recovered from the responsible student.\n7) Major damages (structural): May lead to expulsion from hostel and campus.\n\nRegular room inspections are conducted to identify damages early. Report any pre-existing damage at check-in to avoid being charged at checkout.",
        "category": "hostel",
    },

    # ==========================================
    # ACADEMIC (IN-DEPTH)
    # ==========================================
    {
        "question": "What is the academic calendar?",
        "answer": "Academic calendar (typical engineering program):\n\nOdd Semester (July-December):\n• Classes begin: First week of August\n• Mid-semester exams: October (1-week break)\n• Assignment/project submissions: November\n• End-semester exams: December (3 weeks)\n• Winter break: Last week December - first week January\n\nEven Semester (January-June):\n• Classes begin: Second week of January\n• Mid-semester exams: March\n• Assignment/project submissions: April\n• End-semester exams: May/June\n• Summer break: June-July (4-6 weeks)\n\nKey points:\n• Lab sessions on Saturdays or specific weekdays\n• Industrial visits/Training: Usually in semester breaks\n• Workshops: Periodically on Saturdays\n• Academic calendar is published on the college website and LMS before each semester\n• Minimum 180 instructional days per year as per AICTE norms\n• Attendance is counted from the first day of each semester",
        "category": "academic",
    },
    {
        "question": "What is the attendance requirement?",
        "answer": "Attendance policy:\n\nMinimum 75% attendance required in EACH subject individually:\n\nConsequences of low attendance:\n• Below 75% but above 65%: Warning letter issued to student and parents\n• Below 65% but above 50%: Detained from appearing in end-semester exams for that subject\n• Below 50%: May lead to course deregistration (must repeat the course)\n\nAttendance calculation:\n• Lecture classes: Counted at 100% (each hour = 1 session)\n• Tutorials: Counted at 100%\n• Labs/practicals: Counted at 100% (each 2-hour lab = 1 session)\n\nLeave and exemptions:\n• Medical leave: Counted if supported by valid medical certificate submitted within 3 days\n• On-Duty (OD): College-approved participation in events/fests can compensate up to 5% shortage\n• Maximum OD allowed: 5% of total sessions per semester\n• OD must be applied for in advance through the faculty coordinator\n\nTrack attendance regularly through the LMS portal.",
        "category": "academic",
    },
    {
        "question": "How does the grading system work?",
        "answer": "Grading system (10-point CGPA scale):\n\nGrade Points:\nO (Outstanding): 10 points (90%+)\nA+ (Excellent): 9 points (80-89%)\nA (Very Good): 8 points (70-79%)\nB+ (Good): 7 points (65-69%)\nB (Above Average): 6 points (60-64%)\nC (Average): 5 points (55-59%)\nP (Pass): 4 points (50-54%)\nF (Fail): 0 points (<50%)\n\nCalculation:\n• SGPA (Semester GPA) = Sum(Course Credits × Grade Points) / Sum(Course Credits)\n• CGPA = Weighted average of all semesters' SGPA\n\nEvaluation Breakdown:\n• Internal Assessment (40%): Class tests (2), assignments, lab work, quizzes, presentations\n• End Semester Exam (60%): 3-hour written exam covering full syllabus\n\nPassing Requirements:\n• Minimum 40% in internal assessment AND minimum 40% in end-semester exam SEPARATELY\n• Overall minimum 50% (Grade P) to pass a course\n• Minimum CGPA 4.0 to graduate\n\nA 10-point CGPA of 6.0 = 60% marks for placement eligibility at most companies.",
        "category": "academic",
    },
    {
        "question": "How can I register for elective courses?",
        "answer": "Elective course registration:\n\n1) List of offered electives published on LMS 2 weeks before the semester start.\n2) Login to student portal → Academic → Elective Registration.\n3) Select 1-2 electives (available from 3rd year onward, minimum 1 per semester).\n4) Registration is first-come-first-served — limited seats per elective (usually 30-60).\n5) Registration window: 1 week (typically in the first 2 weeks of the semester).\n6) Professional Electives (Department-specific) and Open Electives (other departments) available.\n7) Some electives have prerequisites — check eligibility before registering.\n8) If your preferred elective is full, you get your second choice.\n9) Once registered, you cannot change electives mid-semester.\n10) Withdrawal allowed within the first 2 weeks of the semester.\n\nPopular department electives: Machine Learning, Cloud Computing, Embedded Systems, VLSI Design, Robotics, Data Analytics.",
        "category": "academic",
    },
    {
        "question": "Can I change my branch after first year?",
        "answer": "Branch change rules:\n\nEligibility:\n• Must complete first-year courses WITHOUT any backlogs (clear all subjects).\n• First-year CGPA determines eligibility — minimum 8.0+ CGPA usually required.\n• Seat must be available in the desired branch (vacancies after first year allocation).\n• Limited to top 5-10% of students based on merit.\n\nProcess:\n1) Branch change applications open in the first 2 weeks of the second year.\n2) Submit application through the academic office with preferred branch.\n3) Selection based on merit list of applicants.\n4) Approved candidates are notified within 2-3 weeks.\n5) Once changed, cannot revert to the original branch.\n\nImportant Notes:\n• Not possible between engineering (B.E./B.Tech) and non-engineering programs.\n• Lateral entry students are generally not eligible for branch change.\n• Credits earned in first-year common subjects are transferred.\n• Branch-specific courses from first year (if any) may need to be completed additionally.\n• Contact the academic office for exact cutoff CGPA and available seats.",
        "category": "academic",
    },
    {
        "question": "What happens if I fail (backlog) in a subject?",
        "answer": "Backlog (failed subject) policy:\n\n1) You can appear for a supplementary exam in the next semester's exam cycle.\n2) Carry up to 4 backlogs and still be promoted to the next academic year.\n3) More than 4 active backlogs: You will be detained (year-back) and must repeat the year.\n4) Supplementary exam fee: ₹500 per subject.\n5) No limit on the number of attempts, but:\n   - First 2 attempts: Regular supplementary exam schedule\n   - 3rd attempt onward: May require special permission + higher fee (₹1,000-2,000)\n6) Clear ALL backlogs before the start of the final year to be eligible for graduation.\n7] Apply for supplementary exams through the exam section within 15 days of result declaration.\n8) The best score among original + supplementary attempts = final grade.\n9) Backlog subjects impact CGPA even after clearing (grade C/P max for backlog clearance in some colleges).\n10) Attendance in backlog subjects: If failed due to attendance shortage, must repeat the course.",
        "category": "exam",
    },

    # ==========================================
    # LMS (IN-DEPTH)
    # ==========================================
    {
        "question": "How do I access the LMS portal?",
        "answer": "LMS access guide:\n\nURL: Your college-specific LMS URL (provided during orientation, typically https://lms.[collegename].ac.in)\n\nLogin Credentials (First Time):\n• Username: Your enrollment/admission number (printed on ID card)\n• Password: Your date of birth in DDMMYYYY format\n\nAfter First Login:\n• MUST change password immediately (alphanumeric + special char, min 8 characters)\n• Set up security questions for password recovery\n• Update your profile (email, phone, profile photo)\n\nCompatible Browsers:\n• Chrome (recommended)\n• Firefox\n• Edge\n• Safari\n\nIf Login Issues:\n• Click 'Forgot Password' on the LMS login page\n• Reset link sent to registered college email\n• Check spam folder if not received\n• IT helpdesk: it-support@college.ac.in or visit Room B-201\n• Support hours: Mon-Fri, 9 AM - 5 PM\n\nMobile Access:\n• Fully responsive on mobile browsers\n• No dedicated mobile app currently (coming soon)",
        "category": "lms",
    },
    {
        "question": "What can I do on the LMS portal?",
        "answer": "LMS features and modules:\n\nCourse Materials:\n• Lecture notes, slides (PDF/PPT)\n• Reference books and articles\n• Video lectures (recorded)\n• Lab manuals\n\nAssignments:\n• View assignment details and deadlines\n• Upload submissions (PDF, DOC, images)\n• Check plagiarism report (Turnitin integrated)\n• View grades and feedback\n\nAcademic Records:\n• Marks scored in class tests, assignments, mid-semester\n• Attendance percentage (subject-wise)\n• Semester grade sheets\n• CGPA/SGPA tracking\n\nCommunication:\n• Discussion forums (course-specific threads)\n• Direct messaging with faculty\n• Course announcements\n• Email notifications\n\nSchedule:\n• Weekly timetable with room numbers\n• Exam schedule and seating arrangement\n• Event calendar (workshops, seminars, holidays)\n\nStudy Tools:\n• Form study groups with classmates\n• Share notes and resources\n• Access previous year question papers\n\nNotifications: Get alerts for new assignments, grade updates, schedule changes, and exam announcements.",
        "category": "lms",
    },
    {
        "question": "I forgot my LMS password. How do I reset it?",
        "answer": "LMS password reset process:\n\nOnline Method:\n1) Go to LMS login page → Click 'Forgot Password' link.\n2) Enter your registered college email address.\n3) Password reset link sent within 5 minutes.\n4) Click the link → Create new password.\n5) Login with new password.\n\nOffline Method (if online reset fails):\n1) Visit the Computer Center / IT helpdesk (Room B-201).\n2) Carry your student ID card.\n3) Request manual password reset.\n4) New password provided immediately.\n5) Hours: Mon-Fri, 9 AM - 5 PM.\n\nEmail Support:\n• Email: it-support@college.ac.in\n• Include: Your full name, enrollment number, branch, and year in the email.\n• Response time: Within 24 hours on working days.\n\nTips:\n• Check spam/promotions folder if link not received.\n• Password must be 8+ chars with uppercase, lowercase, number, and special character.\n• Do not share your password with anyone.\n• Change password every 6 months as per security policy.",
        "category": "lms",
    },

    # ==========================================
    # PLACEMENT (IN-DEPTH)
    # ==========================================
    {
        "question": "How does campus placement work?",
        "answer": "Campus placement process:\n\nTimeline: August to March of the final academic year.\n\nStep-by-step:\n1) Registration: Register on the placement portal with updated resume by July.\n2) Pre-Placement Training (3rd year onwards):\n   - Aptitude training (Quant, Logical, Verbal)\n   - Coding practice (C++, Java, Python, DSA)\n   - Soft skills and interview preparation\n3) Company Arrival: Companies register for campus recruitment drives.\n4) Pre-Placement Talk (PPT): Company presents its profile, role, package, criteria.\n5) Online Test: Aptitude, technical, coding tests.\n6) Group Discussion (if applicable): Topic discussion round.\n7) Technical Interview: Domain knowledge, projects, coding.\n8) HR Interview: Communication, attitude, career goals.\n9) Offer Letter: Selected candidates receive offer letter.\n10) Acceptance: Accept or decline the offer.\n\nRules:\n• One-offer policy: Once placed, cannot sit for other companies.\n• Eligibility: Minimum 6.0 CGPA, no active backlogs.\n• Dress code: Formal attire for all placement activities.\n\nAverage packages: ₹4-8 LPA depending on branch and company.",
        "category": "placement",
    },
    {
        "question": "When should I start preparing for placements?",
        "answer": "Placement preparation timeline:\n\n1st Year:\n• Focus on communication skills (English).\n• Learn basics of one programming language (C or Python).\n• Build a strong foundation in Mathematics.\n\n2nd Year:\n• Start DSA (Data Structures & Algorithms).\n• Practice on LeetCode, HackerRank (minimum 50 problems).\n• Learn OOP concepts (C++/Java).\n• Build small projects.\n\n3rd Year:\n• Deepen DSA (100+ problems on LeetCode).\n• Learn web development / frameworks (React, Django, Spring Boot).\n• Build 2-3 substantial projects.\n• Contribute to open source.\n• Participate in hackathons.\n• Do a summer internship (highly recommended).\n\nFinal Year (Pre-Placement):\n• Polish resume (1 page, achievement-oriented).\n• Practice mock interviews (peer groups, placement cell).\n• Solve last year company-specific papers.\n• Prepare HR interview answers (Tell me about yourself, strengths, weaknesses, etc.).\n• Attend the placement cell's 3-month training program (May-July).\n\nRecommended daily: 1-2 hours of coding practice, 30 minutes of aptitude.",
        "category": "placement",
    },
    {
        "question": "What is the minimum CGPA required for placements?",
        "answer": "Minimum CGPA requirements by company tier:\n\nTop Tier (Google, Microsoft, Amazon, Adobe, Uber):\n• CGPA: 7.5 - 8.0 minimum\n• No active backlogs\n• Strong DSA + projects required\n\nMid Tier (Service-based: TCS, Infosys, Wipro, Accenture):\n• CGPA: 6.0 minimum\n• No active backlogs (or max 1 backlog allowed)\n• Basic aptitude + communication skills\n\nCore Companies (L&T, Mahindra, Bosch, Siemens):\n• CGPA: 6.5 - 7.0 minimum\n• Domain knowledge important\n\nIT Services (Cognizant, Tech Mahindra, Capgemini):\n• CGPA: 5.5 - 6.0 minimum\n• Good communication skills\n\nStartups:\n• CGPA: Varies, but 7.0+ preferred\n• Focus on skills and portfolio\n\nKey takeaway: Higher CGPA = access to more companies and better packages. Maintain at least 7.5+ to keep all options open.",
        "category": "placement",
    },
    {
        "question": "Which companies visit the campus for placements?",
        "answer": "Companies that typically visit for campus placements:\n\nIT/Software Companies:\n• TCS (Tata Consultancy Services)\n• Infosys\n• Wipro\n• Accenture\n• Capgemini\n• Tech Mahindra\n• Cognizant (CTS)\n• IBM\n• HCL Technologies\n• LTI Mindtree\n\nProduct/Tech Companies:\n• Microsoft (select colleges)\n• Amazon (select colleges)\n• Google (top NITs/IITs)\n• Adobe\n• Oracle\n• SAP\n\nCore Engineering Companies:\n• Larsen & Toubro (L&T)\n• Mahindra & Mahindra\n• Bosch\n• Siemens\n• Tata Motors\n• Schaeffler\n• Cummins\n\nBanking/Finance:\n• HDFC Bank\n• ICICI Bank\n• JP Morgan (select)\n\nNote: Company visits depend on college reputation, accreditation, and placement cell relationships. Not all companies visit every college.",
        "category": "placement",
    },

    # ==========================================
    # MENTOR SYSTEM (IN-DEPTH)
    # ==========================================
    {
        "question": "How does the faculty mentor system work?",
        "answer": "Faculty Mentor System in Saarthi:\n\nPurpose:\n• Each student is assigned a faculty mentor after admission approval.\n• Mentor acts as the primary point of contact for academic, personal, and career guidance.\n• One mentor per 15-20 students (as per AICTE norms).\n\nMentor Responsibilities:\n1) Track student's academic progress and attendance each semester.\n2) Conduct regular mentor meetings (bi-weekly or monthly).\n3) Help with course selection and elective choices.\n4) Identify at-risk students (low attendance, backlogs) and provide support.\n5) Guide project selection, internship search, and placement preparation.\n6) Approve onboarding tasks and verify their completion.\n7) Provide personal counseling or refer to the student counselor if needed.\n8) Maintain notes of each mentoring session.\n\nMentee (Student) Responsibilities:\n1) Attend scheduled mentor meetings.\n2) Inform mentor about academic difficulties.\n3) Seek guidance for course/career decisions.\n4) Maintain regular communication.\n5) Update mentor on progress and achievements.\n\nMeeting Cadence:\n• Individual meetings: At least once per month\n• Group meetings: Once per semester\n• Emergency meetings: As needed",
        "category": "general",
    },
    {
        "question": "How do I contact my faculty mentor?",
        "answer": "Contacting your faculty mentor:\n\nThrough Saarthi Platform:\n1) Login to your student dashboard.\n2) Mentor name and contact details are displayed on the dashboard.\n3) Use the in-platform messaging/communication tool to send a message.\n4) Schedule a 1-on-1 meeting through the 'Meetings' section.\n5) Check mentor's availability (office hours) and book a slot.\n\nOffline:\n• Mentor's office/cabin location is provided in the profile.\n• Office hours: Mon-Fri, 10 AM - 4 PM (or as displayed on the door).\n• Can meet during free periods — take prior appointment.\n\nCommunication Etiquette:\n• Use formal and respectful language.\n• Be clear about the purpose of the meeting.\n• Prepare any documents/information needed.\n• Be punctual for scheduled meetings.\n• Follow up if you don't get a response within 48 hours.\n\nUrgent Matters:\n• Email the mentor directly with 'URGENT' in the subject line.\n• If no response in 24 hours, contact the Department Coordinator or HOD.",
        "category": "general",
    },
    {
        "question": "What happens after my admission is approved?",
        "answer": "Post-approval process on Saarthi:\n\nImmediately After Approval:\n1) Receive admission approval notification (in-app + email).\n2) Download admission letter from the AI Admission section.\n3) Faculty mentor is assigned (notification sent to both).\n4) Full student portal access is granted.\n\nNext Steps:\n5) Register for the orientation program (date and link shared).\n6) Receive student ID card and college email credentials.\n7) LMS access is activated — you can log in and explore.\n8) Onboarding tasks are auto-generated in the My Tasks section.\n9) Apply for hostel if needed (Hostel Application section).\n10) Pay first semester fee (or first installment) if not already paid.\n\nOnboarding Checklist (in order):\n• Complete personal profile\n• Upload remaining documents\n• Verify email address\n• Pay admission fee\n• Apply for hostel (if needed)\n• Register for orientation\n• Complete admission application form\n• Track all checklist items\n\nYour dashboard shows a progress bar tracking these steps. Aim to complete everything before orientation day.",
        "category": "general",
    },

    # ==========================================
    # ONBOARDING & PORTAL (IN-DEPTH)
    # ==========================================
    {
        "question": "What tasks do I need to complete after admission?",
        "answer": "Post-admission onboarding tasks:\n\nMandatory Tasks (Complete these first):\n1) Complete personal profile (name, contact, address, parent details)\n2) Upload admission documents (marksheets, certificates, photo, ID proof)\n3) Verify your email address\n4) Pay the admission fee (first installment or full)\n5) Complete the admission application form with all details\n\nOptional but Recommended:\n6) Apply for hostel accommodation (if you need to stay on campus)\n7) Register for the orientation program\n8) Explore the LMS portal\n9) Set up your college email\n10) Submit scholarship applications (if eligible)\n\nTask Tracking:\n• Visit the 'My Tasks' section for a personalized checklist with due dates\n• Each task shows: title, description, category (DOCUMENT/FEE/ACADEMIC/ORIENTATION/GENERAL)\n• Mandatory tasks are clearly marked\n• Tasks requiring document upload are indicated\n• Progress tracking: Dashboard shows completion percentage\n• Overdue tasks are highlighted in red\n\nMissing a mandatory task may delay your final enrollment. Complete all tasks before the orientation date.",
        "category": "general",
    },
    {
        "question": "How do I navigate the Saarthi portal?",
        "answer": "Saarthi portal navigation guide:\n\nSidebar Menu (Desktop — Left Side):\n1) Dashboard — Home screen with progress, quick actions, system status\n2) AI Admission — Admission application form with AI copilot\n3) Ask Saarthi — AI assistant for admission FAQs and help\n4) My Tasks — Personalized onboarding checklist with progress tracking\n5) Documents — Upload and manage admission documents\n6) Fee Payment — View fee structure and pay online\n7) Notifications — Bell icon at the top for alerts\n8) Profile — Update personal details, password, preferences\n\nMobile Navigation:\n• Sidebar collapses into a hamburger menu (top-left)\n• Swipeable interface for mobile browsing\n• All features accessible on mobile\n\nRole-Specific Navigation:\n• Student: Dashboard, AI Admission, Ask Saarthi, My Tasks, Documents, Fee Payment\n• Admin: All Applications, Pending Documents, Analytics, Users, Knowledge Base\n• Coordinator: Department Students, Pending Approvals, Analytics\n• Mentor: Assigned Students, Mentoring Notes, Communication\n• System Admin: Users, Roles, Permissions, System Config, Audit Logs\n\nTip: Use the Ask Saarthi search as a quick way to find answers to admission queries.",
        "category": "general",
    },
    {
        "question": "How do I use the AI assistant effectively?",
        "answer": "Using Saarthi AI assistant effectively:\n\n1) Ask in natural language: Type your question as you would ask a human counselor. For example: 'What documents do I need for OBC category admission?'\n\n2) Be specific: Include relevant details for better answers. Good: 'My CET score is 92 percentile and I want Computer Engineering. Which colleges can I get?' Instead of: 'Which colleges can I get?'\n\n3) Use category filter: When available, select a topic category to narrow down search (Admissions, Fees, Hostel, etc.).\n\n4) Follow up: The assistant remembers your conversation context. Ask follow-up questions like 'What about the fee structure for CS?' or 'How do I apply for scholarship?'\n\n5) Check sources: The assistant cites sources from the knowledge base. You can verify details by reading the full entry.\n\n6) Raise a ticket: If the AI can't fully answer your question, ask it to create a support ticket for you.\n\n7) Verify critical info: For time-sensitive details like exact deadlines or fee amounts, cross-check with the admin office or raise a support ticket.\n\nTip: Use the AI Admission section for filling your application form, and Ask Saarthi for general admission queries.",
        "category": "general",
    },
    {
        "question": "How to track my admission application status?",
        "answer": "Track admission application status:\n\n1) Go to 'AI Admission' section from the sidebar menu.\n2) Your current status is displayed prominently at the top of the page.\n\nStatus Flow:\nNot Applied → Applied → Documents Uploaded → Documents Verified → Approved → Enrolled\n\nWhat each status means:\n• Not Applied: You haven't started your application.\n• Applied: Application submitted but documents pending.\n• Documents Uploaded: All documents uploaded but not yet verified.\n• Documents Verified: All documents verified by AI or Admin.\n• Approved: Admission approved by Admin. Admission letter available for download.\n• Enrolled: Fee paid, onboarding complete, fully enrolled.\n\nWhat you should do:\n• If Rejected: Check the rejection reason and re-submit.\n• If Pending for >3 days: Contact admin through support ticket.\n• If Approved: Download your admission letter from the same section.\n\nNotifications: You'll be notified via in-app alert and email whenever your application status changes.",
        "category": "general",
    },
    {
        "question": "How to raise a support ticket on Saarthi?",
        "answer": "Creating a support ticket:\n\n1) Click on the 'Help' or 'Support' option (available on the footer or sidebar).\n2) Click 'Create New Ticket'.\n3) Fill in:\n   - Title: Brief description of your issue\n   - Description: Detailed explanation of the problem\n   - Category: Technical, Admission, Fee, Document, Mentor, Other\n   - Priority: Low, Medium, High, Urgent\n   - Attachments: Upload screenshots or relevant documents (if any)\n4) Submit the ticket.\n\nAfter submission:\n• Ticket is assigned to the relevant department.\n• You'll receive a ticket ID (e.g., TKT-2026-0042).\n• Track ticket status: Open → In Progress → Resolved → Closed.\n• You'll be notified via in-app notification and email on status updates.\n• Response time: 24-48 hours for standard tickets, 12-24 hours for urgent.\n\nFor Urgent Issues:\n• Select 'Urgent' priority in the ticket.\n• Also call the relevant department (numbers available on the Contact page).\n• In-person: Visit the helpdesk (Room A-101, ground floor).",
        "category": "general",
    },
    {
        "question": "What should I do if I face technical issues on the portal?",
        "answer": "Troubleshooting common technical issues:\n\n1) Page Not Loading: Refresh the page. Clear browser cache (Ctrl+Shift+Del). Try Incognito mode.\n2) Login Issues: Ensure caps lock is off. Try 'Forgot Password' to reset. Clear localStorage errors (logout and re-login).\n3) 401 Unauthorized: Your session expired. Log out completely and log back in.\n4) 500 Server Error: Server is temporarily down. Wait 5 minutes and try again.\n5) Slow Loading: Check your internet speed. Try a different browser (Chrome/Firefox recommended).\n6) File Upload Fails: Ensure file is under 10 MB. Accepted formats: PDF, JPG, JPEG, PNG. File names should not contain special characters.\n7) Form Not Submitting: Check all mandatory fields are filled. Ensure no validation errors.\n8) Page Broken: Update your browser to the latest version.\n\nIf issues persist:\n• Raise a support ticket (include browser, OS, and error details).\n• Contact IT helpdesk: it-support@college.ac.in\n• Visit IT support desk (Room B-201) during office hours (Mon-Fri, 9 AM-5 PM).",
        "category": "general",
    },
    {
        "question": "Can I access Saarthi on my mobile phone?",
        "answer": "Yes, Saarthi is fully responsive:\n\n• Access through any mobile browser (Chrome, Safari, Firefox).\n• UI automatically adjusts to your screen size.\n• All features available on mobile.\n• Sidebar becomes a hamburger menu on small screens.\n• Upload documents, chat with AI, complete tasks from your phone.\n• Touch-friendly buttons and dropdowns.\n• Optimized for screens as small as 320px wide.\n\nBest Experience On:\n• Chrome (Android) or Safari (iOS) — latest versions.\n• Minimum internet speed: 2 Mbps recommended.\n• Enable cookies and JavaScript.\n\nComing Soon: Dedicated mobile app (Android + iOS) for an even better experience.",
        "category": "general",
    },
    {
        "question": "What is the college timings?",
        "answer": "College timings:\n\nAcademic Hours:\n• Regular classes: 9:00 AM to 4:30 PM (Monday to Friday)\n• Saturday: 9:00 AM to 1:00 PM (labs, tutorials, extra classes only)\n• Sunday: Holiday\n\nFacility Timings:\n• Library: 8:00 AM to 8:00 PM (Monday to Saturday)\n• Computer Labs: 9:00 AM to 6:00 PM (Monday to Saturday)\n• Sports Grounds: 6:00 AM to 8:00 AM (morning), 4:30 PM to 7:00 PM (evening)\n• Canteen: 8:00 AM to 7:00 PM (all days)\n\nAdministrative Office:\n• Office Hours: 10:00 AM to 5:00 PM (Monday to Friday)\n• Lunch Break: 1:00 PM to 2:00 PM\n• Saturday: Limited operations (10:00 AM to 1:00 PM)\n• Sunday: Closed\n\nEmergency Contact:\n• Campus Security (24/7): +91-XXXX-XXXXXX\n• Medical Emergency: +91-XXXX-XXXXXX\n\nNote: Timings may change on holidays, exam days, or special events. Check the college calendar for exceptions.",
        "category": "general",
    },
    {
        "question": "Who should I contact for different types of help?",
        "answer": "Department contact directory:\n\n1) Admission Queries:\n   - Email: admission@college.ac.in\n   - Visit: Admission helpdesk (Ground floor, Admin Block)\n   - Hours: Mon-Fri, 10 AM - 5 PM\n\n2) Fee/Accounts Related:\n   - Email: accounts@college.ac.in\n   - Visit: Accounts section (Admin Block, Room 104)\n\n3) Hostel Issues:\n   - Report: Floor warden (emergency) / Hostel office (General)\n   - Email: hostel@college.ac.in\n\n4) Academic Queries:\n   - Contact: Class Coordinator (identified at the start of semester)\n   - Escalate: Head of Department (HOD)\n\n5) IT/LMS Support:\n   - Email: it-support@college.ac.in\n   - Visit: Computer Center, Room B-201\n   - Hours: Mon-Fri, 9 AM - 5 PM\n\n6) Placement Related:\n   - Email: placement@college.ac.in\n   - Visit: Placement Cell (2nd floor, Academic Block)\n\n7) General Helpdesk:\n   - Visit: Main office / College reception\n   - Phone: +91-XXXX-XXXXXX\n\n8) Emergency:\n   - Campus Security: +91-XXXX-XXXXXX (24/7)\n   - Medical Room: +91-XXXX-XXXXXX",
        "category": "general",
    },

    # ==========================================
    # MANAGEMENT & NRI QUOTA
    # ==========================================
    {
        "question": "What is management quota in engineering colleges?",
        "answer": "Management quota in engineering:\n\n1) Definition: Seats reserved by private college management for direct admission.\n2) Percentage: 15-30% of total seats in private unaided colleges.\n3) Admission Criteria: Based on 12th marks (PCM aggregate) — CET/JEE not required.\n4) No CAP Round: Direct admission through the college admission office.\n5) Fee: Higher than government quota — ₹1.5-2.5 lakh/year (varies by college and branch).\n6) Eligibility: Minimum 45% in PCM in 12th (40% for reserved categories).\n7) Admission Process: First-come, first-served — early applicants get priority.\n8) Some colleges have their own entrance test for management quota.\n9) Degree: Management quota students receive the same degree as government quota students.\n10) Transfer: Management quota students cannot switch to government quota mid-course.",
        "category": "admission",
    },
    {
        "question": "What is NRI quota in engineering?",
        "answer": "NRI quota for engineering admission:\n\n1) Definition: 5-10% seats reserved for Non-Resident Indian (NRI) / PIO / OCI candidates.\n2) Fee: Higher — typically $3,000-$5,000 per year or ₹2-5 lakh.\n3) Eligibility: Based on 12th marks (no CET/JEE required in most cases).\n4) Who qualifies: NRI students, children of NRIs, or NRI-sponsored students.\n5) Documents needed: NRI status proof — passport, visa, work permit, or NRI certificate.\n6) NRI Sponsorship: A relative in India (parent, sibling) can sponsor an NRI seat with proof of NRI status.\n7) OCI/PIO card holders are also eligible under NRI quota.\n8) Separate application process through the college's international cell.\n9) Some colleges accept foreign exam scores (SAT, ACT).\n10) NRI quota students get the same degree and status as regular students.\n\nNote: NRI quota rules vary by college and state. Contact the admission office for specific eligibility requirements.",
        "category": "admission",
    },

    # ==========================================
    # AI ADMISSION ASSISTANT (SAARTHI FEATURES)
    # ==========================================
    {
        "question": "How do I fill the admission application on Saarthi?",
        "answer": "Filling the admission application on Saarthi:\n\n1) Go to 'AI Admission' section from the sidebar.\n2) The form is pre-filled with your profile details (name, email, phone from your account).\n3) Fill in remaining fields step by step:\n   - Personal Details: Full name, DOB, gender, nationality, Aadhaar\n   - Contact: Address, city, state, pincode, alternate phone\n   - Parent/Guardian: Name, occupation, income, contact\n   - Academic: 10th board, percentage, year; 12th board, percentage, year\n   - Entrance Exam: CET/JEE score, percentile, rank\n   - Preferences: Top 3 branch choices\n   - Category: General/OBC/SC/ST/EWS\n   - Hostel: Yes/No\n   - Documents: Upload scanned copies\n4) You can either:\n   - Fill fields directly in the form (click and type)\n   - OR chat with the AI assistant to fill fields through conversation\n5) Review all information before final submission.\n6) Submit: You'll receive a confirmation with an application number.\n7) Track status in the same section.\n\nTip: Use the AI assistant on the right panel to auto-fill fields from your conversation!",
        "category": "admission",
    },
    {
        "question": "What is the AI admission assistant and how does it help?",
        "answer": "AI Admission Assistant (Saarthi Copilot):\n\n1) Conversational AI that helps with the entire admission process.\n2) Answer questions about: CET/JEE, eligibility, documents, fee, scholarships, hostel.\n3) Guide you step-by-step through the application filling process.\n4) Predict required documents based on: Your category (SC/ST/OBC/General), course, and quota type.\n5) Auto-fill form fields from natural conversation:\n   - Say 'My name is Rahul Sharma and I scored 85% in 12th' → fields auto-filled\n   - Say 'I want Computer Engineering' → program choice set\n6) Track admission progress: Shows completion percentage and missing fields.\n7) Dynamic question asking: If you mention your CET score, it may follow up with 'Which branch do you prefer?'\n8) Remember context across conversations — no need to repeat information.\n9) Available 24/7 — instant responses, no waiting for office hours.\n10) Access: 'AI Admission' section for application help, or 'Ask Saarthi' for general queries.",
        "category": "admission",
    },
]

ALL_ADMISSION_KNOWLEDGE = ADMISSION_KNOWLEDGE_BASE
