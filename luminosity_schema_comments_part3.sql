
-- 🏫 periods
COMMENT ON TABLE periods IS 'Defines the daily schedule periods (e.g., "1st Period", "Lunch") including time bounds.';
COMMENT ON COLUMN periods.name IS 'Name of the period (e.g., "1st Period", "Lunch").';
COMMENT ON COLUMN periods.start_time IS 'Time the period starts (24-hour format).';
COMMENT ON COLUMN periods.end_time IS 'Time the period ends (24-hour format).';

-- 🏫 school_calendar
COMMENT ON TABLE school_calendar IS 'Tracks the school calendar for each date, including holidays and school days.';
COMMENT ON COLUMN school_calendar.calendar_date IS 'Specific date on the calendar.';
COMMENT ON COLUMN school_calendar.is_school_day IS 'Boolean: whether this date is a regular school day.';
COMMENT ON COLUMN school_calendar.is_holiday IS 'Boolean: whether this date is a holiday.';
COMMENT ON COLUMN school_calendar.holiday_name IS 'Name of the holiday, if applicable.';
COMMENT ON COLUMN school_calendar.comment IS 'Any notes or special information for this date.';

-- 🏢 classrooms
COMMENT ON TABLE classrooms IS 'List of classrooms or instructional spaces in the school buildings.';
COMMENT ON COLUMN classrooms.room_id IS 'Primary key: unique identifier for the room.';
COMMENT ON COLUMN classrooms.building IS 'Name of the building the room belongs to.';
COMMENT ON COLUMN classrooms.room_number IS 'Room number within the building.';

-- 💰 fee_types
COMMENT ON TABLE fee_types IS 'Defines types of student fees such as tuition, books, or activity fees.';
COMMENT ON COLUMN fee_types.name IS 'Name or description of the fee (e.g., Tuition, Lab Fee).';
COMMENT ON COLUMN fee_types.amount IS 'Amount charged for this fee type.';
COMMENT ON COLUMN fee_types.due_by IS 'Due date for the fee payment.';
COMMENT ON COLUMN fee_types.recurring IS 'Boolean: whether the fee is recurring.';

-- 💰 payments
COMMENT ON TABLE payments IS 'Records payments made by students toward fees.';
COMMENT ON COLUMN payments.amount_paid IS 'Dollar amount paid.';
COMMENT ON COLUMN payments.date_paid IS 'Date the payment was made.';

-- 🎯 attendance
COMMENT ON TABLE attendance IS 'Tracks student attendance for each school day.';
COMMENT ON COLUMN attendance.date IS 'Date of the attendance record.';
COMMENT ON COLUMN attendance.status IS 'Attendance status (e.g., Present, Absent, Tardy).';

-- 📝 discipline_reports
COMMENT ON TABLE discipline_reports IS 'Documents student discipline events and resulting actions.';
COMMENT ON COLUMN discipline_reports.date IS 'Date of the incident.';
COMMENT ON COLUMN discipline_reports.type IS 'Type of infraction (e.g., Cheating, Fighting).';
COMMENT ON COLUMN discipline_reports.severity IS 'Severity level of the incident.';
COMMENT ON COLUMN discipline_reports.action_taken IS 'Consequence issued (e.g., Detention, Suspension).';
COMMENT ON COLUMN discipline_reports.description IS 'Detailed narrative of the incident.';

-- 📊 standardized_tests
COMMENT ON TABLE standardized_tests IS 'Stores standardized test performance for students across subjects.';
COMMENT ON COLUMN standardized_tests.test_name IS 'Name of the standardized test (e.g., MAP, SAT).';
COMMENT ON COLUMN standardized_tests.test_date IS 'Date the test was administered.';
COMMENT ON COLUMN standardized_tests.subject IS 'Subject area covered by the test.';
COMMENT ON COLUMN standardized_tests.score IS 'Raw score earned by the student.';
COMMENT ON COLUMN standardized_tests.percentile IS 'Percentile rank relative to national norms.';
