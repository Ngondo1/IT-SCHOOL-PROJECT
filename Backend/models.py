from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Messages table
class Messages(db.Model):
    __tablename__ = 'messages'
    messageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shortCode = db.Column(db.Integer)
    SendTime = db.Column(db.TIMESTAMP)
    phoneNo = db.Column(db.String(30))
    message = db.Column(db.Text)
    messageType = db.Column(db.Enum('user', 'System'))

# Users table
class Users(db.Model):
    __tablename__ = 'users'
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RegistrationTime = db.Column(db.Date, default=None)
    Name = db.Column(db.String(100), default=None)
    Age = db.Column(db.Integer, default=None)
    phoneNo = db.Column(db.String(30), default=None)
    Gender = db.Column(db.String(50), default=None)
    County = db.Column(db.String(100), default=None)
    Town = db.Column(db.String(100), default=None)
    LevelOfEducation = db.Column(db.String(100), default=None)
    Profession = db.Column(db.String(100), default=None)
    MaritalStatus = db.Column(db.String(50), default=None)
    Religion = db.Column(db.String(100), default=None)
    Ethnicity = db.Column(db.String(100), default=None)
    Description = db.Column(db.Text)

# Matches Request table
class MatchesRequest(db.Model):
    __tablename__ = 'matches_request'
    matchID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requester_phoneNo = db.Column(db.String(30))
    match_phoneNo = db.Column(db.String(30))
    status = db.Column(db.Enum('pending', 'approved', 'declined'), default='pending')
    request_time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

# Jobs table
class Jobs(db.Model):
    __tablename__ = 'jobs'
    jobID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employerID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    jobTitle = db.Column(db.String(100))
    jobDescription = db.Column(db.Text)
    jobLocation = db.Column(db.String(150))
    salaryRange = db.Column(db.String(50))
    employmentType = db.Column(db.Enum('full-time', 'part-time', 'casual'))
    postDate = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    status = db.Column(db.Enum('active', 'filled', 'expired'), default='active')

# Applications table
class Applications(db.Model):
    __tablename__ = 'applications'
    applicationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jobID = db.Column(db.Integer, db.ForeignKey('jobs.jobID'))
    applicantID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    applicationDate = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    status = db.Column(db.Enum('pending', 'shortlisted', 'rejected', 'hired'), default='pending')

# Ratings table
class Ratings(db.Model):
    __tablename__ = 'ratings'
    ratingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    raterID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    rateeID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    rating = db.Column(db.Integer)  # scale of 1–5
    comment = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
class Employers(db.Model):
    __tablename__ = 'employers'
    employerID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True)
    companyName = db.Column(db.String(150), nullable=False)
    businessTypeID = db.Column(db.Integer, db.ForeignKey('business_types.id'))
    registrationNumber = db.Column(db.String(100), unique=True)
    companyEmail = db.Column(db.String(150), unique=True)
    companyPhone = db.Column(db.String(30))
    companyLocation = db.Column(db.String(200))
    logoUrl = db.Column(db.String(255))
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Employees(db.Model):
    __tablename__ = 'employees'
    employeeID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True)
    skills = db.Column(db.Text)
    yearsOfExperience = db.Column(db.Integer)
    expectedSalary = db.Column(db.String(50))
    availability = db.Column(db.Enum('immediately', '1 week', '1 month'))
    preferredJobTypes = db.Column(db.String(150))  # e.g. "full-time, part-time"
    portfolioUrl = db.Column(db.String(255))  # Optional
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())