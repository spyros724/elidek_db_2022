from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, IntegerRangeField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class ProgramForm(FlaskForm):
    program_name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])

    program_address = StringField(label = "Address", validators = [DataRequired(message = "Address is a required field.")])

    submit = SubmitField("Create")


class ProjectForm(FlaskForm):
    title = StringField(label = "Title", validators = [Optional()])

    summary = StringField(label = "Summary", validators = [Optional()])

    funds = IntegerField(label = "Funds", validators = [Optional()])

    starting_date = DateField(label = "Starting Date", validators = [Optional()])

    ending_date = DateField(label = "Ending Date", validators = [Optional()])

    duration = IntegerField(label = "Duration", validators = [Optional()])

    executive_name = StringField(label = "Executive Name", validators = [Optional()])

    executive_surname = StringField(label = "Executive Surname", validators = [Optional()])

    submit = SubmitField("Submit")


class ProjectCreateForm(FlaskForm):
    project_id = IntegerField(label = "Id", validators = [DataRequired(message = "This is a required field.")])

    title = StringField(label = "Title", validators = [DataRequired(message = "This is a required field.")])

    summary = StringField(label = "Summary", validators = [DataRequired(message = "This is a required field.")])

    funds = IntegerField(label = "Funds", validators = [DataRequired(message = "This is a required field.")])

    starting_date = DateField(label = "Starting Date", validators = [DataRequired(message = "This is a required field.")])

    ending_date = DateField(label = "Ending Date", validators = [DataRequired(message = "This is a required field.")])

    executive_id = StringField(label = "Executive id", validators = [DataRequired(message = "This is a required field.")])

    program_id = StringField(label = "Program id", validators = [DataRequired(message = "This is a required field.")])

    organization_id = StringField(label = "Organization id", validators = [DataRequired(message = "This is a required field.")])

    researcher_id = StringField(label = "Researcher id", validators = [DataRequired(message = "This is a required field.")])

    deliverables = IntegerField(label = "Deliverables", validators = [DataRequired(message = "This is a required field.")])

    submit = SubmitField("Submit")


class ResearcherForm(FlaskForm):
    researcher_id = IntegerField(label = "Id", validators = [Optional()])

    name = StringField(label = "Researcher's Name", validators = [Optional()])

    surname = StringField(label = "Researcher's Surname", validators = [Optional()])

    gender = StringField(label = "Researcher's Gender", validators = [Optional()])

    birth_date = DateField(label = "Birth Date", validators = [Optional()])

    organization_id = IntegerField(label = "Org. Id", validators = [Optional()])

    recruitment_date = DateField(label = "Recruitment Date", validators = [Optional()])

    submit = SubmitField("Submit")


class ResearcherCreateForm(FlaskForm):
    researcher_id = IntegerField(label = "Id", validators = [Optional()])

    name = StringField(label = "Researcher's Name", validators = [DataRequired(message = "This is a required field.")])

    surname = StringField(label = "Researcher's Surname", validators = [DataRequired(message = "This is a required field.")])

    gender = StringField(label = "Researcher's Gender", validators = [DataRequired(message = "This is a required field.")])

    birth_date = DateField(label = "Birth Date", validators = [DataRequired(message = "This is a required field.")])

    organization_id = IntegerField(label = "Org. Id", validators = [DataRequired(message = "This is a required field.")])

    recruitment_date = DateField(label = "Recruitment Date", validators = [DataRequired(message = "This is a required field.")])

    submit = SubmitField("Submit")


class FieldForm(FlaskForm):
    field_id = IntegerField(label = "Id", validators = [Optional()])

    field_name = StringField(label = "Field Name", validators = [DataRequired(message = "Field Name is a required field.")])

    submit = SubmitField("Submit")


class ExecutiveForm(FlaskForm):
    executive_id = IntegerField(label = "Id", validators = [Optional()])

    executive_name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])

    executive_surname = StringField(label = "Surname", validators = [DataRequired(message = "Surname is a required field.")])

    submit = SubmitField("Submit")


class Refers_ToForm(FlaskForm):
    project_id = IntegerField(label = "Project Id", validators = [Optional()])

    field_id = IntegerField(label = "Field Id", validators = [DataRequired(message = "id is a required field.")])

    submit = SubmitField("Submit")

class UniversityForm(FlaskForm):
    university_id = IntegerField(label = "University Id", validators = [DataRequired(message = "id is a required field.")])

    organization_id = IntegerField(label = "Organization Id", validators = [DataRequired(message = "id is a required field.")])

    ministry_budget = IntegerField(label = "Ministry Budget", validators = [DataRequired(message = "Budget is a required field.")])

    submit = SubmitField("Submit")


class CompanyForm(FlaskForm):
    company_id = IntegerField(label = "Company Id", validators = [DataRequired(message = "id is a required field.")])

    organization_id = IntegerField(label = "Organization Id", validators = [DataRequired(message = "id is a required field.")])

    company_budget = IntegerField(label = "Company Budget", validators = [DataRequired(message = "Budget is a required field.")])

    submit = SubmitField("Submit")

class Research_CenterForm(FlaskForm):
    research_center_id = IntegerField(label = "Research Center Id", validators = [DataRequired(message = "id is a required field.")])

    organization_id = IntegerField(label = "Organization Id", validators = [DataRequired(message = "id is a required field.")])

    center_budget = IntegerField(label = "Company Budget", validators = [DataRequired(message = "Budget is a required field.")])

    ministry_budget = IntegerField(label = "Ministry Budget", validators = [DataRequired(message = "Budget is a required field.")])

    submit = SubmitField("Submit")


class Organization_PhoneForm(FlaskForm):
    Organization_id = IntegerField(label = "Organization Id", validators = [DataRequired(message = "id is a required field.")])

    phone_number = IntegerField(label = "Phone Number", validators = [DataRequired(message = "Phone Number is a required field.")])

    submit = SubmitField("Submit")

class OrganizationForm(FlaskForm):
    organization_id = IntegerField(label = "Id", validators = [Optional()])

    acronym = StringField(label = "Acronym", validators = [DataRequired(message = "This is a required field.")])

    name = StringField(label = "Name", validators = [DataRequired(message = "This is a required field.")])

    postal_code = StringField(label = "Postal Code", validators = [DataRequired(message = "This is a required field.")])

    street = StringField(label = "Street", validators = [DataRequired(message = "This is a required field.")])

    city = StringField(label = "city", validators = [DataRequired(message = "This is a required field.")])

    genre = StringField(label = "Genre", validators = [DataRequired(message = "This is a required field.")])

    submit = SubmitField("Submit")


class Works_OnForm(FlaskForm):
    project_id = IntegerField(label = "Project Id", validators =  [DataRequired(message = "id is a required field.")])

    researcher_id = IntegerField(label = "Field Id", validators = [Optional()])

    submit = SubmitField("Submit")

class EvaluationForm(FlaskForm):
    project_id = IntegerField(label = "Project Id", validators = [DataRequired(message = "id is a required field.")])

    researcher_id = IntegerField(label = "Field Id", validators = [Optional()])

    evaluation_date = DateField(label = "Evaluation Date", validators = [DataRequired(message = "This is a required field.")])

    grade = IntegerField(label = "Grade", validators = [DataRequired(message = "This is a required field.")])

    submit = SubmitField("Submit")


class DeliverableForm(FlaskForm):
    Deliverable_id = IntegerField(label = "Deliverable Id", validators = [Optional()])

    project_id = IntegerField(label = "Project Id", validators = [DataRequired(message = "id is a required field.")])

    submission_date = DateField(label = "Submission Date", validators = [DataRequired(message = "This is a required field.")])

    title = StringField(label = "Title", validators = [DataRequired(message = "This is a required field.")])

    summary = StringField(label = "Summary", validators = [DataRequired(message = "This is a required field.")])

    submit = SubmitField("Submit")
