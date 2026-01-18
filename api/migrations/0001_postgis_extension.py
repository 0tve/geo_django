from django.contrib.postgres import operations as pg_operations
from django.db import migrations


class Migration(migrations.Migration):
    operations = [pg_operations.CreateExtension('postgis')]
