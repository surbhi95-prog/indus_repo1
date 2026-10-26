from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hrms", "0012_shift_unique_active_shift_name_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="is_late",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="attendance",
            name="late_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
