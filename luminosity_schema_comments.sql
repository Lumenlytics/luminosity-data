
-- ===========================
-- 🏫 Table: students
-- ===========================
COMMENT ON TABLE students IS 'All enrolled students, uniquely identified. Primary demographic and grade level information.';
COMMENT ON COLUMN students.student_id IS 'Primary key: unique student identifier';
COMMENT ON COLUMN students.first_name IS 'Student first name';
COMMENT ON COLUMN students.last_name IS 'Student last name';
COMMENT ON COLUMN students.birthdate IS 'Date of birth';
COMMENT ON COLUMN students.gender IS 'Student gender (M/F/Other)';
COMMENT ON COLUMN students.grade IS 'Foreign key to grade_levels.grade — student''s current grade';

-- ===========================
-- 👨‍👩‍👧 Table: guardians
-- ===========================
COMMENT ON TABLE guardians IS 'Parents or guardians associated with students';
COMMENT ON COLUMN guardians.guardian_id IS 'Primary key: unique guardian identifier';
COMMENT ON COLUMN guardians.first_name IS 'Guardian first name';
COMMENT ON COLUMN guardians.last_name IS 'Guardian last name';
COMMENT ON COLUMN guardians.phone IS 'Contact phone number';
COMMENT ON COLUMN guardians.email IS 'Contact email address';

-- ===========================
-- 📛 Table: guardian_types
-- ===========================
COMMENT ON TABLE guardian_types IS 'Types of relationships guardians can have with students (e.g., Mother, Father, Stepmother)';
COMMENT ON COLUMN guardian_types.guardian_type_id IS 'Primary key';
COMMENT ON COLUMN guardian_types.type_name IS 'Guardian type label';

-- ===========================
-- 🔗 Table: student_guardians
-- ===========================
COMMENT ON TABLE student_guardians IS 'Join table linking students to their guardians';
COMMENT ON COLUMN student_guardians.student_id IS 'Foreign key to students.student_id';
COMMENT ON COLUMN student_guardians.guardian_id IS 'Foreign key to guardians.guardian_id';
COMMENT ON COLUMN student_guardians.guardian_type_id IS 'Foreign key to guardian_types.guardian_type_id — identifies relationship type';

-- ===========================
-- 🧑‍🏫 Table: teachers
-- ===========================
COMMENT ON TABLE teachers IS 'All teaching staff members';
COMMENT ON COLUMN teachers.teacher_id IS 'Primary key: unique teacher identifier';
COMMENT ON COLUMN teachers.first_name IS 'Teacher first name';
COMMENT ON COLUMN teachers.last_name IS 'Teacher last name';

-- ===========================
-- 🏛️ Table: departments
-- ===========================
COMMENT ON TABLE departments IS 'School departments (e.g., Math, Science)';
COMMENT ON COLUMN departments.department_id IS 'Primary key';
COMMENT ON COLUMN departments.department_name IS 'Department name';

-- ===========================
-- 📚 Table: teacher_subjects
-- ===========================
COMMENT ON TABLE teacher_subjects IS 'Subjects that a teacher is qualified to teach';
COMMENT ON COLUMN teacher_subjects.teacher_id IS 'Foreign key to teachers.teacher_id';
COMMENT ON COLUMN teacher_subjects.subject IS 'Subject area (e.g., Algebra, Biology)';
COMMENT ON COLUMN teacher_subjects.department_id IS 'Foreign key to departments.department_id';

-- ===========================
-- 🏫 Table: classrooms
-- ===========================
COMMENT ON TABLE classrooms IS 'List of physical classrooms';
COMMENT ON COLUMN classrooms.room_id IS 'Primary key';
COMMENT ON COLUMN classrooms.building IS 'Building name';
COMMENT ON COLUMN classrooms.room_number IS 'Room number';

-- ===========================
-- 🏷️ Table: classes
-- ===========================
COMMENT ON TABLE classes IS 'Offered classes by subject, teacher, grade level, and period';
COMMENT ON COLUMN classes.class_id IS 'Primary key';
COMMENT ON COLUMN classes.subject IS 'Subject area (e.g., Math, History)';
COMMENT ON COLUMN classes.grade_level IS 'Grade level that the class targets';
COMMENT ON COLUMN classes.teacher_id IS 'Foreign key to teachers.teacher_id';
COMMENT ON COLUMN classes.room_id IS 'Foreign key to classrooms.room_id';
COMMENT ON COLUMN classes.period_id IS 'Foreign key to periods.period_id';
COMMENT ON COLUMN classes.term_id IS 'Foreign key to terms.term_id';

-- ===========================
-- 🧾 Table: enrollments
-- ===========================
COMMENT ON TABLE enrollments IS 'Join table assigning students to classes';
COMMENT ON COLUMN enrollments.enrollment_id IS 'Primary key';
COMMENT ON COLUMN enrollments.student_id IS 'Foreign key to students.student_id';
COMMENT ON COLUMN enrollments.class_id IS 'Foreign key to classes.class_id';

-- ===========================
-- 📝 Table: assignments
-- ===========================
COMMENT ON TABLE assignments IS 'Graded assignments given in classes';
COMMENT ON COLUMN assignments.assignment_id IS 'Primary key';
COMMENT ON COLUMN assignments.class_id IS 'Foreign key to classes.class_id';
COMMENT ON COLUMN assignments.title IS 'Assignment title or short description';
COMMENT ON COLUMN assignments.due_date IS 'Date assignment is due';
COMMENT ON COLUMN assignments.points_possible IS 'Total points possible';
COMMENT ON COLUMN assignments.category IS 'Category of assignment (e.g., Homework, Quiz)';

-- ===========================
-- 🧮 Table: grades
-- ===========================
COMMENT ON TABLE grades IS 'Scores earned by students for assignments';
COMMENT ON COLUMN grades.grade_id IS 'Primary key';
COMMENT ON COLUMN grades.student_id IS 'Foreign key to students.student_id';
COMMENT ON COLUMN grades.assignment_id IS 'Soft reference to assignments.assignment_id (some grades may point to missing assignments)';
COMMENT ON COLUMN grades.score IS 'Points earned';
COMMENT ON COLUMN grades.submitted_on IS 'Date assignment was submitted';

-- (to be continued...)
