useful shell commands for testing:

from users.models import User, Company

user = User.objects.create(username="testuser", email="test@example.com", is_company=True)
user.set_password("testpassword")
user.save()
user.is_active = True

checks:
    user.id
    User.objects.filter(email="test@example.com").exists()
    User.objects.all()
    print(user.is_active)

Login:
    user = authenticate(username="testuser", password="testpassword")
print(user)


company = Company.objects.create(user=user, field="Electricity")
Company.objects.all()