from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, Enum, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid
from datetime import datetime, timezone

Base = declarative_base()

# Enums
class AlertType(enum.Enum):
    missed_medication = "missed_medication"
    emergency = "emergency"

class ReferenceType(enum.Enum):
    medication = "medication"
    appointment = "appointment"
    event = "event"

# User and Roles
class User(Base):
    __tablename__ = 'user'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean, default=True)
    f6_uniquifier = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    roles = relationship('UserRole', back_populates='user', cascade='all, delete-orphan')
    senior_citizen = relationship('SeniorCitizen', uselist=False, back_populates='user', cascade='all, delete-orphan')
    caregiver = relationship('Caregiver', uselist=False, back_populates='user', cascade='all, delete-orphan')
    alerts = relationship('Alert', back_populates='recipient', cascade='all, delete-orphan')


class Role(Base):
    __tablename__ = 'role'
    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)

    users = relationship('UserRole', back_populates='role', cascade='all, delete-orphan')


class UserRole(Base):
    __tablename__ = 'userroles'
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.role_id', ondelete='CASCADE'), primary_key=True)

    user = relationship('User', back_populates='roles')
    role = relationship('Role', back_populates='users')


# SeniorCitizen and Caregiver
class SeniorCitizen(Base):
    __tablename__ = 'seniorcitizen'
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    font_size = Column(String)
    theme = Column(String)

    user = relationship('User', back_populates='senior_citizen')
    appointments = relationship('Appointment', back_populates='senior', cascade='all, delete-orphan')
    medications = relationship('Medication', back_populates='senior', cascade='all, delete-orphan')
    emergency_contacts = relationship('EmergencyContact', back_populates='senior', cascade='all, delete-orphan')
    caregiver_assignments = relationship('CaregiverAssignment', back_populates='senior', cascade='all, delete-orphan')
    event_attendance = relationship('EventAttendance', back_populates='senior', cascade='all, delete-orphan')


class Caregiver(Base):
    __tablename__ = 'caregiver'
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)

    user = relationship('User', back_populates='caregiver')
    assignments = relationship('CaregiverAssignment', back_populates='caregiver', cascade='all, delete-orphan')


class CaregiverAssignment(Base):
    __tablename__ = 'caregiver_assignment'
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey('caregiver.user_id', ondelete='CASCADE'), primary_key=True)
    senior_id = Column(UUID(as_uuid=True), ForeignKey('seniorcitizen.user_id', ondelete='CASCADE'), primary_key=True)

    caregiver = relationship('Caregiver', back_populates='assignments')
    senior = relationship('SeniorCitizen', back_populates='caregiver_assignments')


# Appointments and Medication
class Appointment(Base):
    __tablename__ = 'appointment'
    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    date_time = Column(DateTime)
    location = Column(String)
    senior_id = Column(UUID(as_uuid=True), ForeignKey('seniorcitizen.user_id', ondelete='CASCADE'))

    senior = relationship('SeniorCitizen', back_populates='appointments')


class Medication(Base):
    __tablename__ = 'medication'
    medication_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    dosage = Column(String)
    time = Column(DateTime)
    isTaken = Column(Boolean, default=False)
    senior_id = Column(UUID(as_uuid=True), ForeignKey('seniorcitizen.user_id', ondelete='CASCADE'))

    senior = relationship('SeniorCitizen', back_populates='medications')


# Emergency Contacts
class EmergencyContact(Base):
    __tablename__ = 'emergency_contact'
    contact_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    relation = Column(String)
    phone = Column(String)
    senior_id = Column(UUID(as_uuid=True), ForeignKey('seniorcitizen.user_id', ondelete='CASCADE'))

    senior = relationship('SeniorCitizen', back_populates='emergency_contacts')


# News & Preferences
class News(Base):
    __tablename__ = 'news'
    news_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    api_article_id = Column(String)
    title = Column(String)
    description = Column(Text)
    url = Column(String)
    source = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


# Events & Attendance
class ServiceProvider(Base):
    __tablename__ = 'service_provider'
    service_provider_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    events = relationship('Event', back_populates='service_provider', cascade='all, delete-orphan')


class Event(Base):
    __tablename__ = 'event'
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    date_time = Column(DateTime)
    location = Column(String)
    description = Column(Text)
    service_provider_id = Column(UUID(as_uuid=True), ForeignKey('service_provider.service_provider_id', ondelete='CASCADE'))

    service_provider = relationship('ServiceProvider', back_populates='events')
    attendance = relationship('EventAttendance', back_populates='event', cascade='all, delete-orphan')


class EventAttendance(Base):
    __tablename__ = 'event_attendance'
    senior_id = Column(UUID(as_uuid=True), ForeignKey('seniorcitizen.user_id', ondelete='CASCADE'), primary_key=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey('event.event_id', ondelete='CASCADE'), primary_key=True)

    senior = relationship('SeniorCitizen', back_populates='event_attendance')
    event = relationship('Event', back_populates='attendance')


class Alert(Base):
    __tablename__ = 'alert'
    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipient_user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id', ondelete='CASCADE'))
    alert_type = Column(Enum(AlertType))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    reference_type = Column(Enum(ReferenceType))
    reference_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    recipient = relationship('User', back_populates='alerts')