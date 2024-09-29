SELECT group_name, AVG(grade) AS avg_grade
FROM groups
JOIN students ON groups.group_id = students.group_id
JOIN grades ON students.student_id = grades.student_id
WHERE subject_id = 3 
GROUP BY group_name;