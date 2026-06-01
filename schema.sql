CREATE DATABASE InterviewManager;

USE InterviewManager;

CREATE TABLE GlobalAdmin(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Companies(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE CompanyAdmin(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

CREATE TABLE Interviewer(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

CREATE TABLE Candidate(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Jobs(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    company_id INT NOT NULL,
    vacancies INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

CREATE TABLE Applications(
    id INT PRIMARY KEY AUTO_INCREMENT,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    resume TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (candidate_id) REFERENCES Candidate(id),
    FOREIGN KEY (job_id) REFERENCES Jobs(id)
);

CREATE TABLE Interviews(
    id INT PRIMARY KEY AUTO_INCREMENT,
    application_id INT NOT NULL,
    interviewer_id INT NOT NULL,
    scheduled_time DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (application_id) REFERENCES Applications(id),
    FOREIGN KEY (interviewer_id) REFERENCES Interviewer(id)
);
