"""
Seed Database Command
======================
Populates lookup tables and demo tutor data for local development.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import ParentProfile, TutorProfile
from apps.tutors.models import Language, Review, Subject


User = get_user_model()


KOLKATA_TUTORS = [
    {
        "email": "anirban.chatterjee@tuitionconnect.demo",
        "full_name": "Anirban Chatterjee",
        "phone_number": "+919830000101",
        "whatsapp_number": "+919830000101",
        "age": 34,
        "gender": TutorProfile.Gender.MALE,
        "qualifications": "M.Sc. in Mathematics, University of Calcutta; B.Ed.; WBJEE coaching specialist.",
        "experience_years": 10,
        "bio": "I help secondary and higher secondary students build strong problem-solving habits for board exams and engineering entrance preparation.",
        "address": "Flat 3B, Southern Avenue, Lake Market, Kolkata, West Bengal 700029",
        "latitude": 22.5177,
        "longitude": 88.3496,
        "teaching_method": TutorProfile.TeachingMethod.BOTH,
        "grade_level": TutorProfile.GradeLevel.HIGH,
        "price_per_hour": 1800,
        "subjects": ["Mathematics", "Physics", "JEE Preparation"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["madhumita", "sourav"],
    },
    {
        "email": "madhurima.sen@tuitionconnect.demo",
        "full_name": "Madhurima Sen",
        "phone_number": "+919830000102",
        "whatsapp_number": "+919830000102",
        "age": 29,
        "gender": TutorProfile.Gender.FEMALE,
        "qualifications": "M.A. in English Literature, Jadavpur University; Cambridge CELTA.",
        "experience_years": 7,
        "bio": "I focus on spoken English, ICSE and CBSE literature, and confidence-building sessions for school and college learners.",
        "address": "12/4 Hindustan Park, Gariahat, Kolkata, West Bengal 700029",
        "latitude": 22.5185,
        "longitude": 88.3647,
        "teaching_method": TutorProfile.TeachingMethod.BOTH,
        "grade_level": TutorProfile.GradeLevel.COLLEGE,
        "price_per_hour": 1500,
        "subjects": ["English", "Spoken English", "Public Speaking"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["puja", "madhumita"],
    },
    {
        "email": "subhajit.ghosh@tuitionconnect.demo",
        "full_name": "Subhajit Ghosh",
        "phone_number": "+919830000103",
        "whatsapp_number": "+919830000103",
        "age": 38,
        "gender": TutorProfile.Gender.MALE,
        "qualifications": "B.Tech. in Computer Science, MAKAUT; certified Python instructor.",
        "experience_years": 12,
        "bio": "I teach coding from school fundamentals to Python projects, with special support for ISC computer science practicals.",
        "address": "204 Salt Lake Sector 1, Bidhannagar, Kolkata, West Bengal 700064",
        "latitude": 22.5958,
        "longitude": 88.4173,
        "teaching_method": TutorProfile.TeachingMethod.ONLINE,
        "grade_level": TutorProfile.GradeLevel.COLLEGE,
        "price_per_hour": 2200,
        "subjects": ["Computer Science", "Coding & Programming", "Mathematics"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["arijit"],
    },
    {
        "email": "debarati.mukherjee@tuitionconnect.demo",
        "full_name": "Debarati Mukherjee",
        "phone_number": "+919830000104",
        "whatsapp_number": "+919830000104",
        "age": 32,
        "gender": TutorProfile.Gender.FEMALE,
        "qualifications": "M.Sc. in Chemistry, Presidency University; NET qualified.",
        "experience_years": 8,
        "bio": "My classes combine concept clarity, handwritten notes, and weekly tests for Class 9-12 chemistry and NEET aspirants.",
        "address": "9A Shyambazar Street, Shyambazar, Kolkata, West Bengal 700004",
        "latitude": 22.6025,
        "longitude": 88.3736,
        "teaching_method": TutorProfile.TeachingMethod.BOTH,
        "grade_level": TutorProfile.GradeLevel.HIGH,
        "price_per_hour": 1700,
        "subjects": ["Chemistry", "Biology", "NEET Preparation"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["puja"],
    },
    {
        "email": "sayan.banerjee@tuitionconnect.demo",
        "full_name": "Sayan Banerjee",
        "phone_number": "+919830000105",
        "whatsapp_number": "+919830000105",
        "age": 36,
        "gender": TutorProfile.Gender.MALE,
        "qualifications": "M.A. in History, University of Calcutta; B.Ed.; WBCS mentoring experience.",
        "experience_years": 11,
        "bio": "I teach humanities with structured timelines, answer-writing drills, and current affairs integration for boards and competitive exams.",
        "address": "31/2 Dum Dum Road, Dum Dum, Kolkata, West Bengal 700074",
        "latitude": 22.6248,
        "longitude": 88.4219,
        "teaching_method": TutorProfile.TeachingMethod.OFFLINE,
        "grade_level": TutorProfile.GradeLevel.HIGH,
        "price_per_hour": 1300,
        "subjects": ["History", "Political Science", "UPSC/IAS"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["sourav"],
    },
    {
        "email": "ritwika.das@tuitionconnect.demo",
        "full_name": "Ritwika Das",
        "phone_number": "+919830000106",
        "whatsapp_number": "+919830000106",
        "age": 27,
        "gender": TutorProfile.Gender.FEMALE,
        "qualifications": "M.Com., St. Xavier's University Kolkata; CA Intermediate.",
        "experience_years": 5,
        "bio": "I work with commerce students on accountancy fundamentals, exam strategy, and practical examples from real business cases.",
        "address": "89A Rashbehari Avenue, Ballygunge, Kolkata, West Bengal 700019",
        "latitude": 22.5269,
        "longitude": 88.3654,
        "teaching_method": TutorProfile.TeachingMethod.BOTH,
        "grade_level": TutorProfile.GradeLevel.COLLEGE,
        "price_per_hour": 1400,
        "subjects": ["Accountancy", "Economics", "CAT/MBA"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["madhumita"],
    },
    {
        "email": "arnab.roy@tuitionconnect.demo",
        "full_name": "Arnab Roy",
        "phone_number": "+919830000107",
        "whatsapp_number": "+919830000107",
        "age": 31,
        "gender": TutorProfile.Gender.MALE,
        "qualifications": "M.Sc. in Physics, IISER Kolkata; GATE qualified.",
        "experience_years": 9,
        "bio": "I simplify physics through visualization, numerical practice, and doubt-clearing sessions for JEE and board students.",
        "address": "55 Prince Anwar Shah Road, Tollygunge, Kolkata, West Bengal 700033",
        "latitude": 22.4973,
        "longitude": 88.3619,
        "teaching_method": TutorProfile.TeachingMethod.BOTH,
        "grade_level": TutorProfile.GradeLevel.HIGH,
        "price_per_hour": 1900,
        "subjects": ["Physics", "Mathematics", "GATE"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["arijit", "puja"],
    },
    {
        "email": "priyanka.naskar@tuitionconnect.demo",
        "full_name": "Priyanka Naskar",
        "phone_number": "+919830000108",
        "whatsapp_number": "+919830000108",
        "age": 30,
        "gender": TutorProfile.Gender.FEMALE,
        "qualifications": "M.A. in Bengali, Rabindra Bharati University; diploma in child pedagogy.",
        "experience_years": 6,
        "bio": "I teach Bengali, social studies, and foundational language skills for younger learners with activity-based lessons.",
        "address": "17 Behala Tram Depot Road, Behala, Kolkata, West Bengal 700034",
        "latitude": 22.5006,
        "longitude": 88.3182,
        "teaching_method": TutorProfile.TeachingMethod.OFFLINE,
        "grade_level": TutorProfile.GradeLevel.MIDDLE,
        "price_per_hour": 900,
        "subjects": ["Bengali", "Social Studies", "History"],
        "languages": ["English", "Hindi", "Bengali"],
        "review_refs": ["sourav"],
    },
]


KOLKATA_PARENTS = {
    "madhumita": {
        "email": "madhumita.dey.parent@tuitionconnect.demo",
        "full_name": "Madhumita Dey",
        "phone_number": "+919830001201",
        "address": "New Alipore Block L, Kolkata, West Bengal 700053",
        "latitude": 22.5107,
        "longitude": 88.3342,
        "children_count": 1,
    },
    "sourav": {
        "email": "sourav.basu.parent@tuitionconnect.demo",
        "full_name": "Sourav Basu",
        "phone_number": "+919830001202",
        "address": "Baguiati Main Road, Kolkata, West Bengal 700059",
        "latitude": 22.6135,
        "longitude": 88.4292,
        "children_count": 2,
    },
    "puja": {
        "email": "puja.sarkar.parent@tuitionconnect.demo",
        "full_name": "Puja Sarkar",
        "phone_number": "+919830001203",
        "address": "Kasba Bosepukur, Kolkata, West Bengal 700042",
        "latitude": 22.5141,
        "longitude": 88.3927,
        "children_count": 1,
    },
    "arijit": {
        "email": "arijit.dhar.parent@tuitionconnect.demo",
        "full_name": "Arijit Dhar",
        "phone_number": "+919830001204",
        "address": "Sinthi More, Kolkata, West Bengal 700050",
        "latitude": 22.6203,
        "longitude": 88.3826,
        "children_count": 1,
    },
}


REVIEWS = {
    ("anirban.chatterjee@tuitionconnect.demo", "madhumita"): {
        "rating": 5,
        "comment": "Excellent for Class 11 mathematics. My son became much more confident with algebra and calculus.",
    },
    ("anirban.chatterjee@tuitionconnect.demo", "sourav"): {
        "rating": 4,
        "comment": "Very disciplined and punctual. Weekly tests have been especially useful.",
    },
    ("madhurima.sen@tuitionconnect.demo", "puja"): {
        "rating": 5,
        "comment": "Her spoken English sessions are engaging and practical. My daughter now speaks far more fluently.",
    },
    ("madhurima.sen@tuitionconnect.demo", "madhumita"): {
        "rating": 5,
        "comment": "Strong literature guidance with clear explanation of prose and poetry answers.",
    },
    ("subhajit.ghosh@tuitionconnect.demo", "arijit"): {
        "rating": 5,
        "comment": "Great coding mentor. He explains Python from first principles and gives good project ideas.",
    },
    ("debarati.mukherjee@tuitionconnect.demo", "puja"): {
        "rating": 4,
        "comment": "Very clear chemistry notes and mock tests. Helpful for NEET preparation.",
    },
    ("sayan.banerjee@tuitionconnect.demo", "sourav"): {
        "rating": 4,
        "comment": "Makes history and polity easy to remember with timelines and current examples.",
    },
    ("ritwika.das@tuitionconnect.demo", "madhumita"): {
        "rating": 5,
        "comment": "Accountancy classes are structured and very exam-focused.",
    },
    ("arnab.roy@tuitionconnect.demo", "arijit"): {
        "rating": 5,
        "comment": "My child finally enjoys physics. The problem-solving approach is excellent.",
    },
    ("arnab.roy@tuitionconnect.demo", "puja"): {
        "rating": 4,
        "comment": "Strong conceptual teaching and regular doubt-clearing support.",
    },
    ("priyanka.naskar@tuitionconnect.demo", "sourav"): {
        "rating": 5,
        "comment": "Very warm with younger students and great at building language basics.",
    },
}


class Command(BaseCommand):
    help = "Seeds the database with lookup tables and demo Kolkata tutors"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding database...\n")

        self._seed_subjects()
        self._seed_languages()

        parent_users = self._seed_parents()
        tutor_profiles = self._seed_tutors()
        review_count = self._seed_reviews(parent_users, tutor_profiles)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
        self.stdout.write(
            f"Summary: {len(tutor_profiles)} Kolkata tutors available, "
            f"{len(parent_users)} parent accounts ready, {review_count} reviews synced."
        )

    def _seed_subjects(self):
        subjects = [
            ("Mathematics", "academic", "calculator"),
            ("Physics", "academic", "atom"),
            ("Chemistry", "academic", "flask-conical"),
            ("Biology", "academic", "leaf"),
            ("English", "academic", "book-open"),
            ("Hindi", "academic", "languages"),
            ("Bengali", "academic", "languages"),
            ("History", "academic", "landmark"),
            ("Geography", "academic", "globe"),
            ("Computer Science", "academic", "monitor"),
            ("Economics", "academic", "trending-up"),
            ("Accountancy", "academic", "file-spreadsheet"),
            ("Political Science", "academic", "scale"),
            ("Sanskrit", "academic", "scroll-text"),
            ("Social Studies", "academic", "users"),
            ("Environmental Science", "academic", "trees"),
            ("JEE Preparation", "competitive", "target"),
            ("NEET Preparation", "competitive", "stethoscope"),
            ("UPSC/IAS", "competitive", "award"),
            ("SSC", "competitive", "file-check"),
            ("Bank Exams", "competitive", "building-2"),
            ("CAT/MBA", "competitive", "briefcase"),
            ("GATE", "competitive", "cpu"),
            ("CLAT", "competitive", "gavel"),
            ("Spoken English", "skill", "mic"),
            ("Coding & Programming", "skill", "code"),
            ("Piano / Music", "skill", "music"),
            ("Art & Drawing", "skill", "palette"),
            ("Yoga & Fitness", "skill", "heart-pulse"),
            ("Photography", "skill", "camera"),
            ("Public Speaking", "skill", "megaphone"),
            ("French", "language", "flag"),
            ("German", "language", "flag"),
            ("Spanish", "language", "flag"),
            ("Japanese", "language", "flag"),
            ("Chinese (Mandarin)", "language", "flag"),
        ]

        created_count = 0
        for name, category, icon in subjects:
            _, created = Subject.objects.get_or_create(
                name=name,
                defaults={"category": category, "icon": icon},
            )
            if created:
                created_count += 1

        self.stdout.write(
            f"  Subjects: {created_count} created, {len(subjects) - created_count} already existed"
        )

    def _seed_languages(self):
        languages = [
            ("English", "en"),
            ("Hindi", "hi"),
            ("Bengali", "bn"),
            ("Telugu", "te"),
            ("Marathi", "mr"),
            ("Tamil", "ta"),
            ("Gujarati", "gu"),
            ("Urdu", "ur"),
            ("Kannada", "kn"),
            ("Odia", "or"),
            ("Malayalam", "ml"),
            ("Punjabi", "pa"),
            ("Assamese", "as"),
            ("Maithili", "mai"),
            ("Sanskrit", "sa"),
        ]

        created_count = 0
        for name, code in languages:
            _, created = Language.objects.get_or_create(
                name=name,
                defaults={"code": code},
            )
            if created:
                created_count += 1

        self.stdout.write(
            f"  Languages: {created_count} created, {len(languages) - created_count} already existed"
        )

    def _seed_parents(self):
        parent_users = {}
        for parent_key, parent_data in KOLKATA_PARENTS.items():
            user = self._upsert_user(
                email=parent_data["email"],
                full_name=parent_data["full_name"],
                phone_number=parent_data["phone_number"],
                role=User.Role.PARENT,
            )

            profile, _ = ParentProfile.objects.get_or_create(user=user)
            profile.address = parent_data["address"]
            profile.latitude = parent_data["latitude"]
            profile.longitude = parent_data["longitude"]
            profile.children_count = parent_data["children_count"]
            profile.save()

            parent_users[parent_key] = user

        self.stdout.write(f"  Parents: {len(parent_users)} synced")
        return parent_users

    def _seed_tutors(self):
        tutor_profiles = {}

        for tutor_data in KOLKATA_TUTORS:
            user = self._upsert_user(
                email=tutor_data["email"],
                full_name=tutor_data["full_name"],
                phone_number=tutor_data["phone_number"],
                role=User.Role.TUTOR,
            )

            profile, _ = TutorProfile.objects.get_or_create(user=user)
            profile.whatsapp_number = tutor_data["whatsapp_number"]
            profile.age = tutor_data["age"]
            profile.gender = tutor_data["gender"]
            profile.qualifications = tutor_data["qualifications"]
            profile.experience_years = tutor_data["experience_years"]
            profile.bio = tutor_data["bio"]
            profile.address = tutor_data["address"]
            profile.latitude = tutor_data["latitude"]
            profile.longitude = tutor_data["longitude"]
            profile.teaching_method = tutor_data["teaching_method"]
            profile.grade_level = tutor_data["grade_level"]
            profile.price_per_hour = tutor_data["price_per_hour"]
            profile.is_published = True
            profile.payment_completed = True
            profile.onboarding_step = 5
            profile.save()

            profile.subjects.set(
                Subject.objects.filter(name__in=tutor_data["subjects"]).order_by("name")
            )
            profile.languages.set(
                Language.objects.filter(name__in=tutor_data["languages"]).order_by("name")
            )

            tutor_profiles[tutor_data["email"]] = profile

        self.stdout.write(f"  Tutors: {len(tutor_profiles)} Kolkata tutor profiles synced")
        return tutor_profiles

    def _seed_reviews(self, parent_users, tutor_profiles):
        review_count = 0
        for (tutor_email, parent_key), review_data in REVIEWS.items():
            tutor = tutor_profiles[tutor_email]
            parent = parent_users[parent_key]
            Review.objects.update_or_create(
                tutor=tutor,
                parent=parent,
                defaults=review_data,
            )
            review_count += 1

        self.stdout.write(f"  Reviews: {review_count} synced")
        return review_count

    def _upsert_user(self, email, full_name, phone_number, role):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "phone_number": phone_number,
                "role": role,
                "auth_provider": User.AuthProvider.EMAIL,
                "is_active": True,
            },
        )

        if created:
            user.set_password("demo12345")

        user.full_name = full_name
        user.phone_number = phone_number
        user.role = role
        user.auth_provider = User.AuthProvider.EMAIL
        user.is_active = True
        user.save()

        return user
