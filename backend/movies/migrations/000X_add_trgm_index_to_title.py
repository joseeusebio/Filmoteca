from django.db import migrations

class Migration(migrations.Migration):
    atomic = True

    dependencies = [
        ("movies", "000X_create_pg_trgm_extension"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE INDEX IF NOT EXISTS movie_title_trgm_idx
                ON movie USING GIN (title gin_trgm_ops);
            """,
            reverse_sql="DROP INDEX IF EXISTS movie_title_trgm_idx;"
        )
    ]
