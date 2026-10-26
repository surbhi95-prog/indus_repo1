from django.db import migrations, models


def _rename_shift_type(apps, schema_editor, old_value, new_value):
    Shift = apps.get_model("hrms", "Shift")
    database = schema_editor.connection.alias
    old_shifts = Shift.objects.using(database).filter(
        shift_type__iexact=old_value,
    )

    # The active-shift uniqueness constraint includes shift_type. Check for
    # collisions before updating so the migration never merges or deletes rows.
    for shift in old_shifts.filter(is_deleted=False).iterator():
        collision_exists = (
            Shift.objects.using(database)
            .filter(
                company_id=shift.company_id,
                plant_id=shift.plant_id,
                name=shift.name,
                shift_type__iexact=new_value,
                is_deleted=False,
            )
            .exclude(pk=shift.pk)
            .exists()
        )
        if collision_exists:
            raise RuntimeError(
                "Cannot rename shift type values safely: an active shift "
                f"already conflicts with {new_value!r} for shift {shift.pk}. "
                "Resolve the duplicate shift name before retrying the migration."
            )

    old_shifts.update(shift_type=new_value)


def forwards(apps, schema_editor):
    _rename_shift_type(apps, schema_editor, "basic", "general")


def backwards(apps, schema_editor):
    _rename_shift_type(apps, schema_editor, "general", "basic")


class Migration(migrations.Migration):
    dependencies = [
        ("hrms", "0018_rosterassignment_source"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name="shift",
            name="shift_type",
            field=models.CharField(
                choices=[("general", "General"), ("contract", "Contract")],
                max_length=20,
            ),
        ),
    ]
