from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from elidek import app, db ## initially created by __init__.py, need to be used here
from elidek.forms import *

@app.route("/")
def index():
        return render_template("landing.html", pageTitle = "Landing Page")
@app.route("/programs")
def getPrograms():
        form = ProgramForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM PROGRAM")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("programs.html", views = views, pageTitle = "Programs Page", form=form)

@app.route("/programs/create", methods = ["GET", "POST"]) ## "GET" by default
def createStudent():
    form = ProgramForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newProgram = form.__dict__
        query = "INSERT INTO PROGRAM(program_name, program_address) VALUES ('{}', '{}');".format(newProgram['program_name'].data, newProgram['program_address'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Program inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_program.html", pageTitle = "Create Program", form = form)

@app.route("/programs/update/<int:programID>", methods = ["POST"])
def updateProgram(programID):
    form = ProgramForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE PROGRAM SET program_name = '{}', program_address = '{}' WHERE program_id = {};".format(updateData['program_name'].data, updateData['program_address'].data, programID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Program updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getPrograms"))

@app.route("/programs/delete/<int:programID>", methods = ["POST"])
def deleteProgram(programID):
    query = f"DELETE FROM PROGRAM WHERE program_id = {programID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Program deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getPrograms"))


@app.route("/projects", methods = ['GET', 'POST'])
def getProjects():
    form = ProjectForm()
    cur = db.connection.cursor()

    query = """
    SELECT project_id, title, summary, starting_date, ending_date, funds, e.executive_name, e.executive_surname
    FROM PROJECT p INNER JOIN EXECUTIVE e
    ON p.executive_id = e.executive_id

    """
    if(request.method == "POST" and form.validate_on_submit()):
        starting_date = str(request.form.get('starting_date'))
        ending_date = str(request.form.get('ending_date'))
        duration = str(request.form.get('duration'))
        executive_name = str(request.form.get('executive_name'))
        executive_surname = str(request.form.get('executive_surname'))
        where_clause = 'WHERE'
        if starting_date != '':
            query += f'{where_clause} p.starting_date= \'{starting_date}\''
            where_clause = '  AND'
        if ending_date != '':
            query += f'{where_clause} p.ending_date= \'{ending_date}\''
            where_clause = '  AND'
        if duration != '':
            query += f'{where_clause} p.ending_date-p.starting_date = \'{duration}\''
            where_clause = '  AND'
        if executive_name != '':
            query += f'{where_clause} e.executive_name = \'{executive_name}\''
            where_clause = '  AND'
        if executive_surname != '':
            query += f'{where_clause} e.executive_surname = \'{executive_surname}\''
            where_clause = '  AND'
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    projects = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("projects.html", projects=projects, pageTitle = "Projects Page", form = form)


@app.route("/researchers_per_project", methods = ['GET', 'POST'])
def getResearchers():
    form = ResearcherForm()
    cur = db.connection.cursor()
    query = """
    SELECT *
    from RESEARCHER r JOIN WORKS_ON w
    where r.researcher_id=w.researcher_id
    """
    if(request.method == "POST" and form.validate_on_submit()):
        researcher_id = str(request.form.get('researcher_id'))
        if researcher_id != '':
            query += f' AND w.project_id= \'{researcher_id}\''
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("researchers_per_project.html", researchers=researchers, pageTitle = "Researchers per Project Page", form = form)


@app.route("/researchers_per_project/update/<int:researcherID>", methods = ["POST"])
def updateResearcher(researcherID):
    form = ResearcherForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE RESEARCHER SET name = '{}', surname = '{}', gender = '{}', birth_date = '{}', organization_id = '{}', recruitment_date = '{}' WHERE researcher_id = {};".format(updateData['name'].data, updateData['surname'].data, updateData['gender'].data, updateData['birth_date'].data, updateData['organization_id'].data, updateData['recruitment_date'].data, researcherID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Researcher updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getResearchers"))

@app.route("/researchers_per_project/delete/<int:researcherID>", methods = ["POST"])
def deleteResearcher(researcherID):
    query = f"DELETE FROM RESEARCHER WHERE researcher_id = {researcherID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Researcher deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getResearcher"))


@app.route("/projects/update/<int:projectID>", methods = ["POST"])
def updateProject(projectID):
    form = ProjectForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE PROJECT SET title = '{}', summary = '{}', funds = '{}', starting_date = '{}', ending_date = '{}' WHERE project_id = {};".format(updateData['title'].data, updateData['summary'].data, updateData['funds'].data, updateData['starting_date'].data, updateData['ending_date'].data, projectID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Project updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getProjects"))

@app.route("/projects/delete/<int:projectID>", methods = ["POST"])
def deleteProject(projectID):
    query = f"DELETE FROM PROJECT WHERE project_id = {projectID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Project deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getProjects"))

@app.route("/projects_per_researcher", methods = ['GET', 'POST'])
def getProjPerRes():
    cur = db.connection.cursor()
    query = """
    select * from proj_per_res
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("projects_per_researcher.html", views=views, pageTitle = "View1: Projects per Researcher")

@app.route("/deliverables_per_project", methods = ['GET', 'POST'])
def getDelPerProj():
    cur = db.connection.cursor()
    query = """
    select * from del_per_proj
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("deliverables_per_project.html", views=views, pageTitle = "View2: Deliverables Per Project")



@app.route("/consecutive_years", methods = ['GET', 'POST'])
def getConsecutiveYears():
    cur = db.connection.cursor()
    query = """
    select org.organization_id as c1, org.name as c2, same_proj.first_year as c3, proj_now as c4
            from ( select DISTINCT organization_id as fav_id, YEAR(starting_date) as first_year, (
                    select count(*)
                    from PROJECT
                    where YEAR(starting_date) = first_year
                    and organization_id = fav_id
                ) as proj_now, (
                    select count(*) from PROJECT
                    where YEAR(starting_date) + 1 = first_year and organization_id = fav_id ) as proj_before
                from PROJECT
                having proj_now = proj_before and proj_now>10
                order by fav_id ) same_proj inner join ORGANIZATION org ON org.organization_id = same_proj.fav_id
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("consecutive_years.html", views=views, pageTitle = "Same number of projects in two consecutive years")


@app.route("/field_pairs", methods = ['GET', 'POST'])
def getFieldPairs():
    cur = db.connection.cursor()
    query = """
    select f1.field_name as c1, f2.field_name as c2, cnt as c3
       from ( select distinct ref1.field_id as id1, ref2.field_id as id2,
              ( select count(*) from REFERS_TO ref3 join REFERS_TO ref4 on ref3.project_id = ref4.project_id
                       where ref3.field_id = ref1.field_id and ref4.field_id = ref2.field_id and ref3.field_id <> ref4.field_id ) as cnt
              from REFERS_TO ref1 join REFERS_TO ref2 on ref1.project_id = ref2.project_id
              where ref1.field_id < ref2.field_id
              order by cnt DESC LIMIT 3 ) as result
        join FIELD f1 on f1.field_id = result.id1 join FIELD f2 on result.id2 = f2.field_id
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("field_pairs.html", views=views, pageTitle = "Most common pairs of fields in a project")


@app.route("/no_deliverables", methods = ['GET', 'POST'])
def getNoDeliverables():
    cur = db.connection.cursor()
    query = """
        select r.name as c1, r.surname as c2, count(no_del.project_id) as c3 from
    ( select project_id from PROJECT where deliverables=0) no_del
    join WORKS_ON w on no_del.project_id = w.project_id
    join RESEARCHER r on w.researcher_id = r.researcher_id
    group by r.researcher_id having c3 >= 5
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("no_deliverables.html", views=views, pageTitle = "Researchers on projects with no deliverables")


@app.route("/create_field", methods = ["GET", "POST"]) ## "GET" by default
def createfield():
    form = FieldForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO FIELD(field_id, field_name) VALUES ('{}', '{}');".format(new['field_id'].data, new['field_name'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Field inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_field.html", pageTitle = "Create Field", form = form)

@app.route("/create_executive", methods = ["GET", "POST"]) ## "GET" by default
def createexecutive():
    form = ExecutiveForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO EXECUTIVE(executive_id, executive_name, executive_surname) VALUES ('{}', '{}', '{}');".format(new['executive_id'].data, new['executive_name'].data, new['executive_surname'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Executive inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_executive.html", pageTitle = "Create Executive", form = form)


@app.route("/create_organization", methods = ["GET", "POST"]) ## "GET" by default
def createorganization():
    form = OrganizationForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO ORGANIZATION(organization_id, acronym, name, postal_code, street, city, genre) VALUES ('{}', '{}', '{}','{}','{}','{}','{}');".format(new['organization_id'].data, new['acronym'].data, new['name'].data, new['postal_code'].data, new['street'].data, new['city'].data, new['genre'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Organization inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_organization.html", pageTitle = "Create Organization", form = form)


@app.route("/create_university", methods = ["GET", "POST"]) ## "GET" by default
def createuniversity():
    form = UniversityForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO UNIVERSITY(ministry_budget, organization_id, university_id) VALUES ('{}', '{}', '{}');".format(new['ministry_budget'].data, new['organization_id'].data, new['university_id'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("University inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_university.html", pageTitle = "Create University", form = form)

@app.route("/create_company", methods = ["GET", "POST"]) ## "GET" by default
def createcompany():
    form = CompanyForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO COMPANY(company_budget, organization_id, company_id) VALUES ('{}', '{}', '{}');".format(new['company_budget'].data, new['organization_id'].data, new['company_id'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Company inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_company.html", pageTitle = "Create Company", form = form)

@app.route("/create_research_center", methods = ["GET", "POST"]) ## "GET" by default
def createresearch():
    form = Research_CenterForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO RESEARCH_CENTER (center_budget, ministry_budget, organization_id, research_center_id) VALUES ('{}', '{}', '{}', '{}');".format(new['center_budget'].data, new['ministry_budget'].data, new['organization_id'].data, new['research_center_id'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Center inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_research_center.html", pageTitle = "Create Research Center", form = form)


@app.route("/create_phone_number", methods = ["GET", "POST"]) ## "GET" by default
def createphone():
    form = Organization_PhoneForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO ORGANIZATION_PHONE (phone_number, organization_id) VALUES ('{}', '{}');".format(new['phone_number'].data, new['organizaton_id'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Phone Number inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_phone_number.html", pageTitle = "Insert a phone number for an organization", form = form)


@app.route("/create_researcher", methods = ["GET", "POST"]) ## "GET" by default
def createresearcher():
    form = ResearcherCreateForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO RESEARCHER(researcher_id, name, surname, gender, birth_date, organization_id, recruitment_date) VALUES ('{}', '{}', '{}','{}','{}','{}','{}');".format(new['researcher_id'].data, new['name'].data, new['surname'].data, new['gender'].data, new['birth_date'].data, new['organization_id'].data, new['recruitment_date'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Researcher inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_researcher.html", pageTitle = "Create Researcher", form = form)

@app.route("/create_project", methods = ["GET", "POST"]) ## "GET" by default
def createproject():
    form = ProjectCreateForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO PROJECT(project_id, title, summary, funds, starting_date, ending_date, executive_id, program_id, organization_id, researcher_id, deliverables) VALUES ('{}', '{}', '{}','{}','{}','{}','{}', '{}', '{}', '{}', '{}');".format(new['project_id'].data, new['title'].data, new['summary'].data, new['funds'].data, new['starting_date'].data, new['ending_date'].data, new['executive_id'].data, new['program_id'].data, new['organization_id'].data, new['researcher_id'].data, new['deliverables'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Project inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_project.html", pageTitle = "Create Project", form = form)

@app.route("/create_deliverable", methods = ["GET", "POST"]) ## "GET" by default
def createdeliverable():
    form = DeliverableForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO DELIVERABLE(deliverable_id, summary, submission_date, title, project_id,) VALUES ('{}', '{}', '{}','{}','{}');".format(new['deliverable_id'].data, new['summary'].data, new['submission_date'].data, new['title'].data, new['project_id'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Deliverable inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_deliverable.html", pageTitle = "Create Deliverable", form = form)

@app.route("/create_evaluation", methods = ["GET", "POST"]) ## "GET" by default
def createevaluation():
    form = EvaluationForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO EVALUATION(project_id, researcher_id, evaluation_date, grade) VALUES ('{}', '{}', '{}','{}');".format(new['project_id'].data, new['researcher_id'].data, new['evaluation_date'].data, new['grade'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Evaluation inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_evaluation.html", pageTitle = "Set a Researcher to evaluate a project", form = form)

@app.route("/create_works_on", methods = ["GET", "POST"]) ## "GET" by default
def createworks_on():
    form = Works_OnForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO WORKS_ON (project_id, researcher_id) VALUES ('{}', '{}');".format(new['project_id'].data, new['researcher_id'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("The researcher will start working as soon as possible", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_works_on.html", pageTitle = "Set a researcher to work on a project", form = form)

@app.route("/create_refers_to", methods = ["GET", "POST"]) ## "GET" by default
def createrefers_to():
    form = Refers_ToForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        new = form.__dict__
        query = "INSERT INTO REFERS_TO (project_id, field_id) VALUES ('{}', '{}');".format(new['project_id'].data, new['field_id'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("The project was associated with the field", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_refers_to.html", pageTitle = "Set a project to refer to a research field", form = form)



@app.route("/fields")
def getFields():
        form = FieldForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM FIELD")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("fields.html", views = views, pageTitle = "Update-Delete Section", form=form)

@app.route("/fields/update/<int:fieldID>", methods = ["POST"])
def updateField(fieldID):
    form = FieldForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE FIELD SET field_name = '{}' WHERE field_id = {};".format(updateData['field_name'].data, fieldID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getFields"))

@app.route("/fields/delete/<int:fieldID>", methods = ["POST"])
def deleteField(fieldID):
    query = f"DELETE FROM FIELD WHERE field_id = {fieldID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getFields"))

@app.route("/executives")
def getExecutives():
        form = ExecutiveForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM EXECUTIVE")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("executives.html", views = views, pageTitle = "Update-Delete Section", form=form)

@app.route("/executives/update/<int:executiveID>", methods = ["POST"])
def updateExecutive(executiveID):
    form = ExecutiveForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE EXECUTIVE SET executive_name = '{}', executive_surname = '{}' WHERE executive_id = {};".format(updateData['executive_name'].data, updateData['executive_surname'].data, executiveID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getExecutives"))

@app.route("/executives/delete/<int:executiveID>", methods = ["POST"])
def deleteExecutive(executiveID):
    query = f"DELETE FROM EXECUTIVE WHERE executive_id = {executiveID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getExecutives"))

@app.route("/organizations")
def getOrganizations():
        form = OrganizationForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM ORGANIZATION")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("organizations.html", views = views, pageTitle = "Update-Delete Section", form=form)

@app.route("/organizations/update/<int:organizationID>", methods = ["POST"])
def updateOrganization(organizationID):
    form = OrganizationForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE ORGANIZATION SET acronym = '{}', name = '{}', postal_code = '{}', street = '{}', city = '{}', genre = '{}' WHERE organization_id = {};".format(updateData['acronym'].data, updateData['name'].data, updateData['postal_code'].data, updateData['street'].data, updateData['city'].data, updateData['genre'].data, organizationID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getOrganizations"))

@app.route("/organizations/delete/<int:organizationID>", methods = ["POST"])
def deleteOrganization(organizationID):
    query = f"DELETE FROM ORGANIZATION WHERE organization_id = {organizationID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getOrganizations"))


@app.route("/deliverables")
def getDeliverables():
        form = DeliverableForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM DELIVERABLE")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("deliverables.html", views = views, pageTitle = "Update-Delete Section", form=form)

@app.route("/deliverables/update/<int:deliverableID>", methods = ["POST"])
def updateDeliverable(deliverableID):
    form = DeliverableForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE DELIVERABLE SET summary = '{}', submission_date = '{}', title = '{}', project_id = '{}' WHERE deliverable_id = {};".format(updateData['summary'].data, updateData['submission_date'].data, updateData['title'].data, updateData['project_id'].data, deliverableID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getDeliverables"))

@app.route("/deliverables/delete/<int:deliverableID>", methods = ["POST"])
def deleteDeliverable(deliverableID):
    query = f"DELETE FROM DELIVERABLE WHERE deliverable_id = {deliverableID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getDeliverables"))

@app.route("/evaluations")
def getEvaluations():
        form = EvaluationForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM EVALUATION")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("evaluations.html", views = views, pageTitle = "Update-Delete Section", form=form)

@app.route("/evaluations/update/<int:researcherID>", methods = ["POST"])
def updateEvaluation(researcherID):
    form = EvaluationForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE EVALUATION SET project_id = '{}', evaluation_date = '{}', grade = '{}' WHERE researcher_id = {};".format(updateData['project_id'].data, updateData['evaluation_date'].data, updateData['grade'].data, researcherID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getEvaluations"))

@app.route("/evaluations/delete/<int:researcherID>", methods = ["POST"])
def deleteEvaluation(researcherID):
    query = f"DELETE FROM EVALUATION WHERE researcher_id = {researcherID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getEvaluations"))


@app.route("/works_on")
def getWorks_On():
        form = Works_OnForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM WORKS_ON")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("works_on.html", views = views, pageTitle = "Update-Delete Section", form=form)

@app.route("/works_on/update/<int:researcherID>", methods = ["POST"])
def updateWorks_On(researcherID):
    form = Works_OnForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE WORKS_ON SET project_id = '{}' WHERE researcher_id = {};".format(updateData['project_id'].data, researcherID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getWorks_On"))

@app.route("/works_on/delete/<int:researcherID>", methods = ["POST"])
def deleteWorks_On(researcherID):
    query = f"DELETE FROM WORKS_ON WHERE researcher_id = {researcherID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getWorks_On"))

@app.route("/interesting_field", methods = ['GET', 'POST'])
def interesting_field():
    views1=[]
    views2=[]
    form = FieldForm()
    cur = db.connection.cursor()
    if(request.method == "POST"):
        field_name = str(request.form.get('field_name'))
        query1 = f"""
        select p.project_id as c1, p.title as c2, f.field_name as c3
        FROM PROJECT p
        INNER JOIN REFERS_TO ref
        ON p.project_id=ref.project_id AND p.ending_date>NOW()
        INNER JOIN FIELD f
        ON ref.field_id=f.field_id
        WHERE f.field_name= '{field_name}'
        """

        query2 = f"""
        select r.name as c4, r.surname as c5
        from WORKS_ON w
        inner join
        (select p.project_id as col1
        FROM PROJECT p join REFERS_TO ref ON p.project_id=ref.project_id AND p.ending_date>NOW() AND DATEDIFF(NOW(), p.starting_date) > 365
        INNER JOIN FIELD f
        ON ref.field_id=f.field_id WHERE f.field_name= '{field_name}' ) a
        on a.col1=w.project_id
        join RESEARCHER r
        on w.researcher_id=r.researcher_id AND DATEDIFF(NOW(), r.recruitment_date) > 365

        """
        cur.execute(query1)
        column_names1 = [i[0] for i in cur.description]
        views1 = [dict(zip(column_names1, entry)) for entry in cur.fetchall()]
        cur.execute(query2)
        column_names = [i[0] for i in cur.description]
        views2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        print(query1)
    return render_template("interesting_field.html", views1=views1, views2=views2, form = form, pageTitle = "And all of a sudden this field became so interesting...")

@app.route("/refers_to")
def getRefers_To():
        form = Refers_ToForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM REFERS_TO")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("refers_to.html", views = views, pageTitle = "Update-Delete Section", form=form)

@app.route("/refers_to/update/<int:projectID>", methods = ["POST"])
def updateRefers_To(projectID):
    form = Refers_ToForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE REFERS_TO SET field_id = '{}' WHERE project_id = {};".format(updateData['field_id'].data, projectID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getRefers_To"))

@app.route("/refers_to/delete/<int:projectID>", methods = ["POST"])
def deleteRefers_To(projectID):
    query = f"DELETE FROM REFERS_TO WHERE project_id = {projectID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getRefers_To"))



@app.route("/researchers")
def getRes():
        form = ResearcherForm()
        cur = db.connection.cursor()
        cur.execute("SELECT researcher_id, name, surname FROM RESEARCHER")
        column_names = [i[0] for i in cur.description]
        views = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("researchers.html", views = views, pageTitle = "Update-Delete Section", form=form)


@app.route("/researchers/delete/<int:researcherID>", methods = ["POST"])
def deleteRes(researcherID):
    query = f"DELETE FROM RESEARCHER WHERE researcher_id = {researcherID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getRes"))



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500
