few_shots = [
    {
        'Question': "What is the CGPA of Bilal Ahmed?",
        'SQLQuery': "SELECT cgpa FROM students WHERE name = 'Bilal Ahmed'",
        'SQLResult': "Result of the SQL query",
        'Answer': "2.10"
    },
    {
        'Question': "What is the average CGPA of students in the Computer Science department?",
        'SQLQuery': "SELECT AVG(cgpa) FROM students WHERE department = 'Computer Science'",
        'SQLResult': "Result of the SQL query",
        'Answer': "2.90"
    },
    {
        'Question': "Which students got an F grade in any course?",
        'SQLQuery': """SELECT s.name, e.course_name, e.grade
FROM students s JOIN enrollments e ON s.student_id = e.student_id
WHERE e.grade = 'F'""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Bilal Ahmed (Computer Networks), Usman Tariq (Project Management)"
    },
    {
        'Question': "What is the weighted GPA of Ali Raza based on his enrolled courses, where grade points are A=4.0, B=3.0, C=2.0, D=1.0, F=0.0, weighted by credit hours?",
        'SQLQuery': """SELECT s.name,
       SUM(CASE e.grade
           WHEN 'A' THEN 4.0 WHEN 'B' THEN 3.0 WHEN 'C' THEN 2.0
           WHEN 'D' THEN 1.0 ELSE 0.0 END * e.credit_hours) / SUM(e.credit_hours) AS weighted_gpa
FROM students s JOIN enrollments e ON s.student_id = e.student_id
WHERE s.name = 'Ali Raza'
GROUP BY s.name""",
        'SQLResult': "Result of the SQL query",
        'Answer': "3.43"
    },
    {
        'Question': "List all students who are on academic probation, where probation means CGPA below 2.5.",
        'SQLQuery': "SELECT name, cgpa FROM students WHERE cgpa < 2.5",
        'SQLResult': "Result of the SQL query",
        'Answer': "Bilal Ahmed (2.10), Usman Tariq (1.95), Fahad Nasir (2.40)"
    },
    {
        'Question': "Which course has the highest number of F grades?",
        'SQLQuery': """SELECT course_name, COUNT(*) as f_count
FROM enrollments
WHERE grade = 'F'
GROUP BY course_name
ORDER BY f_count DESC
LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Computer Networks"
    }
]