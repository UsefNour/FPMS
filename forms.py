from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, DateField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class FighterProfileForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=60)])
    height = FloatField('Height (cm)', validators=[DataRequired(), NumberRange(min=150, max=220)])
    walk_around_weight = FloatField('Walk-Around Weight (lbs)', validators=[DataRequired(), NumberRange(min=100, max=400)])
    weight_class = SelectField('Weight Class', choices=[
        ('Flyweight', 'Flyweight (125 lbs)'),
        ('Bantamweight', 'Bantamweight (135 lbs)'),
        ('Featherweight', 'Featherweight (145 lbs)'),
        ('Lightweight', 'Lightweight (155 lbs)'),
        ('Welterweight', 'Welterweight (170 lbs)'),
        ('Middleweight', 'Middleweight (185 lbs)'),
        ('Light Heavyweight', 'Light Heavyweight (205 lbs)'),
        ('Heavyweight', 'Heavyweight (265 lbs)')
    ], validators=[DataRequired()])
    fight_date = DateField('Fight Date', validators=[DataRequired()])
    training_availability = IntegerField('Training Days/Week', validators=[DataRequired(), NumberRange(min=1, max=7)])
    se_angle = SelectField('Preferred Fighting Style', choices=[
        ('Striking', 'Striking'),
        ('Grappling', 'Grappling'),
        ('Mixed', 'Mixed'),
        ('Kickboxing', 'Kickboxing'),
        ('Boxing', 'Boxing'),
        ('Wrestling', 'Wrestling'),
        ('BJJ', 'Brazilian Jiu-Jitsu'),
        ('Muay Thai', 'Muay Thai'),
        ('Krav Maga', 'Krav Maga')
    ], validators=[DataRequired()])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Save Profile')

class CampPlanForm(FlaskForm):
    fight_type = SelectField('Fight Type', choices=[
        ('3 Rounds', '3 Rounds'),
        ('5 Rounds', '5 Rounds')
    ], validators=[DataRequired()])
    opponent_name = StringField('Opponent Name (Optional)')
    opponent_strengths = TextAreaField('Opponent Strengths', validators=[DataRequired()], 
        render_kw={"placeholder": "e.g., Strong wrestling, knockout power, good cardio, pressure fighter..."})
    opponent_weaknesses = TextAreaField('Opponent Weaknesses', validators=[DataRequired()],
        render_kw={"placeholder": "e.g., Weak chin, poor cardio, bad takedown defense, slow starter..."})
    submit = SubmitField('Generate Camp Plan')

class GamePlanForm(FlaskForm):
    fight_rounds = SelectField('Number of Rounds', choices=[
        ('3', '3 Rounds'),
        ('5', '5 Rounds')
    ], validators=[DataRequired()])
    opponent_strengths = TextAreaField('Opponent Strengths', validators=[DataRequired()])
    opponent_weaknesses = TextAreaField('Opponent Weaknesses', validators=[DataRequired()])
    submit = SubmitField('Generate Game Plan')

class WeightLogForm(FlaskForm):
    weight = FloatField('Weight (lbs)', validators=[DataRequired(), NumberRange(min=100, max=400)])
    submit = SubmitField('Log Weight')

class FriendRequestForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Send Friend Request')


class FighterForm(FlaskForm):
    name = StringField('Fighter Name', validators=[DataRequired(), Length(min=1, max=150)])
    nickname = StringField('Nickname (optional)', validators=[Length(max=100)])
    weight_class = SelectField('Weight Class', choices=[
        ('Flyweight', 'Flyweight (125 lbs)'),
        ('Bantamweight', 'Bantamweight (135 lbs)'),
        ('Featherweight', 'Featherweight (145 lbs)'),
        ('Lightweight', 'Lightweight (155 lbs)'),
        ('Welterweight', 'Welterweight (170 lbs)'),
        ('Middleweight', 'Middleweight (185 lbs)'),
        ('Light Heavyweight', 'Light Heavyweight (205 lbs)'),
        ('Heavyweight', 'Heavyweight (265 lbs)')
    ], validators=[DataRequired()])
    record = StringField('Record (e.g., 15-5-0)', validators=[Length(max=20)])
    fighting_style = SelectField('Fighting Style', choices=[
        ('Striking', 'Striking'),
        ('Grappling', 'Grappling'),
        ('Mixed', 'Mixed'),
        ('Kickboxing', 'Kickboxing'),
        ('Boxing', 'Boxing'),
        ('Wrestling', 'Wrestling'),
        ('BJJ', 'Brazilian Jiu-Jitsu'),
        ('Muay Thai', 'Muay Thai'),
        ('Krav Maga', 'Krav Maga'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    strengths = TextAreaField('Strengths (comma-separated)', validators=[Length(max=500)])
    weaknesses = TextAreaField('Weaknesses (comma-separated)', validators=[Length(max=500)])
    notable_fights = TextAreaField('Notable Fights (wins/losses)', validators=[Length(max=1000)])
    submit = SubmitField('Add Fighter')

class SparringProfileForm(FlaskForm):
    location = StringField('Location (City, State/Country)', validators=[DataRequired(), Length(max=255)])
    latitude = FloatField('Latitude', validators=[])  # Optional - auto-filled by geocoding
    longitude = FloatField('Longitude', validators=[])  # Optional - auto-filled by geocoding
    skill_level = SelectField('Skill Level', choices=[
        ('Beginner', 'Beginner (0-1 years experience)'),
        ('Intermediate', 'Intermediate (1-3 years experience)'),
        ('Advanced', 'Advanced (3-5 years experience)'),
        ('Expert', 'Expert (5+ years experience)')
    ], validators=[DataRequired()])
    preferred_styles = SelectField('Preferred Fighting Styles', choices=[
        ('Striking', 'Striking'),
        ('Grappling', 'Grappling'),
        ('Mixed', 'Mixed'),
        ('Kickboxing', 'Kickboxing'),
        ('Boxing', 'Boxing'),
        ('Wrestling', 'Wrestling'),
        ('BJJ', 'Brazilian Jiu-Jitsu'),
        ('Muay Thai', 'Muay Thai'),
        ('Krav Maga', 'Krav Maga')
    ], validators=[DataRequired()])
    availability = TextAreaField('Availability (e.g., Mon-Fri 6-8PM, Sat 10AM-12PM)', validators=[DataRequired()])
    max_distance = IntegerField('Max Distance for Matches (miles)', validators=[DataRequired(), NumberRange(min=1, max=500)], default=50)
    self_skill_rating = IntegerField('Self Skill Rating (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)], default=5)
    submit = SubmitField('Save Sparring Profile')

class SparringSessionForm(FlaskForm):
    partner_username = StringField('Partner Username', validators=[DataRequired()])
    session_date = DateField('Session Date', validators=[DataRequired()])
    session_time = StringField('Session Time (e.g., 2:00 PM)', validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=30, max=180)], default=60)
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    notes = TextAreaField('Notes (optional)', validators=[Length(max=1000)])
    submit = SubmitField('Request Sparring Session')

class SkillAssessmentForm(FlaskForm):
    skill_rating = IntegerField('Skill Rating (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    assessment_notes = TextAreaField('Assessment Notes', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit Assessment')


class CreateEventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Event Description', validators=[Length(max=2000)],
        render_kw={"placeholder": "Describe your event, rules, format, etc."})
    event_type = SelectField('Event Type', choices=[
        ('Amateur', 'Amateur'),
        ('Semi-Pro', 'Semi-Pro'),
        ('Professional', 'Professional'),
        ('Open', 'Open (All Levels)')
    ], validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    event_time = StringField('Event Time', validators=[DataRequired()],
        render_kw={"placeholder": "e.g., 6:00 PM"})
    registration_deadline = DateField('Registration Deadline', validators=[Optional()])
    venue_name = StringField('Venue Name', validators=[Length(max=200)],
        render_kw={"placeholder": "e.g., Downtown Athletic Center"})
    location = StringField('Full Address', validators=[DataRequired(), Length(max=255)],
        render_kw={"placeholder": "e.g., 123 Main St, Los Angeles, CA"})
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Province', validators=[Length(max=100)])
    country = SelectField('Country', choices=[
        ('USA', 'United States'),
        ('Canada', 'Canada'),
        ('UK', 'United Kingdom'),
        ('Australia', 'Australia'),
        ('Brazil', 'Brazil'),
        ('Mexico', 'Mexico'),
        ('Other', 'Other')
    ], default='USA')
    weight_classes = SelectMultipleField('Weight Classes Available', choices=[
        ('Strawweight', 'Strawweight (115 lbs)'),
        ('Flyweight', 'Flyweight (125 lbs)'),
        ('Bantamweight', 'Bantamweight (135 lbs)'),
        ('Featherweight', 'Featherweight (145 lbs)'),
        ('Lightweight', 'Lightweight (155 lbs)'),
        ('Welterweight', 'Welterweight (170 lbs)'),
        ('Middleweight', 'Middleweight (185 lbs)'),
        ('Light Heavyweight', 'Light Heavyweight (205 lbs)'),
        ('Heavyweight', 'Heavyweight (265 lbs)'),
        ('Open Weight', 'Open Weight')
    ], validators=[DataRequired()])
    experience_levels = SelectMultipleField('Experience Levels', choices=[
        ('Beginner', 'Beginner (0-1 fights)'),
        ('Intermediate', 'Intermediate (2-5 fights)'),
        ('Advanced', 'Advanced (6-10 fights)'),
        ('Expert', 'Expert (10+ fights)')
    ], validators=[DataRequired()])
    rules = SelectField('Competition Rules', choices=[
        ('MMA', 'MMA (Mixed Martial Arts)'),
        ('Boxing', 'Boxing'),
        ('Kickboxing', 'Kickboxing'),
        ('Muay Thai', 'Muay Thai'),
        ('BJJ', 'Brazilian Jiu-Jitsu'),
        ('Wrestling', 'Wrestling'),
        ('Grappling', 'Submission Grappling'),
        ('Karate', 'Karate'),
        ('Taekwondo', 'Taekwondo'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    entry_fee = FloatField('Entry Fee ($)', validators=[Optional(), NumberRange(min=0, max=10000)], default=0)
    prize_info = TextAreaField('Prize Information', validators=[Length(max=500)],
        render_kw={"placeholder": "e.g., $500 cash prize for winners, medals for top 3"})
    max_participants = IntegerField('Max Participants', validators=[Optional(), NumberRange(min=2, max=1000)])
    contact_email = StringField('Contact Email', validators=[Optional(), Email(), Length(max=150)])
    contact_phone = StringField('Contact Phone', validators=[Length(max=50)])
    website = StringField('Event Website', validators=[Length(max=255)],
        render_kw={"placeholder": "https://..."})
    submit = SubmitField('Create Event')


class EventFilterForm(FlaskForm):
    city = StringField('City', validators=[Length(max=100)])
    state = StringField('State', validators=[Length(max=100)])
    weight_class = SelectField('Weight Class', choices=[
        ('', 'All Weight Classes'),
        ('Strawweight', 'Strawweight (115 lbs)'),
        ('Flyweight', 'Flyweight (125 lbs)'),
        ('Bantamweight', 'Bantamweight (135 lbs)'),
        ('Featherweight', 'Featherweight (145 lbs)'),
        ('Lightweight', 'Lightweight (155 lbs)'),
        ('Welterweight', 'Welterweight (170 lbs)'),
        ('Middleweight', 'Middleweight (185 lbs)'),
        ('Light Heavyweight', 'Light Heavyweight (205 lbs)'),
        ('Heavyweight', 'Heavyweight (265 lbs)'),
        ('Open Weight', 'Open Weight')
    ])
    experience_level = SelectField('Experience Level', choices=[
        ('', 'All Levels'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert')
    ])
    event_type = SelectField('Event Type', choices=[
        ('', 'All Types'),
        ('Amateur', 'Amateur'),
        ('Semi-Pro', 'Semi-Pro'),
        ('Professional', 'Professional'),
        ('Open', 'Open')
    ])
    rules = SelectField('Competition Rules', choices=[
        ('', 'All Rules'),
        ('MMA', 'MMA'),
        ('Boxing', 'Boxing'),
        ('Kickboxing', 'Kickboxing'),
        ('Muay Thai', 'Muay Thai'),
        ('BJJ', 'BJJ'),
        ('Wrestling', 'Wrestling'),
        ('Grappling', 'Grappling')
    ])
    submit = SubmitField('Filter')


class EventInterestForm(FlaskForm):
    weight_class = SelectField('Weight Class', validators=[DataRequired()])
    notes = TextAreaField('Notes (Optional)', validators=[Length(max=500)],
        render_kw={"placeholder": "Any additional information for the organizer..."})
    submit = SubmitField('Express Interest')
