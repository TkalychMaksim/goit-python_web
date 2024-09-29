SELECT AVG(grade) AS avg_grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.subject_id
WHERE teacher_id = 2; 
