from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actistream', '0002_notice_index_together'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='notice',
            new_name='notice',
            old_fields=('user', 'read_at'),
        ),
    ]
