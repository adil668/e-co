from django.db import migrations, models
import hashlib


def populate_content_hashes(apps, schema_editor):
    KnowledgeSource = apps.get_model("chatbot", "KnowledgeSource")
    seen_hashes = set()
    for source in KnowledgeSource.objects.all():
        base = source.content or f"knowledge-source-{source.pk}"
        digest = hashlib.sha256(base.encode("utf-8")).hexdigest()
        if digest in seen_hashes:
            digest = hashlib.sha256(f"{base}:{source.pk}".encode("utf-8")).hexdigest()
        seen_hashes.add(digest)
        source.content_hash = digest
        source.save(update_fields=["content_hash"])


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="knowledgesource",
            name="content_hash",
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.AddField(
            model_name="knowledgesource",
            name="original_filename",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="knowledgesource",
            name="file_size",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="knowledgesource",
            name="chunk_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(populate_content_hashes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="knowledgesource",
            name="content_hash",
            field=models.CharField(blank=True, db_index=True, editable=False, max_length=64, unique=True),
        ),
    ]
