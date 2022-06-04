DROP DATABASE if exists elidek;
CREATE DATABASE if not exists elidek;
USE elidek;

CREATE TABLE IF NOT EXISTS PROGRAM (
    program_id INT unsigned AUTO_INCREMENT,
    program_name VARCHAR(45) NOT NULL,
    program_address VARCHAR(45) NOT NULL,
    PRIMARY KEY (program_id)
);

CREATE TABLE IF NOT EXISTS EXECUTIVE (
    executive_id INT unsigned AUTO_INCREMENT,
    executive_name VARCHAR(45) NOT NULL,
    executive_surname VARCHAR(45) NOT NULL,
    PRIMARY KEY (executive_id)
);

CREATE TABLE IF NOT EXISTS ORGANIZATION (
    organization_id INT unsigned AUTO_INCREMENT,
    acronym VARCHAR(45) NOT NULL,
    name VARCHAR(45) NOT NULL,
    postal_code VARCHAR(45) NOT NULL,
    street VARCHAR(45) NOT NULL,
    city VARCHAR(45) NOT NULL,
    genre ENUM('University', 'Company', 'Research Center') NOT NULL,
    PRIMARY KEY (organization_id)
);

CREATE TABLE IF NOT EXISTS ORGANIZATION_PHONE (
    phone_number BIGINT unsigned,
    organization_id INT unsigned,
    PRIMARY KEY (phone_number),
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION (organization_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS UNIVERSITY (
    university_id INT unsigned AUTO_INCREMENT,
    ministry_budget INT unsigned,
    organization_id INT unsigned,
    PRIMARY KEY (university_id),
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION (organization_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS COMPANY (
    company_id INT unsigned AUTO_INCREMENT,
    company_budget INT unsigned,
    organization_id INT unsigned,
    PRIMARY KEY (company_id),
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION (organization_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS RESEARCH_CENTER (
    research_center_id INT unsigned AUTO_INCREMENT,
    ministry_budget INT unsigned,
    center_budget INT unsigned,
    organization_id INT unsigned,
    PRIMARY KEY (research_center_id),
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION (organization_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS RESEARCHER (
    CHECK (birth_date<recruitment_date),
    CHECK(DATEDIFF(NOW(), birth_date) > 5844 AND DATEDIFF(recruitment_date, NOW()) < 0),
    researcher_id INT unsigned AUTO_INCREMENT,
    name VARCHAR(45) NOT NULL,
    surname VARCHAR(45) NOT NULL,
    gender VARCHAR(45) NOT NULL CHECK (gender='Male' OR gender='Female' OR gender='Other'),
    birth_date date NOT NULL,
    recruitment_date date NOT NULL,
    organization_id INT unsigned,
    PRIMARY KEY (researcher_id),
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION (organization_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS FIELD (
    field_id INT unsigned AUTO_INCREMENT,
    field_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (field_id)
);

CREATE TABLE IF NOT EXISTS PROJECT (
    CHECK (DATEDIFF(ending_date,starting_date) > 364 AND DATEDIFF(ending_date,starting_date) < 1461),
    project_id INT unsigned AUTO_INCREMENT,
    title VARCHAR(45) NOT NULL,
    summary VARCHAR(45) NOT NULL,
    funds INT unsigned CHECK (funds>100000 AND funds<1000000),
    starting_date date NOT NULL,
    ending_date date NOT NULL,
    executive_id INT unsigned,
    program_id INT unsigned,
    organization_id INT unsigned,
    researcher_id INT unsigned,
    deliverables INT unsigned CHECK(deliverables>=0),
    PRIMARY KEY (project_id),
    FOREIGN KEY (executive_id) REFERENCES EXECUTIVE (executive_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (program_id) REFERENCES PROGRAM (program_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION (organization_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (researcher_id) REFERENCES RESEARCHER (researcher_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS EVALUATION (
    project_id INT unsigned UNIQUE,
    researcher_id INT unsigned,
    evaluation_date date NOT NULL,
    grade INT unsigned NOT NULL CHECK(grade<=10 AND grade>=0),
    FOREIGN KEY (project_id) REFERENCES PROJECT (project_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (researcher_id) REFERENCES RESEARCHER (researcher_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS WORKS_ON (
    project_id INT unsigned,
    researcher_id INT unsigned,
    FOREIGN KEY (project_id) REFERENCES PROJECT (project_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (researcher_id) REFERENCES RESEARCHER (researcher_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS DELIVERABLE (
    deliverable_id INT unsigned AUTO_INCREMENT,
    summary VARCHAR(45) NOT NULL,
    title VARCHAR(45) NOT NULL,
    submission_date date NOT NULL,
    project_id INT unsigned,
    PRIMARY KEY (deliverable_id),
    FOREIGN KEY (project_id) REFERENCES PROJECT (project_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS REFERS_TO (
    field_id INT unsigned,
    project_id INT unsigned,
    FOREIGN KEY (field_id) REFERENCES FIELD (field_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (project_id) REFERENCES PROJECT (project_id) ON DELETE CASCADE ON UPDATE CASCADE
);




DELIMITER $$
CREATE TRIGGER deliverables_problem BEFORE INSERT ON DELIVERABLE
FOR EACH ROW
BEGIN
    IF (DATEDIFF(new.submission_date, (SELECT ending_date FROM PROJECT WHERE project_id = new.project_id)) > 0 OR DATEDIFF(new.submission_date, (SELECT starting_date FROM PROJECT WHERE project_id = new.project_id)) < 0) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Check once again the dates!!';
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER evaluation_problem BEFORE INSERT ON EVALUATION
FOR EACH ROW
BEGIN
    IF ((SELECT organization_id FROM RESEARCHER WHERE researcher_id = new.researcher_id) = (SELECT organization_id FROM PROJECT WHERE project_id = new.project_id) ) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'evaluation problem';
    END IF;
END$$
DELIMITER ;


CREATE INDEX STARTING_DATE_INDEX ON PROJECT(starting_date);
CREATE INDEX ENDING_DATE_INDEX ON PROJECT(ending_date);
CREATE INDEX FUNDS_INDEX ON PROJECT(funds);
CREATE INDEX EXEC_PROJ_INDEX ON PROJECT(executive_id);
CREATE INDEX PROG_PROJ_INDEX ON PROJECT(program_id);
CREATE INDEX ORG_PROJ_INDEX ON PROJECT(organization_id);
CREATE INDEX EVAL_PROJ_INDEX ON EVALUATION(project_id);
CREATE INDEX EVAL_RES_INDEX ON EVALUATION(researcher_id);
CREATE INDEX W_PROJ_INDEX ON WORKS_ON(project_id);
CREATE INDEX W_RES_INDEX ON WORKS_ON(researcher_id);
CREATE INDEX DEL_PROJ_INDEX ON DELIVERABLE(project_id);
CREATE INDEX REF_FIELD_INDEX ON REFERS_TO(field_id);
CREATE INDEX REF_PROJ_INDEX ON REFERS_TO(project_id);




CREATE VIEW proj_per_res AS
SELECT r.researcher_id as c1, r.name as c2, r.surname as c3, p.project_id as c4, p.title as c5
FROM RESEARCHER r INNER JOIN WORKS_ON w ON r.researcher_id= w.researcher_id
INNER JOIN PROJECT p on w.project_id = p.project_id
ORDER BY r.researcher_id;


CREATE VIEW del_per_proj AS
SELECT p.project_id as c1, p.title as c2, d.deliverable_id as c3, d.title as c4
FROM DELIVERABLE d JOIN PROJECT p
WHERE d.project_id=p.project_id
order by p.project_id;
