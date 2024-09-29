SELECT student_name, AVG(grade) AS avg_grade
FROM students
JOIN grades ON students.student_id = grades.student_id
GROUP BY student_name
ORDER BY avg_grade DESC
LIMIT 5;
