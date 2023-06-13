# Generated by Django 4.2.1 on 2023-06-13 21:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("l1o", "0008_alter_match_e2e_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="division",
            name="number_of_promoted_teams",
            field=models.IntegerField(
                choices=[(10, "Ten"), (12, "Twelve")], default=12
            ),
            preserve_default=False,
        ),
    ]