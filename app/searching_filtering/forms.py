from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from app import df


class SearchForm(FlaskForm):
    # The keywords field can be empty, therefor no validator needed (if empty return all result)
    keywords = StringField('Keywords', render_kw={"placeholder": "Search BetterPath"})
    search = SubmitField('Search')
    saved_courses = SubmitField('SavedCourses')
    log_out = SubmitField('Logout')

# reuse the form in the orginal educationpath repo
class FilterForm(FlaskForm):
    divisions = [('Any','Any')] + sorted([
        (t,t) for t in set(df.Division.values)
    ])

    departments = [('Any','Any')] + sorted([
        (t,t) for t in set(df.Department.values)
    ])

    campus = [('Any','Any')] + sorted([
        (t,t) for t in set(df.Campus.values)
    ])

    year_choices = [
        (t,t) for t in set(df['Course Level'].values)
    ]
            
    top = [
        ('10','10'),
        ('25','25'),
        ('50','50')
    ]
    select = SelectField('Course Year:', choices=year_choices)
    top = SelectField('',choices=top)
    divisions = SelectField('Division:', choices=divisions)
    departments = SelectField('Department:', choices=departments)
    campuses = SelectField('Campus:', choices=campus)
    search = StringField('Search Terms:')
