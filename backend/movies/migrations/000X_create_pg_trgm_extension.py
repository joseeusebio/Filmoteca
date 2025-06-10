from django.db import migrations

class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("movies", "0006_movie_movie_title_5da1db_idx"),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            reverse_sql="DROP EXTENSION IF EXISTS pg_trgm;"
        )
    ]
