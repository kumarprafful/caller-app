from faker import Faker
from users.models import User
from contacts.models import Contact

fake = Faker('en_IN')

for _ in range(1000):
    User.objects.create_user(
        email=fake.email(),
        full_name=fake.name(),
        mobile=fake.phone_number(),
        password="test@123"
    )


for i in range(1000):
    Contact.objects.create(
        full_name=fake.name(),
        mobile=fake.phone_number()
    )

import random

contacts = Contact.objects.all()

users = User.objects.all()
for user in users:
    random_contacts = random.sample(list(contacts), random.randint(5, 50))
    for r in random_contacts:
        user.contacts.add(r)
