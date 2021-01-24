import random

import pytz
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.fields import GenericRelation
from django.db import IntegrityError

from accounts.models import *
from announcements.models import *
from courses.models import *
from event_calendar.models import *
from home.models import *
from students.models import *

# Run using ./manage.py shell < common/sampledata.py


print("Starting...")
# Define groups
student_permissions = []
student_group = Group.objects.get_or_create(name="student")[0]
for permission in student_permissions:
    student_group.permissions.add(Permission.objects.get(codename=permission))

staff_permissions = [
    "add_profile", "change_profile", "delete_profile", "view_profile",
    "add_course", "change_course", "delete_course", "view_course", "change_module",
    "add_assignment", "change_assignment", "delete_assignment", "view_assignment",
    "can_accept", "can_reject",
    "can_add",
]
staff_group = Group.objects.get_or_create(name="staff")[0]
for permission in staff_permissions:
    staff_group.permissions.add(Permission.objects.get(codename=permission))
print("Created Groups")

# Profile class (Auth user)
admin = Profile.objects.get_or_create_superuser("admin1", "admin1@email.com", "account")[0]
admin.first_name = "Admin"
admin.last_name = "The Guy"
admin.save()

account = Profile.objects.get_or_create_user("u1", "account@email.com", "account")[0]
account.first_name = "Account"
account.last_name = "Person"
account.save()

student1 = Profile.objects.get_or_create_user("u2", "student1@email.com", "account")[0]
student_group.user_set.add(student1)
student1.first_name = "Student1"
student1.last_name = "Person"
student1.save()

student2 = Profile.objects.get_or_create_user("u3", "student2@email.com", "account")[0]
student_group.user_set.add(student2)
student2.first_name = "Student2"
student2.last_name = "Person"
student2.save()

student3 = Profile.objects.get_or_create_user("u4", "student3@email.com", "account")[0]
student_group.user_set.add(student3)
student3.first_name = "Student3"
student3.last_name = "Person"
student3.save()

staff = Profile.objects.get_or_create_user("u5", "staff@email.com", "account")[0]
staff_group.user_set.add(staff)
staff.first_name = "Staff"
staff.last_name = "Person"
staff.save()

studentstaff = Profile.objects.get_or_create_user("u6", "studentstaff@email.com", "account")[0]
student_group.user_set.add(studentstaff)
staff_group.user_set.add(studentstaff)
studentstaff.first_name = "Studentstaff"
studentstaff.last_name = "Person"
studentstaff.save()
print("Created Users")

# Subject class
mathematics = Subject.objects.get_or_create(title="Mathematics", slug="mathematics")[0]
physics = Subject.objects.get_or_create(title="Physics", slug="physics")[0]
biology = Subject.objects.get_or_create(title="Biology", slug="biology")[0]
literature = Subject.objects.get_or_create(title="Literature", slug="literature")[0]
print("Created Subjects")

# Course class DEPENDS ON User, Subject
core_maths = Course.objects.get_or_create(owner=admin, subject=mathematics,
                                          title="Core Maths", slug="core_maths",
                                          overview="Fundamentals of mathematics")[0]
core_maths.students.add(student1)
core_maths.students.add(student2)
core_maths.students.add(student3)
core_maths.students.add(studentstaff)
advanced_maths = Course.objects.get_or_create(owner=admin, subject=mathematics,
                                              title="Advanced Maths", slug="advanced_maths",
                                              overview="A more advanced course on mathematics")[0]
advanced_maths.students.add(student1)
advanced_maths.students.add(student2)
advanced_maths.students.add(studentstaff)
computer_science = Course.objects.get_or_create(owner=staff, subject=mathematics,
                                                title="Computer Science", slug="computer_science",
                                                overview="The good one")[0]
computer_science.students.add(student2)

natural_sciences = Course.objects.get_or_create(owner=staff, subject=physics,
                                                title="Natural Sciences", slug="natural_sciences",
                                                overview="Fundamentals of the natural sciences")[0]
natural_sciences.students.add(student1)
natural_sciences.students.add(student3)
theoretical_physics = Course.objects.get_or_create(owner=staff, subject=physics,
                                                   title="Theoretical Physics", slug="theoretical_physics",
                                                   overview="Physics. But that's just a theory. A PHYSICS THEORY")[0]
theoretical_physics.students.add(student3)
harry_potter = Course.objects.get_or_create(owner=studentstaff, subject=physics,
                                            title="Harry Potter", slug="why",
                                            overview="Why is this a real thing? Why is this here?"
                                                     " IT'S NOT EVEN PHYSICS!")[0]
harry_potter.students.add(student2)
harry_potter.students.add(studentstaff)

basic_biology = Course.objects.get_or_create(owner=staff, subject=biology,
                                             title="Basic Biology", slug="basic_biology",
                                             overview="Fundamentals of biology")[0]
basic_biology.students.add(student3)
medical_science = Course.objects.get_or_create(owner=staff, subject=biology,
                                               title="Medical Science", slug="medical_science",
                                               overview="Specialised course in medicinal science")[0]
medical_science.students.add(student1)
medical_science.students.add(student2)
medical_science.students.add(student3)

basic_literature = Course.objects.get_or_create(owner=admin, subject=literature,
                                                title="Basic Literature", slug="basic_literature",
                                                overview="Fundamental reading and writing skills")[0]
basic_literature.students.add(student1)
basic_literature.students.add(student3)
fitness_gram = Course.objects.get_or_create(owner=studentstaff, subject=literature,
                                            title="Fitnessgram Pacer Test", slug="fitnessgram_pacer_test",
                                            overview="I mean, in a way it IS literature. Technically.")[0]
fitness_gram.students.add(student2)
fitness_gram.students.add(student3)
fitness_gram.students.add(studentstaff)
longest_word = Course.objects.get_or_create(owner=studentstaff, subject=literature,
                                            title="The Longest Word", slug="the_longest_word",
                                            overview="Antidisestablishmentarianism")[0]
longest_word.students.add(student1)
longest_word.students.add(studentstaff)
print("Created Courses")

# AccountSubmission class DEPENDS ON Course
AccountSubmission.objects.get_or_create(course=core_maths, email="new.person@email.com")
AccountSubmission.objects.get_or_create(course=core_maths, email="newer.person@email.com")
AccountSubmission.objects.get_or_create(course=core_maths, email="newest.person@email.com")

AccountSubmission.objects.get_or_create(course=medical_science, email="iwannamedic@email.com")

AccountSubmission.objects.get_or_create(course=longest_word, email="legit.man@email.com")
print("Create Account Submissions")

# Announcements class DEPENDS ON User, Course
Announcement.objects.get_or_create(title="Welcome", author=core_maths.owner, course=core_maths,
                                   content="Welcome to the core maths course")
Announcement.objects.get_or_create(title="Did you know?", author=core_maths.owner, course=core_maths,
                                   content="Did you know 1+4=6?")
Announcement.objects.get_or_create(title="Correction", author=core_maths.owner, course=core_maths,
                                   content="Sorry, it was 4 not 6. My bad.")
Announcement.objects.get_or_create(title="sjdhfojhashduaiodshfadh", author=core_maths.owner, course=core_maths,
                                   content="I am having a day.")

Announcement.objects.get_or_create(title="Welcome", author=advanced_maths.owner, course=advanced_maths,
                                   content="Welcome to the advanced maths course")

Announcement.objects.get_or_create(title="Welcome", author=computer_science.owner, course=computer_science,
                                   content="Welcome to the computer science course")

Announcement.objects.get_or_create(title="Welcome", author=natural_sciences.owner, course=natural_sciences,
                                   content="Welcome to the natural sciences course")

Announcement.objects.get_or_create(title="Welcome", author=theoretical_physics.owner, course=theoretical_physics,
                                   content="Welcome to the theoretical physics course")

Announcement.objects.get_or_create(title="Welcome", author=harry_potter.owner, course=harry_potter,
                                   content="Welcome to the harry potter course")

Announcement.objects.get_or_create(title="Welcome", author=basic_biology.owner, course=basic_biology,
                                   content="Welcome to the basic biology course")

Announcement.objects.get_or_create(title="Welcome", author=medical_science.owner, course=medical_science,
                                   content="Welcome to the medical science course")
Announcement.objects.get_or_create(title="Actual Longest Word", author=medical_science.owner, course=medical_science,
                                   content="Prof. Studentstaff claims antidisestablishmentarianism is the longest word."
                                           " I disagree with this sentiment. The longest word is clearly "
                                           "pnumonoultramicroscopicsilicovolcanoconiosis")
Announcement.objects.get_or_create(title="Staff Is A Nerd", author=studentstaff, course=medical_science,
                                   content="Nuh uh, Antidisestablishmentarianism is clearly better!")
Announcement.objects.get_or_create(title="A Disagreement", author=medical_science.owner, course=medical_science,
                                   content="This is not a competition of the better word, rather it is a competition of"
                                           " length. In this regard pneumonoultramicroscopicsilicovolcanoconiosis is"
                                           " clearly superior.")
Announcement.objects.get_or_create(title="Gottem", author=studentstaff, course=medical_science,
                                   content="You're not a competition of the better word!")
Announcement.objects.get_or_create(title="Warning", author=admin, course=medical_science,
                                   content="This is an announcement board, not your private DM's. Stop acting like"
                                           " children and take this discussion elsewhere")

Announcement.objects.get_or_create(title="Welcome", author=basic_literature.owner, course=basic_literature,
                                   content="Welcome to the basic literature course")

Announcement.objects.get_or_create(title="Welcome", author=fitness_gram.owner, course=fitness_gram,
                                   content="Welcome to the fitnessgram pacer test course")

Announcement.objects.get_or_create(title="Welcome", author=longest_word.owner, course=longest_word,
                                   content="What are you doing here? I already told you my longest word.")
Announcement.objects.get_or_create(title="Do A Flip", author=longest_word.owner, course=longest_word,
                                   content="Do a flip!")
Announcement.objects.get_or_create(title="PSA", author=admin, course=longest_word,
                                   content="Please refrain from performing backflips on the courtyard.")
print("Created Announcements")

# Module class DEPENDS ON Course
arithmetic = Module.objects.get_or_create(course=core_maths, title="Arithmetic", order=1,
                                          description="Basic numbers and arithmetic operations")[0]
trigonometry = Module.objects.get_or_create(course=core_maths, title="Trigonometry", order=2,
                                            description="Basically just pythagoras' theorem")[0]

algebra = Module.objects.get_or_create(course=advanced_maths, title="Algebra", order=1,
                                       description="Basics of algebra.")[0]
calculus = Module.objects.get_or_create(course=advanced_maths, title="Calculus", order=2,
                                        description="Basics of derivation and integration.")[0]
statistics = Module.objects.get_or_create(course=advanced_maths, title="Statistics", order=3,
                                          description="Fundamental statistical concepts and operations")[0]

sets = Module.objects.get_or_create(course=computer_science, title="Sets", order=1,
                                    description="I think this is a course we did last year")[0]
python = Module.objects.get_or_create(course=computer_science, title="Python", order=2,
                                      description="Can't remember what this even is")[0]
java = Module.objects.get_or_create(course=computer_science, title="Python", order=3,
                                    description="I do like a good cup of coffee just before bed")[0]
databases = Module.objects.get_or_create(course=computer_science, title="Databases", order=4,
                                         description="I think databases are a myth")[0]
architecture = Module.objects.get_or_create(course=computer_science, title="Architecture", order=5,
                                            description="Ah yes! I definitely know this one ;)."
                                                        " No lies here :P. None XD")[0]

boglogy = Module.objects.get_or_create(course=natural_sciences, title="Boglogy", order=1,
                                       description="We did this in school")[0]
physik = Module.objects.get_or_create(course=natural_sciences, title="Physik", order=2,
                                      description="I think this is the hard one")[0]
dru__ = Module.objects.get_or_create(course=natural_sciences, title="Dru**", order=3,
                                     description="I think I misread something. Is that the police?")[0]

astrophysics = Module.objects.get_or_create(course=theoretical_physics, title="Astrophysics", order=1,
                                            description="Modelling and understanding the wonders of the cosmos")[0]
quantum_mechanics = Module.objects.get_or_create(course=theoretical_physics, title="Quantum Mechanics", order=2,
                                                 description="Understanding the nature of the very small")[0]

what = Module.objects.get_or_create(course=harry_potter, title="What Even?", order=1,
                                    description="What do they even do in this course?")[0]

human_body = Module.objects.get_or_create(course=basic_biology, title="The Human Body", order=1,
                                          description="Functions and anatomy of the"
                                                      " different parts that make up a human")[0]
genealogy = Module.objects.get_or_create(course=basic_biology, title="Genealogy", order=2,
                                         description="The science behind evolution and the passing on of traits")[0]

advanced_anatomy = Module.objects.get_or_create(course=medical_science, title="Advanced Anatomy", order=1,
                                                description="An advanced overview of the human anatomy")[0]
medical_techniques = Module.objects.get_or_create(course=medical_science, title="Medical Techniques", order=2,
                                                  description="Imma be real with you, I really don't know what subjects"
                                                              " they do in medical sciences. I'm a programmer not a"
                                                              " doctor.")[0]

spelling = Module.objects.get_or_create(course=basic_literature, title="Spelling", order=1,
                                        description="Correct spelling and usage of words")[0]
lord_of_the_flies = Module.objects.get_or_create(course=basic_literature, title="Lord Of The Flies", order=2,
                                                 description="I swear I've read more books than just this...")[0]

fitness = Module.objects.get_or_create(course=fitness_gram, title="The Fitnessgram Pacer Test", order=1,
                                       description="The FitnessGram™ Pacer Test is a multistage aerobic capacity test"
                                                   " that progressively gets more difficult as it continues. The 20"
                                                   " meter pacer test will begin in 30 seconds. Line up at the start."
                                                   " The running speed starts slowly, but gets faster each minute after"
                                                   " you hear this signal. [beep] A single lap should be completed each"
                                                   " time you hear this sound. [ding] Remember to run in a straight"
                                                   " line, and run as long as possible. The second time you fail to"
                                                   " complete a lap before the sound, your test is over. The test will"
                                                   " begin on the word start. On your mark, get ready, start.")[0]
summit = Module.objects.get_or_create(course=fitness_gram, title="Not The Fitnessgram Pacer Test", order=2,
                                      description="This is not the FitnessGram™ Pacer Test."
                                                  " A multistage aerobic capacity test"
                                                  " that progressively gets more difficult as it continues. The 20"
                                                  " meter pacer test will begin in 30 seconds. Line up at the start."
                                                  " The running speed starts slowly, but gets faster each minute after"
                                                  " you hear this signal. [beep] A single lap should be completed each"
                                                  " time you hear this sound. [ding] Remember to run in a straight"
                                                  " line, and run as long as possible. The second time you fail to"
                                                  " complete a lap before the sound, your test is over. The test will"
                                                  " begin on the word start. On your mark, get ready, start.")[0]

knowledge = Module.objects.get_or_create(course=longest_word, title="Now You Know", order=1,
                                         description="Now you know the longest word")[0]
print("Created Modules")

# Assignment class DEPENDS ON module
# AssignmentContent class DEPENDS ON assignment
# Text class DEPENDS ON User
AssignmentContent.objects.all().delete()
arithmetic_a1 = Assignment.objects.get_or_create(module=arithmetic, title="Basic sums", order=1,
                                                 description="Answer the following and submit in a text document.")[0]
AssignmentContent.objects.create(
    assignment=arithmetic_a1, order=1,
    item=Text.objects.get_or_create(
        owner=arithmetic_a1.module.course.owner,
        content="What is 420 - 69?",
        title="q1"
    )[0]
)
AssignmentContent.objects.create(
    assignment=arithmetic_a1, order=2,
    item=Text.objects.get_or_create(
        owner=arithmetic_a1.module.course.owner,
        content="What is 8000000 + 8135",
        title="q2"
    )[0]
)
arithmetic_a2 = Assignment.objects.get_or_create(module=arithmetic, title="Less basic sums", order=2,
                                                 description="What is 69 - 420?")[0]
arithmetic_a3 = Assignment.objects.get_or_create(module=arithmetic, title="Lesserer basic sums", order=2,
                                                 description="What is 4(92-36(528*14-1+1)-(16+2e))+1?")[0]

trigonometry_a1 = Assignment.objects.get_or_create(module=trigonometry, title="Pythagoras", order=1,
                                                   description="What is Pythagoras' theorem?")[0]
trigonometry_a2 = Assignment.objects.get_or_create(module=trigonometry, title="Basic Trig", order=1,
                                                   description="")[0]

algebra_a1 = Assignment.objects.get_or_create(module=algebra, title="Simple algebra", order=1,
                                              description="Given x = 20y - 4 and y = 16x, find x.")[0]

calculus_a1 = Assignment.objects.get_or_create(module=calculus, title="Differentiation", order=1,
                                               description="What is the derivation of y = 10(21x^2 + 6.9x) + 1")[0]

statistics_a1 = Assignment.objects.get_or_create(module=statistics, title="String", order=1,
                                                 description="How long is this piece of string?")[0]

sets_a1 = Assignment.objects.get_or_create(module=sets, title="Subsets?", order=1,
                                           description="Set the subset of this set's"
                                                       " sets to set setting sets in sets")[0]

python_a1 = Assignment.objects.get_or_create(module=python, title="Who knows?", order=1,
                                             description="Surprise me")[0]

java_a1 = Assignment.objects.get_or_create(module=java, title="Coffee", order=1,
                                           description="Get me a cup of coffee. This will be on your exam.")[0]

architecture_a1 = Assignment.objects.get_or_create(module=architecture, title="Build it", order=1,
                                                   description="Build a computer. A whole computer.")[0]

boglogy_a1 = Assignment.objects.get_or_create(module=boglogy, title="Wot", order=1,
                                              description="Wot izza hoomin bean??!")[0]

physik_a1 = Assignment.objects.get_or_create(module=physik, title="Hou", order=1,
                                             description="Hou blok do da floor smashing?!?")[0]

dru___a1 = Assignment.objects.get_or_create(module=dru__, title="Brooooooo", order=1,
                                            description="Like, what is up my dude. My main man."
                                                        " My primary individual.")[0]

astrophysics_a1 = Assignment.objects.get_or_create(module=astrophysics, title="Newton", order=1,
                                                   description="Name each of Newton's laws of motion")[0]

quantum_mechanics_a1 = Assignment.objects.get_or_create(module=quantum_mechanics, title="Quarks", order=1,
                                                        description="Name each of the quarks")[0]

what_a1 = Assignment.objects.get_or_create(module=what, title="Umm", order=1,
                                           description="Read chapter 1 I guess?")[0]

human_body_a1 = Assignment.objects.get_or_create(module=human_body, title="Assignment 1", order=1,
                                                 description="Given x=19x-27z^2, the speed of light c=300Mm/s, and the"
                                                             " melting point of ice m0=273.15K"
                                                             " what is the surface area of the Sun?")[0]

genealogy_a1 = Assignment.objects.get_or_create(module=genealogy, title="Ancestry", order=1,
                                                description="Where are my parents?")[0]

advanced_anatomy_a1 = Assignment.objects.get_or_create(module=advanced_anatomy, title="Crab", order=1,
                                                       description="Dissect the stomatogastric ganglion"
                                                                   " from this crab.")[0]

medical_techniques_a1 = Assignment.objects.get_or_create(module=medical_techniques, title="Qualifications", order=1,
                                                         description="I am not qualified to even try"
                                                                     " make a question for this")[0]

spelling_a1 = Assignment.objects.get_or_create(module=spelling, title="Spelling test", order=1,
                                               description="Spell this word (book).")[0]

lord_of_the_flies_a1 = Assignment.objects.get_or_create(module=lord_of_the_flies, title="Analysis", order=1,
                                                        description="Describe the phallic nature of the pink rocks.")[0]

fitness_a1 = Assignment.objects.get_or_create(module=fitness, title="Do a front flip", order=1,
                                              description="Maybe not. I hear it's kinda dangerous."
                                                          " Do a back flip instead")[0]
fitness_a2 = Assignment.objects.get_or_create(module=fitness, title="Do a back flip", order=2,
                                              description="These are perfectly safe")[0]

summit_a1 = Assignment.objects.get_or_create(module=summit, title="Do a funny dance", order=1,
                                             description="Make me laugh.")[0]

knowledge_a1 = Assignment.objects.get_or_create(module=knowledge, title="Know", order=1,
                                                description="Show you know what you know.")[0]
print("Created Assignments")

start = timezone.datetime(2020, 9, 16, tzinfo=pytz.UTC)
end = timezone.now()
delta = int((end - start).total_seconds())
for student in (s for s in Profile.objects.all() if s.is_student):
    for assignment in Assignment.objects.all():
        if random.random() > 0.2:
            rdate = start + timezone.timedelta(seconds=random.randint(0, delta))
            sdate = rdate - timezone.timedelta(seconds=random.randint(delta - 86400, delta - 3600))
            edate = sdate + timezone.timedelta(seconds=random.randint(300, 3300))
            Grade.objects.get_or_create(student=student, assignment=assignment, grade=random.randint(0, 100),
                                        datetime_started=sdate, datetime_submitted=edate,
                                        teacher=assignment.module.course.owner)
print("Assigned Grades")
