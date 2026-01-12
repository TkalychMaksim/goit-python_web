from sqlalchemy.orm import Session
from config import SessionLocal
from models import Student, Grade, Teacher, Subject, Group
from sqlalchemy import func


session = SessionLocal()


def close_session():
    session.close()


def select_1():
    result = session.query(
        Student.name,
        func.avg(Grade.grade).label("average_grade")
    ).join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()
    return result


def select_2(subject_name):
    result = session.query(
        Student.name,
        func.avg(Grade.grade).label("average_grade")
    ).join(Grade).join(Subject).filter(Subject.name == subject_name).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()
    return result


def select_3(subject_name):
    result = session.query(
        Group.name,
        func.avg(Grade.grade).label("average_grade")
    ).join(Student, Group.id == Student.group_id)\
     .join(Grade, Student.id == Grade.student_id)\
     .join(Subject, Grade.subject_id == Subject.id)\
     .filter(Subject.name == subject_name)\
     .group_by(Group.id).all()
    return result


def select_4():
    result = session.query(
        func.avg(Grade.grade).label("average_grade")
    ).scalar()
    return result


def select_5(teacher_name):
    result = session.query(
        Subject.name
    ).join(Teacher).filter(Teacher.name == teacher_name).all()
    return result


def select_6(group_name):
    result = session.query(
        Student.name
    ).join(Group).filter(Group.name == group_name).all()
    return result


def select_7(group_name, subject_name):
    result = session.query(
        Student.name,
        Grade.grade
    ).join(Group).join(Grade).join(Subject).filter(
        Group.name == group_name,
        Subject.name == subject_name
    ).all()
    return result


def select_8(teacher_name):
    result = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Subject.id == Grade.subject_id)  # Зв'язок оцінки з предметом
        .join(Teacher, Teacher.id == Subject.teacher_id)  # Зв'язок предмета з викладачем
        .filter(Teacher.name == teacher_name)  # Фільтр за іменем викладача
        .scalar()
    )
    return result


def select_9(student_name):
    result = session.query(
        Subject.name
    ).join(Grade).join(Student).filter(Student.name == student_name).distinct().all()
    return result


def select_10(student_name, teacher_name):
    result = session.query(
        Subject.name
    ).join(Grade).join(Student).join(Teacher).filter(
        Student.name == student_name,
        Teacher.name == teacher_name
    ).distinct().all()
    return result


close_session()

result1 = select_1()
print(result1)
print("_-_-_-_-_-_-_-")
result2 = select_2("Cybersecurity")
print(result2)
print("_-_-_-_-_-_-_-")
result3 = select_3("Game Development")
print(result3)
print("_-_-_-_-_-_-_-")
result4 = select_4()
print(result4)
print("_-_-_-_-_-_-_-")
result5 = select_5("Miguel Carroll")
print(result5)
print("_-_-_-_-_-_-_-")
result6 = select_6("Group 1")
print(result6)
print("_-_-_-_-_-_-_-")
result7 = select_7("Group 1","Computer Graphics")
print(result7)
print("_-_-_-_-_-_-_-")
result8 = select_8("Leslie Mercer")
print(result8)
print("_-_-_-_-_-_-_-")
result9 = select_9("Billy Nash")
print(result9)
print("_-_-_-_-_-_-_-")
result10 = select_10("Melissa King", "Miguel Carroll")
print(result10)
