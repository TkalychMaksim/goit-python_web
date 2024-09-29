SELECT student_name, AVG(grade) AS avg_grade
FROM students
JOIN grades ON students.student_id = grades.student_id
WHERE subject_id = 3
GROUP BY student_name
ORDER BY avg_grade DESC
LIMIT 1;