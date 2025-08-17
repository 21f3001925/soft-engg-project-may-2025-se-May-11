from flask_security import UserMixin, RoleMixin
import enum
import secrets
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from extensions import db


class AlertType(enum.Enum):
    missed_medication = "missed_medication"
    emergency = "emergency"


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.String(36), db.ForeignKey("user.user_id")),
    db.Column("role_id", db.String(36), db.ForeignKey("role.id")),
)


class ReferenceType(enum.Enum):
    medication = "medication"
    appointment = "appointment"
    event = "event"


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship("User", secondary=roles_users, back_populates="roles")


class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        default=lambda: secrets.token_urlsafe(32),
    )
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    roles = db.relationship("Role", secondary=roles_users, back_populates="users")
    senior_citizen = db.relationship(
        "SeniorCitizen",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    caregiver = db.relationship(
        "Caregiver", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    service_provider = db.relationship(
        "ServiceProvider",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    alerts = db.relationship(
        "Alert", back_populates="recipient", cascade="all, delete-orphan"
    )
    name = db.Column(db.String)

    avatar_url = db.Column(db.String)
    avatar_url = db.Column(db.String)

    emergency_contacts = db.relationship(
        "EmergencyContact", back_populates="senior", cascade="all, delete-orphan"
    )


class SeniorCitizen(db.Model):
    __tablename__ = "seniorcitizen"
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    age = db.Column(db.Integer)
    font_size = db.Column(db.String, default="small")
    theme = db.Column(db.String, default="light")
    news_categories = db.Column(db.String)  # Comma-separated news categories
    topics_liked = db.Column(db.Integer, default=0)
    comments_posted = db.Column(db.Integer, default=0)
    appointments_missed = db.Column(db.Integer, default=0)
    medications_missed = db.Column(db.Integer, default=0)
    total_screentime = db.Column(db.Integer, default=0)

    user = relationship("User", back_populates="senior_citizen")
    appointments = relationship(
        "Appointment", back_populates="senior", cascade="all, delete-orphan"
    )
    medications = relationship(
        "Medication", back_populates="senior", cascade="all, delete-orphan"
    )

    caregiver_assignments = relationship(
        "CaregiverAssignment", back_populates="senior", cascade="all, delete-orphan"
    )
    event_attendance = relationship(
        "EventAttendance", back_populates="senior", cascade="all, delete-orphan"
    )


class Caregiver(db.Model):
    __tablename__ = "caregiver"
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )

    user = relationship("User", back_populates="caregiver")
    assignments = relationship(
        "CaregiverAssignment", back_populates="caregiver", cascade="all, delete-orphan"
    )


class CaregiverAssignment(db.Model):
    __tablename__ = "caregiver_assignment"
    caregiver_id = db.Column(
        db.String(36),
        db.ForeignKey("caregiver.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    senior_id = db.Column(
        db.String(36),
        db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE"),
        primary_key=True,
    )

    caregiver = relationship("Caregiver", back_populates="assignments")
    senior = relationship("SeniorCitizen", back_populates="caregiver_assignments")


class Appointment(db.Model):
    __tablename__ = "appointment"
    appointment_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title = db.Column(db.String)
    date_time = db.Column(db.DateTime)
    location = db.Column(db.String)
    reminder_time = db.Column(db.DateTime, nullable=True)
    senior_id = db.Column(
        db.String(36), db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE")
    )
    reminder_task_id = db.Column(db.String(36), nullable=True)
    status = db.Column(db.String(50), default="Scheduled", nullable=False)

    senior = relationship("SeniorCitizen", back_populates="appointments")


class Medication(db.Model):
    __tablename__ = "medication"
    medication_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String)
    dosage = db.Column(db.String)
    time = db.Column(db.DateTime)
    isTaken = db.Column(db.Boolean, default=False)
    missed_counted = db.Column(db.Boolean, default=False)
    senior_id = db.Column(
        db.String(36), db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE")
    )

    reminder_task_id = db.Column(db.String(36), nullable=True)

    senior = relationship("SeniorCitizen", back_populates="medications")


class EmergencyContact(db.Model):
    __tablename__ = "emergency_contact"
    contact_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String)
    relation = db.Column(db.String)
    phone = db.Column(db.String)

    email = db.Column(db.String)

    senior_id = db.Column(
        db.String(36), db.ForeignKey("user.user_id", ondelete="CASCADE")
    )

    senior = relationship("User", back_populates="emergency_contacts")


class Feedback(db.Model):
    __tablename__ = "news"
    news_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    api_article_id = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    url = db.Column(db.String)
    source = db.Column(db.String)
    category = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class ServiceProvider(db.Model):
    __tablename__ = "service_provider"
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    name = db.Column(db.String, nullable=True)
    contact_email = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String)
    services_offered = db.Column(db.String)
    user = relationship("User", back_populates="service_provider")
    events = relationship(
        "Event", back_populates="service_provider", cascade="all, delete-orphan"
    )


class Event(db.Model):
    __tablename__ = "event"
    event_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String)
    date_time = db.Column(db.DateTime(timezone=True))
    location = db.Column(db.String)
    description = db.Column(db.Text)
    service_provider_id = db.Column(
        db.String(36),
        db.ForeignKey("service_provider.user_id", ondelete="CASCADE"),
    )

    service_provider = relationship("ServiceProvider", back_populates="events")
    attendance = relationship(
        "EventAttendance", back_populates="event", cascade="all, delete-orphan"
    )


class EventAttendance(db.Model):
    __tablename__ = "event_attendance"
    senior_id = db.Column(
        db.String(36),
        db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    event_id = db.Column(
        db.String(36),
        db.ForeignKey("event.event_id", ondelete="CASCADE"),
        primary_key=True,
    )
    # --- ADD THIS LINE ---
    reminder_task_id = db.Column(
        db.String(36), nullable=True
    )  # To store the Celery task ID

    senior = relationship("SeniorCitizen", back_populates="event_attendance")
    event = relationship("Event", back_populates="attendance")


class Alert(db.Model):
    __tablename__ = "alert"
    alert_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    recipient_user_id = db.Column(
        db.String(36), db.ForeignKey("user.user_id", ondelete="CASCADE")
    )
    alert_type = db.Column(db.Enum(AlertType))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    reference_type = db.Column(db.Enum(ReferenceType))
    reference_id = db.Column(db.String(36))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    recipient = relationship("User", back_populates="alerts")


class Report(db.Model):
    __tablename__ = "report"
    report_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    original_filename = db.Column(db.String, nullable=False)
    stored_filename = db.Column(db.String, nullable=False, unique=True)
    extracted_text = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    status = db.Column(db.String, nullable=False, default="processing")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    senior_id = db.Column(
        db.String(36), db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE")
    )

    senior = relationship("SeniorCitizen", back_populates="reports")


# Add the back-populates for reports to the SeniorCitizen model
SeniorCitizen.reports = relationship(
    "Report", back_populates="senior", cascade="all, delete-orphan"
)
