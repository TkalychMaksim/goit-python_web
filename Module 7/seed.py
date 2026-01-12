import random
from datetime import date, timedelta
from faker import Faker
from models import Group, Student, Teacher, Subject, Grade, Base

faker = Faker()
subjects_list = [
    "Computer Programming",
    "Data Structures and Algorithms",
    "Database Management Systems (DBMS)",
    "Software Engineering",
    "Operating Systems",
    "Computer Networks",
    "Web Development",
    "Mobile Application Development",
    "Cybersecurity",
    "Artificial Intelligence (AI)",
    "Machine Learning (ML)",
    "Cloud Computing",
    "Big Data Analytics",
    "Human-Computer Interaction (HCI)",
    "Software Testing and Quality Assurance (QA)",
    "DevOps",
    "Blockchain Technology",
    "Computer Graphics",
    "Embedded Systems",
    "Game Development"
]

def seed_data():
    session = SessionLocal()  

    try:
        groups = [Group(name=f"Group {i+1}") for i in range(3)]
        session.add_all(groups)
        session.commit()

        teachers = [Teacher(name=faker.name()) for _ in range(4)]
        session.add_all(teachers)
        session.commit()

        random_subjects = random.sample(subjects_list, 6) 
        subjects = [Subject(name=subject, teacher=random.choice(teachers)) for subject in random_subjects]
        session.add_all(subjects)
        session.commit()
        
        students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(35)]
        session.add_all(students)
        session.commit()

        for student in students:
            for subject in subjects:
                grades = [
                    Grade(
                        student=student,
                        subject=subject,
                        grade=random.randint(1, 5), 
                        date=date.today() - timedelta(days=random.randint(1, 365))
                    )
                    for _ in range(random.randint(5, 20)) 
                ]
                session.add_all(grades)

        session.commit()
    except Exception as e:
        session.rollback() 
        print(f"Error seeding data: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    seed_data()
