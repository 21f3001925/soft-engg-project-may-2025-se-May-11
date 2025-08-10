import uuid
import random
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

from app import create_app  # Import your Flask app factory
from extensions import db
from models import User, Role, SeniorCitizen, Caregiver, CaregiverAssignment

app = create_app()

with app.app_context():
    # Step 1: Ensure roles exist
    role_names = ["admin", "caregiver", "senior_citizen"]
    role_objects = {}

    for role_name in role_names:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(
                id=str(uuid.uuid4()),
                name=role_name,
                description=f"Role for {role_name}",
            )
            db.session.add(role)
        role_objects[role_name] = role

    db.session.commit()

    # Step 2: Create dummy users
    users = []
    seniors = []
    caregivers = []

    for i in range(10):
        # Assign roles in a round-robin fashion
        role_name = role_names[i % len(role_names)]
        user = User(
            user_id=str(uuid.uuid4()),
            username=f"user{i}",
            email=f"user{i}@example.com",
            password=generate_password_hash("password123"),
            phone_number=f"+91123456{i:03}",
            active=True,
            name=f"User {i}",
            created_at=datetime.now(timezone.utc),
        )
        user.roles.append(role_objects[role_name])
        db.session.add(user)
        db.session.flush()  # Get the ID immediately

        if role_name == "senior_citizen":
            senior = SeniorCitizen(
                user_id=user.user_id,
                age=random.randint(60, 85),
                font_size=random.choice(["small", "medium", "large"]),
                theme=random.choice(["light", "dark"]),
                news_categories="health,finance,technology",
            )
            db.session.add(senior)
            seniors.append(senior)

        elif role_name == "caregiver":
            caregiver = Caregiver(user_id=user.user_id)
            db.session.add(caregiver)
            caregivers.append(caregiver)

        users.append(user)

    db.session.commit()

    # Step 3: Assign seniors to caregivers
    if seniors and caregivers:
        for caregiver in caregivers:
            assigned_seniors = random.sample(seniors, k=min(2, len(seniors)))
            for senior in assigned_seniors:
                assignment = CaregiverAssignment(
                    caregiver_id=caregiver.user_id, senior_id=senior.user_id
                )
                db.session.add(assignment)

    db.session.commit()

    print("✅ Database populated with:")
    print(f" - {len(users)} users")
    print(f" - {len(seniors)} senior citizens")
    print(f" - {len(caregivers)} caregivers")
    print(" - Seniors assigned to caregivers")
