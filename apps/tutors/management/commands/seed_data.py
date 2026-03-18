"""
Seed Database Command
======================
Populates the database with initial subjects and languages.
"""

from django.core.management.base import BaseCommand
from apps.tutors.models import Subject, Language


class Command(BaseCommand):
    help = 'Seeds the database with initial subjects and languages'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...\n')
        self._seed_subjects()
        self._seed_languages()
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))

    def _seed_subjects(self):
        subjects = [
            # Academic
            ('Mathematics', 'academic', 'calculator'),
            ('Physics', 'academic', 'atom'),
            ('Chemistry', 'academic', 'flask-conical'),
            ('Biology', 'academic', 'leaf'),
            ('English', 'academic', 'book-open'),
            ('Hindi', 'academic', 'languages'),
            ('History', 'academic', 'landmark'),
            ('Geography', 'academic', 'globe'),
            ('Computer Science', 'academic', 'monitor'),
            ('Economics', 'academic', 'trending-up'),
            ('Accountancy', 'academic', 'file-spreadsheet'),
            ('Political Science', 'academic', 'scale'),
            ('Sanskrit', 'academic', 'scroll-text'),
            ('Social Studies', 'academic', 'users'),
            ('Environmental Science', 'academic', 'trees'),

            # Competitive Exams
            ('JEE Preparation', 'competitive', 'target'),
            ('NEET Preparation', 'competitive', 'stethoscope'),
            ('UPSC/IAS', 'competitive', 'award'),
            ('SSC', 'competitive', 'file-check'),
            ('Bank Exams', 'competitive', 'building-2'),
            ('CAT/MBA', 'competitive', 'briefcase'),
            ('GATE', 'competitive', 'cpu'),
            ('CLAT', 'competitive', 'gavel'),

            # Skills
            ('Spoken English', 'skill', 'mic'),
            ('Coding & Programming', 'skill', 'code'),
            ('Piano / Music', 'skill', 'music'),
            ('Art & Drawing', 'skill', 'palette'),
            ('Yoga & Fitness', 'skill', 'heart-pulse'),
            ('Photography', 'skill', 'camera'),
            ('Public Speaking', 'skill', 'megaphone'),

            # Language Learning
            ('French', 'language', 'flag'),
            ('German', 'language', 'flag'),
            ('Spanish', 'language', 'flag'),
            ('Japanese', 'language', 'flag'),
            ('Chinese (Mandarin)', 'language', 'flag'),
        ]

        created_count = 0
        for name, category, icon in subjects:
            _, created = Subject.objects.get_or_create(
                name=name,
                defaults={'category': category, 'icon': icon}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  📚 Subjects: {created_count} created, {len(subjects) - created_count} already existed')

    def _seed_languages(self):
        languages = [
            ('English', 'en'),
            ('Hindi', 'hi'),
            ('Bengali', 'bn'),
            ('Telugu', 'te'),
            ('Marathi', 'mr'),
            ('Tamil', 'ta'),
            ('Gujarati', 'gu'),
            ('Urdu', 'ur'),
            ('Kannada', 'kn'),
            ('Odia', 'or'),
            ('Malayalam', 'ml'),
            ('Punjabi', 'pa'),
            ('Assamese', 'as'),
            ('Maithili', 'mai'),
            ('Sanskrit', 'sa'),
        ]

        created_count = 0
        for name, code in languages:
            _, created = Language.objects.get_or_create(
                name=name,
                defaults={'code': code}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  🌐 Languages: {created_count} created, {len(languages) - created_count} already existed')
