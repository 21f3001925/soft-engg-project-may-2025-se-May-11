from models import Role, db


def add_core_roles():
    session = db.session
    core_roles = [
        {"name": "senior_citizen", "description": "Senior Citizen"},
        {"name": "caregiver", "description": "Caregiver"},
        {"name": "service_provider", "description": "Service Provider"},
        # Add more roles as needed
    ]
    for role_data in core_roles:
        if not session.query(Role).filter_by(name=role_data["name"]).first():
            role = Role(name=role_data["name"], description=role_data["description"])
            session.add(role)
    session.commit()
