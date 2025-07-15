-- grade_levels
COMMENT ON TABLE grade_levels IS 'Defines the available grade levels (e.g., 1st grade, 8th grade, etc.).';
COMMENT ON COLUMN grade_levels.grade IS 'Primary key: grade level number (e.g., 1 for 1st grade).';
COMMENT ON COLUMN grade_levels.level_name IS 'Name or label for the grade level.';

-- student_grade_history
COMMENT ON TABLE student_grade_history IS 'Tracks a student''s placement in a specific grade during a given academic year.';
COMMENT ON COLUMN student_grade_history.history_id IS 'Primary key: unique ID for each record.';
COMMENT ON COLUMN student_grade_history.student_id IS 'Foreign key: student enrolled that year.';
COMMENT ON COLUMN student_grade_history.year_id IS 'Foreign key: school year of the record.';
COMMENT ON COLUMN student_grade_history.grade IS 'Foreign key: grade level during that year.';

-- school_years
COMMENT ON TABLE school_years IS 'Defines academic school years with start and end dates.';
COMMENT ON COLUMN school_years.year_id IS 'Primary key: unique ID for each school year.';
COMMENT ON COLUMN school_years.school_id IS 'ID of the associated school (optional for multi-school setups).';
COMMENT ON COLUMN school_years.start_date IS 'Start date of the school year.';
COMMENT ON COLUMN school_years.end_date IS 'End date of the school year.';

-- terms
COMMENT ON TABLE terms IS 'Divides a school year into terms (e.g., semesters, trimesters).';
COMMENT ON COLUMN terms.term_id IS 'Primary key: unique ID for the term.';
COMMENT ON COLUMN terms.year_id IS 'Foreign key: which school year the term belongs to.';
COMMENT ON COLUMN terms.name IS 'Name of the term (e.g., Fall, Q1).';
COMMENT ON COLUMN terms.start_date IS 'Start date of the term.';
COMMENT ON COLUMN terms.end_date IS 'End date of the term.';

-- attendance
COMMENT ON TABLE attendance IS 'Records daily attendance status for each student.';
COMMENT ON COLUMN attendance.attendance_id IS 'Primary key: unique ID for each attendance record.';
COMMENT ON COLUMN attendance.student_id IS 'Foreign key: student whose attendance is recorded.';
COMMENT ON COLUMN attendance.date IS 'Date of the attendance record.';
COMMENT ON COLUMN attendance.status IS 'Attendance status (e.g., Present, Absent, Tardy).';

-- discipline_reports
COMMENT ON TABLE discipline_reports IS 'Logs disciplinary incidents involving students.';
COMMENT ON COLUMN discipline_reports.report_id IS 'Primary key: unique ID for each incident.';
COMMENT ON COLUMN discipline_reports.student_id IS 'Foreign key: student involved in the incident.';
COMMENT ON COLUMN discipline_reports.date IS 'Date of the incident.';
COMMENT ON COLUMN discipline_reports.type IS 'Type of incident (e.g., disruption, disrespect).';
COMMENT ON COLUMN discipline_reports.severity IS 'Severity rating or level of the incident.';
COMMENT ON COLUMN discipline_reports.action_taken IS 'Disciplinary action taken.';
COMMENT ON COLUMN discipline_reports.description IS 'Optional notes or explanation.';

-- standardized_tests
COMMENT ON TABLE standardized_tests IS 'Stores scores from standardized testing events.';
COMMENT ON COLUMN standardized_tests.test_id IS 'Primary key: unique test result ID.';
COMMENT ON COLUMN standardized_tests.student_id IS 'Foreign key: student who took the test.';
COMMENT ON COLUMN standardized_tests.test_name IS 'Name of the standardized test (e.g., MAP, SAT).';
COMMENT ON COLUMN standardized_tests.test_date IS 'Date the test was taken.';
COMMENT ON COLUMN standardized_tests.subject IS 'Subject area of the test (e.g., Math, ELA).';
COMMENT ON COLUMN standardized_tests.score IS 'Raw or scaled test score.';
COMMENT ON COLUMN standardized_tests.percentile IS 'Percentile ranking, if applicable.';

-- fee_types
COMMENT ON TABLE fee_types IS 'Defines types of fees charged to students.';
COMMENT ON COLUMN fee_types.fee_type_id IS 'Primary key: unique fee category.';
COMMENT ON COLUMN fee_types.name IS 'Name or description of the fee (e.g., Field Trip, Registration).';
COMMENT ON COLUMN fee_types.amount IS 'Dollar amount for the fee.';
COMMENT ON COLUMN fee_types.due_by IS 'Due date for the fee.';
COMMENT ON COLUMN fee_types.recurring IS 'True if the fee recurs (e.g., monthly).';

-- payments
COMMENT ON TABLE payments IS 'Tracks fee payments made by students.';
COMMENT ON COLUMN payments.payment_id IS 'Primary key: unique payment record.';
COMMENT ON COLUMN payments.student_id IS 'Foreign key: student making the payment.';
COMMENT ON COLUMN payments.fee_type_id IS 'Foreign key: fee that was paid.';
COMMENT ON COLUMN payments.amount_paid IS 'Dollar amount paid.';
COMMENT ON COLUMN payments.date_paid IS 'Date payment was received.';

-- school_calendar
COMMENT ON TABLE school_calendar IS 'Captures school calendar events and operating days.';
COMMENT ON COLUMN school_calendar.calendar_date IS 'Date of the calendar entry.';
COMMENT ON COLUMN school_calendar.is_school_day IS 'True if this is a normal school day.';
COMMENT ON COLUMN school_calendar.is_holiday IS 'True if this is a holiday.';
COMMENT ON COLUMN school_calendar.holiday_name IS 'Name of the holiday, if any.';
COMMENT ON COLUMN school_calendar.comment IS 'Additional notes (e.g., half-day, staff PD).';

-- periods
COMMENT ON TABLE periods IS 'Defines class periods (e.g., 1st hour, Block B).';
COMMENT ON COLUMN periods.period_id IS 'Primary key: unique ID for the period.';
COMMENT ON COLUMN periods.name IS 'Name or label for the period.';
COMMENT ON COLUMN periods.start_time IS 'Start time of the period.';
COMMENT ON COLUMN periods.end_time IS 'End time of the period.';