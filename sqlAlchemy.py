from datetime import datetime
from time import time

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import orm

engine = create_engine('mysql+mysqlconnector://root:12345@localhost:3306/обд')

Base = declarative_base()

userRole = Table('project-user', Base.metadata,
                 Column('project_id', Integer, ForeignKey('project.id')),
                 Column('user_id', Integer, ForeignKey('user.id'))
                 )

artefactRole = Table('task-artefact', Base.metadata,
                     Column('task_id', Integer, ForeignKey('task.id')),
                     Column('artefact_id', Integer, ForeignKey('artefact.id'))
                     )


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=45))
    description = Column(String(length=45))
    children = relationship("Task")
    children2 = relationship("User", secondary=userRole)

    def __repr__(self):
        return f"<User(name='{self.name}', description='{self.description}')>"


class Artefact(Base):
    __tablename__ = 'artefact'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=45))
    file = Column(String(length=45))

    def __repr__(self):
        return f"<User(name='{self.name}', file='{self.file}')>"


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=45))
    role = Column(String(length=45))
    email = Column(String(length=45))
    children = relationship("Task")

    def __repr__(self):
        return f"<User(name='{self.name}', role='{self.role}', email='{self.email}')>"


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=45))
    role = Column(String(length=45))
    description = Column(String(length=45))
    time = Column(DATETIME)
    project_id = Column(Integer, ForeignKey('project.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    children2 = relationship("Artefact", secondary=artefactRole)

    def __repr__(self):
        return f"<User(name='{self.name}', role='{self.role}', description='{self.description}', time='{self.time}', " \
               f"project_id='{self.project_id}', user_id='{self.user_id}')> "


# Create a session
Session = orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# Create project
# for i in range(1, 101):
#     session.add(Project(name=f'Project num {i}', description=f'Description num {i}'))
# # session.commit()

# Add a users
# session.add(User(name='Pasha', role='Boss', email='pasha.akaBoss@gmail.com'))
# session.add(User(name='Danya', role='Ashka', email='danya.don@gmail.com'))
# session.add(User(name='Vanya', role='prostoVanya', email='prostoVanya.akaVanya@gmail.com'))
# session.add(User(name='Bogdan', role='Bogomol', email='bogomol.akaKungfu@gmail.com'))
# # session.commit()


# Add a artefacts

# session.add(Artefact(name='ORM',file='C:\\Project1\\Stakeholder requests.md'))
# session.add(Artefact(name='UMLTeamLead',file='C:\\Project1\\Stakeholder requests.md'))
# session.add(Artefact(name='UMLAnalytics',file='C:\\Project1\\Stakeholder requests.md'))
# session.add(Artefact(name='rules',file='C:\\Project1\\Main Points.md'))
# session.add(Artefact(name='UMLDesigned',file='C:\\Project1\\Stakeholder requests.md'))
# session.commit()


# Add Tasks

# session.add(Task(name='Task 1', role='Boss', description='Description 1', time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=1))
# session.add(Task(name='Task 2', role='Ashka', description='Description 2',time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=2))
# session.add(Task(name='Task 3', role='prostoVanya', description='Description 3', time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=3))
# session.add(Task(name='Task 4', role='Bogomol', description='Description 4', time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=4))
# session.add(Task(name='Task 5', role='Boss', description='Description 5', time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=1))
# session.add(Task(name='Task 6', role='Ashka', description='Description 6', time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=2))
# session.add(Task(name='Task 7', role='prostoVanya', description='Description 7', time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=3))
# session.add(Task(name='Task 8', role='Bogomol', description='Description 8', time=datetime(year=2016, month=2, day=3, hour=2), project_id=1, user_id=4))
# session.commit()


# sql = text('select * from table1 WHERE table1.id BETWEEN 120 AND 125')
# result = engine.execute(sql)
# names = [row for row in result]
# print(*names, sep='\n')


# for i in range(1, 111):
#     session.query(Task).filter_by(id=i).delete()
# session.commit()

# # Query the user
# our_user = session.query(Table1).order_by("").all()
# print('\nOur User:')
# print('Nick name in hex: {0}'.format(our_user.nickname.encode('utf-8')))
# session.query(User)
