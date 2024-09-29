SELECT student_name, grade
FROM students
JOIN grades ON students.student_id = grades.student_id
WHERE group_id = 2
AND subject_id = 1; 
