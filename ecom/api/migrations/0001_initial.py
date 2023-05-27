from django.db import migrations
from api.user.models import CustomUser

class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name='Apurva', email='jaiswal.apurva.aj011@gmail.com', is_staff=True, is_superuser=True, phone='9898989898', gender='Male')    # Creating very first user to login
        user.set_password("1234567890")
        user.save()
    
    dependencies = []
    
    operations = [
        migrations.RunPython(seed_data),
    ]