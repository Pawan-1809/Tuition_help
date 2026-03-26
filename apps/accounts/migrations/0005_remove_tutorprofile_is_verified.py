from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_tutorprofile_price_per_hour"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tutorprofile",
            name="is_verified",
        ),
    ]
