CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    credit_hours INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    score REAL NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

INSERT OR IGNORE INTO courses (course_id, course_name, credit_hours)
VALUES
    (1, 'Database', 3),
    (2, 'Programming', 3),
    (3, 'Artificial Intelligence', 3),
    (4, 'Information Systems', 3);

INSERT OR IGNORE INTO enrollments (student_id, course_id, semester, score)
VALUES
    (1001, 1, 1, 90),
    (1001, 2, 1, 85),
    (1002, 3, 1, 95),
    (1003, 4, 1, 65),
    (1004, 2, 1, 80),
    (1005, 4, 1, 60),
    (1006, 3, 1, 92);