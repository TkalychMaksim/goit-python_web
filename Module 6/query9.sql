SELECT DISTINCT subject_name
FROM grades
JOIN subjects ON grades.subject_id = subjects.subject_id
WHERE student_id = 1;
