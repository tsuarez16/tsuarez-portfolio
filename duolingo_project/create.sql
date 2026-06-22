-- Created by Redgate Data Modeler (https://datamodeler.redgate-platform.com)
-- Last modification date: 2025-12-06 19:59:27.7

-- tables
-- Table: Attempt
CREATE TABLE Attempt (
    attempt_id int  NOT NULL,
    attempted_at timestamp  NOT NULL,
    is_correct boolean  NOT NULL,
    learner_id int  NOT NULL,
    CONSTRAINT Attempt_pk PRIMARY KEY (attempt_id)
);

-- Table: Course
CREATE TABLE Course (
    course_id int  NOT NULL,
    name text  NOT NULL,
    language_taught_in text  NOT NULL,
    language_learning text  NOT NULL,
    CONSTRAINT Course_pk PRIMARY KEY (course_id)
);

-- Table: CourseAssignment
CREATE TABLE CourseAssignment (
    employee_id int  NOT NULL,
    course_id int  NOT NULL,
    CONSTRAINT CourseAssignment_pk PRIMARY KEY (employee_id,course_id)
);

-- Table: Employee
CREATE TABLE Employee (
    employee_id int  NOT NULL,
    name text  NOT NULL,
    position text  NOT NULL,
    department text  NOT NULL,
    CONSTRAINT Employee_pk PRIMARY KEY (employee_id)
);

-- Table: Enrollments
CREATE TABLE Enrollments (
    course_id int  NOT NULL,
    learner_id int  NOT NULL,
    CONSTRAINT Enrollments_pk PRIMARY KEY (course_id,learner_id)
);

-- Table: Exercise
CREATE TABLE Exercise (
    exercise_id int  NOT NULL,
    difficulty_level text  NOT NULL,
    question_type text  NOT NULL,
    question text  NOT NULL,
    accuracy_score decimal(4,3)  NOT NULL,
    attempt_id int  NOT NULL,
    lesson_id int  NOT NULL,
    CONSTRAINT Exercise_pk PRIMARY KEY (exercise_id)
);

-- Table: Learner
CREATE TABLE Learner (
    learner_id int  NOT NULL,
    name text  NOT NULL,
    username text  NOT NULL,
    last_login date  NOT NULL,
    languages_learned text  NOT NULL,
    total_xp int  NOT NULL,
    streak int  NOT NULL,
    streak_notification_preference boolean  NOT NULL,
    user_type varchar(10)  NOT NULL CHECK ((user_type IN ('freemium', 'max'))),
    
    -- Freemium User
    current_hearts int   NULL,
    ad_preference text   NULL,

    -- Max USer
    subscription_date date   NULL,
    card_number int  NULL,
    CONSTRAINT Learner_pk PRIMARY KEY (learner_id)
);

-- Table: Lesson
CREATE TABLE Lesson (
    lesson_id int  NOT NULL,
    course_id int  NOT NULL,
    title text  NOT NULL,
    difficulty_level text  NOT NULL,
    accuracy_score decimal(4,3)  NOT NULL,
    CONSTRAINT Lesson_pk PRIMARY KEY (lesson_id)
);

-- Table: LessonProgress
CREATE TABLE LessonProgress (
    learner_id int  NOT NULL,
    lesson_id int  NOT NULL,
    start_time timestamp  NOT NULL,
    completion_time timestamp  NOT NULL,
    best_accuracy decimal(4,3)  NOT NULL,
    xp_earned int  NOT NULL,
    CONSTRAINT LessonProgress_pk PRIMARY KEY (learner_id,lesson_id)
);

-- foreign keys
-- Reference: Attempt_Learner (table: Attempt)
ALTER TABLE Attempt ADD CONSTRAINT Attempt_Learner
    FOREIGN KEY (learner_id)
    REFERENCES Learner (learner_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: CourseAssignment_Course (table: CourseAssignment)
ALTER TABLE CourseAssignment ADD CONSTRAINT CourseAssignment_Course
    FOREIGN KEY (course_id)
    REFERENCES Course (course_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: CourseAssignment_Employee (table: CourseAssignment)
ALTER TABLE CourseAssignment ADD CONSTRAINT CourseAssignment_Employee
    FOREIGN KEY (employee_id)
    REFERENCES Employee (employee_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Enrollments_Course (table: Enrollments)
ALTER TABLE Enrollments ADD CONSTRAINT Enrollments_Course
    FOREIGN KEY (course_id)
    REFERENCES Course (course_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Enrollments_Learner (table: Enrollments)
ALTER TABLE Enrollments ADD CONSTRAINT Enrollments_Learner
    FOREIGN KEY (learner_id)
    REFERENCES Learner (learner_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Exercise_Attempt (table: Exercise)
ALTER TABLE Exercise ADD CONSTRAINT Exercise_Attempt
    FOREIGN KEY (attempt_id)
    REFERENCES Attempt (attempt_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Exercise_Lesson (table: Exercise)
ALTER TABLE Exercise ADD CONSTRAINT Exercise_Lesson
    FOREIGN KEY (lesson_id)
    REFERENCES Lesson (lesson_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: LessonProgress_Learner (table: LessonProgress)
ALTER TABLE LessonProgress ADD CONSTRAINT LessonProgress_Learner
    FOREIGN KEY (learner_id)
    REFERENCES Learner (learner_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: LessonProgress_Lesson (table: LessonProgress)
ALTER TABLE LessonProgress ADD CONSTRAINT LessonProgress_Lesson
    FOREIGN KEY (lesson_id)
    REFERENCES Lesson (lesson_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Lesson_Course (table: Lesson)
ALTER TABLE Lesson ADD CONSTRAINT Lesson_Course
    FOREIGN KEY (course_id)
    REFERENCES Course (course_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Triggers
-- Trigger function to decrease hearts when a learner gets something wrong
CREATE OR REPLACE FUNCTION decrease_hearts_on_wrong_answer()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_correct = FALSE THEN
        UPDATE Learner
        SET current_hearts = GREATEST(current_hearts - 1, 0)
        WHERE learner_id = NEW.learner_id AND user_type = 'freemium';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_decrease_hearts
AFTER INSERT ON Attempt
FOR EACH ROW
EXECUTE FUNCTION decrease_hearts_on_wrong_answer();

-- End of file.

