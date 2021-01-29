import random
import urllib
from urllib.request import urlopen

import pytz
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import IntegrityError
from django.templatetags.static import static

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
    "accept_account_submissions", "reject_account_submissions", "add_account_submissions",
]
staff_group = Group.objects.get_or_create(name="staff")[0]
for permission in staff_permissions:
    print(permission)
    staff_group.permissions.add(Permission.objects.get(codename=permission))
print("Created Groups")

# Profile class (Auth user)
admin = Profile.objects.get_or_create_superuser("admin1", "admin1@email.com", "account")[0]
admin.first_name = "Admin"
admin.last_name = "The Guy"
admin.phone_number = "12345678900"
admin.term_address = "Admins don't have houses. They live in the website!"
admin.save()

account = Profile.objects.get_or_create_user("u1", "account@email.com", "account")[0]
account.first_name = "Account"
account.last_name = "Person"
account.phone_number = "Did I do this right?"
account.term_address = "A location, in a place."
account.save()

student1 = Profile.objects.get_or_create_user("u2", "student1@email.com", "account")[0]
student_group.user_set.add(student1)
student1.first_name = "Student1"
student1.last_name = "Person"
student1.phone_number = "00000000000"
student1.term_address = "Who even knows?"
student1.save()

student2 = Profile.objects.get_or_create_user("u3", "student2@email.com", "account")[0]
student_group.user_set.add(student2)
student2.first_name = "Student2"
student2.last_name = "Person"
student2.phone_number = "11111111111"
student2.term_address = "Somewhere"
student2.save()

student3 = Profile.objects.get_or_create_user("u4", "student3@email.com", "account")[0]
student_group.user_set.add(student3)
student3.first_name = "Student3"
student3.last_name = "Person"
student3.phone_number = "22222222222"
student3.term_address = "What does it even mean to live? Can we truly define ourselves" \
                     " merely based on a location we refer to as home?"
student3.save()

staff = Profile.objects.get_or_create_user("u5", "staff@email.com", "account")[0]
staff_group.user_set.add(staff)
staff.first_name = "Staff"
staff.last_name = "Person"
staff.phone_number = "33333333333"
staff.term_address = "Somewhere"
staff.save()

studentstaff = Profile.objects.get_or_create_user("u6", "studentstaff@email.com", "account")[0]
student_group.user_set.add(studentstaff)
staff_group.user_set.add(studentstaff)
studentstaff.first_name = "Studentstaff"
studentstaff.last_name = "Person"
studentstaff.phone_number = "800813542069"
studentstaff.term_address = "Do you like pancakes?"
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

Announcement.objects.get_or_create(title="Good Evening", author=advanced_maths.owner, course=advanced_maths,
                                   content="Why hello there my good chaps. Many welcomes to the fantastical Advanced"
                                           " Mathematics course. Please enjoy your stay")
Announcement.objects.get_or_create(title="How do you do?", author=advanced_maths.owner, course=advanced_maths,
                                   content="Why hello there my good chaps. How do you do this fine evening? Have you"
                                           " completed all your homework? Did you sleep enough last night? Consider"
                                           " your answers carefully, this will be on the exam.")

Announcement.objects.get_or_create(title="Welcome", author=computer_science.owner, course=computer_science,
                                   content="Welcome")
Announcement.objects.get_or_create(title="Game", author=computer_science.owner, course=computer_science,
                                   content="I have a game")
Announcement.objects.get_or_create(title="Game 2. Electric boogaloo.", author=computer_science.owner, course=computer_science,
                                   content="I played a game")
Announcement.objects.get_or_create(title="Game 3. In 3D.", author=computer_science.owner, course=computer_science,
                                   content="I won a game")
Announcement.objects.get_or_create(title="Game 5. The Empire Strikes Back.", author=computer_science.owner, course=computer_science,
                                   content="I ate the game")
Announcement.objects.get_or_create(title="Game 6.", author=computer_science.owner, course=computer_science,
                                   content="Don't ask about game 4.")

Announcement.objects.get_or_create(title="Welcome", author=natural_sciences.owner, course=natural_sciences,
                                   content="What is up man. Let us make love, not war, and join together to extend our"
                                           " chakras to reach the next plane of reality.")

Announcement.objects.get_or_create(title="Welcome", author=theoretical_physics.owner, course=theoretical_physics,
                                   content="Welcome to the theoretical physics course")
Announcement.objects.get_or_create(title="Theory", author=theoretical_physics.owner, course=theoretical_physics,
                                   content="The Earth is clearly flat. Look at the horizon. Do you see a curve?")
Announcement.objects.get_or_create(title="Response", author=studentstaff, course=theoretical_physics,
                                   content="I have taken a microscope and pointed it at a basket ball. By observing the"
                                           " horizon at a zoomed in scale proportional to the scale of a human to the"
                                           " Earth one can see no visible curve. Therefore by all science, basketballs"
                                           " are flat.")

Announcement.objects.get_or_create(title="Welcome", author=harry_potter.owner, course=harry_potter,
                                   content="Welcome to the harry potter course")
Announcement.objects.get_or_create(title="Day 1", author=harry_potter.owner, course=harry_potter,
                                   content="They haven't noticed my infiltration.")
Announcement.objects.get_or_create(title="Day 2", author=harry_potter.owner, course=harry_potter,
                                   content="They still think I'm actually studentstaff.")
Announcement.objects.get_or_create(title="Day 9", author=harry_potter.owner, course=harry_potter,
                                   content="This is starting to get boring.")
Announcement.objects.get_or_create(title="Day 57", author=harry_potter.owner, course=harry_potter,
                                   content="I think they're on to me. They're starting to look at me funny.")
Announcement.objects.get_or_create(title="Day 56", author=harry_potter.owner, course=harry_potter,
                                   content="Nevermind. I just forgot my eyebrows at home.")
Announcement.objects.get_or_create(title="Day 192", author=harry_potter.owner, course=harry_potter,
                                   content="I am starting to question myself. Who am I really? Am I an imposter? Or"
                                           " perhaps...")
Announcement.objects.get_or_create(title="Day 242", author=harry_potter.owner, course=harry_potter,
                                   content="paint")
Announcement.objects.get_or_create(title="Day 491", author=harry_potter.owner, course=harry_potter,
                                   content="I have accepted my position as an actual member of staff in this school. I"
                                           " don't know when things changed, or if they ever did. At this point I don't"
                                           " care. I'm just going to do some school stuff now. I am studentstaff.")

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
Announcement.objects.get_or_create(title="PSA", author=basic_literature.owner, course=basic_literature,
                                   content="It has come to my attention that many students in this school are unable to"
                                           " read or write. If this refers to you please send me an email to sign up"
                                           " for extracurricular english writing lessons.")

Announcement.objects.get_or_create(title="Welcome", author=fitness_gram.owner, course=fitness_gram,
                                   content="The FitnessGram™ Pacer Test is a multistage aerobic capacity test that"
                                           " progressively gets more difficult as it continues.")
Announcement.objects.get_or_create(title="Step 1", author=fitness_gram.owner, course=fitness_gram,
                                   content="The 20 meter pacer test will begin in 30 seconds. Line up at the start.")
Announcement.objects.get_or_create(title="Step 2", author=fitness_gram.owner, course=fitness_gram,
                                   content="The running speed starts slowly, but gets faster each minute after you "
                                           "hear this signal. [beep]")
Announcement.objects.get_or_create(title="Step 3", author=fitness_gram.owner, course=fitness_gram,
                                   content="A single lap should be completed each time you hear this sound. [ding]")
Announcement.objects.get_or_create(title="Step 4", author=fitness_gram.owner, course=fitness_gram,
                                   content="Remember to run in a straight line, and run as long as possible.")
Announcement.objects.get_or_create(title="Step 5", author=fitness_gram.owner, course=fitness_gram,
                                   content="The second time you fail to complete a lap before the sound, your test is"
                                           " over.")
Announcement.objects.get_or_create(title="Step 6", author=fitness_gram.owner, course=fitness_gram,
                                   content="The test will begin on the word start. On your mark, get ready, start.")

Announcement.objects.get_or_create(title="Welcome", author=longest_word.owner, course=longest_word,
                                   content="What are you doing here? I already told you my longest word.")
Announcement.objects.get_or_create(title="Do A Flip", author=longest_word.owner, course=longest_word,
                                   content="Do a flip!")
Announcement.objects.get_or_create(title="PSA", author=admin, course=longest_word,
                                   content="Please refrain from performing backflips on the courtyard.")
print("Created Announcements")

# Module class DEPENDS ON Course
# ModuleContent class DEPENDS ON module
# Text class DEPENDS ON User
ModuleContent.objects.all().delete()
arithmetic = Module.objects.get_or_create(course=core_maths, title="Arithmetic", order=1,
                                          description="Basic numbers and arithmetic operations")[0]
ModuleContent.objects.create(
    module=arithmetic, order=1,
    item=Text.objects.get_or_create(
        owner=arithmetic.course.owner,
        content="To truly comprehend the question that is 'What is 1 + 1?', we must first ask the question; why do we"
                " truly want to know 1 + 1? What benefit do we gain from this knowledge? How does this make us feel?"
                " Only then can we truly enter a stat of mind in which 'What is 1 + 1' has a profound, and powerful"
                " answer.",
        title="What is 1 + 1?",
    )[0]
)
ModuleContent.objects.create(
    module=arithmetic, order=2,
    item=Text.objects.get_or_create(
        owner=arithmetic.course.owner,
        content="Vandals stole my lecture. Sorry.",
        title="The true meaning of 1 + 1",
    )[0]
)
trigonometry = Module.objects.get_or_create(course=core_maths, title="Trigonometry", order=2,
                                            description="Basically just pythagoras' theorem")[0]
ModuleContent.objects.create(
    module=trigonometry, order=1,
    item=Text.objects.get_or_create(
        owner=trigonometry.course.owner,
        content="a² + b² = c².\n That's it. That's the entire module. Mabye a triangle or two for good measure",
        title="The entire module",
    )[0]
)

algebra = Module.objects.get_or_create(course=advanced_maths, title="Algebra", order=1,
                                       description="Basics of algebra.")[0]
ModuleContent.objects.create(
    module=algebra, order=1,
    item=Text.objects.get_or_create(
        owner=algebra.course.owner,
        content="888 + 88 + 8 + 8 + 8 = 1000.\nNow you know.",
        title="Eights",
    )[0]
)
ModuleContent.objects.create(
    module=algebra, order=2,
    item=Text.objects.get_or_create(
        owner=algebra.course.owner,
        content="1 + 2 + 3 = 1 x 2 x 3.\nNow you know.",
        title="Multiply",
    )[0]
)
ModuleContent.objects.create(
    module=algebra, order=3,
    item=Text.objects.get_or_create(
        owner=algebra.course.owner,
        content="If one ship can cross the pacific in six days, how long will it take for six ships?",
        title="Homework",
    )[0]
)
calculus = Module.objects.get_or_create(course=advanced_maths, title="Calculus", order=2,
                                        description="Basics of derivation and integration.")[0]
ModuleContent.objects.create(
    module=calculus, order=1,
    item=Text.objects.get_or_create(
        owner=calculus.course.owner,
        content="888 + 88 + 8 + 8 + 8 = 1000.\nNow you knowledge.",
        title="Eights",
    )[0]
)
ModuleContent.objects.create(
    module=calculus, order=2,
    item=Text.objects.get_or_create(
        owner=calculus.course.owner,
        content="1 + 2 + 3 = 1 x 2 x 3.\nI'm not copying anyone. You are.",
        title="Multiply",
    )[0]
)
ModuleContent.objects.create(
    module=calculus, order=3,
    item=Text.objects.get_or_create(
        owner=calculus.course.owner,
        content="If one ship can cross the pacific in six days, how long will it take for my pizza to cook?",
        title="Homework",
    )[0]
)
statistics = Module.objects.get_or_create(course=advanced_maths, title="Statistics", order=3,
                                          description="Fundamental statistical concepts and operations")[0]
ModuleContent.objects.create(
    module=statistics, order=1,
    item=Text.objects.get_or_create(
        owner=statistics.course.owner,
        content="888 + 88 + 8 + 8 + 8 ⋍ 1000.\nNow you likely know.",
        title="Eights",
    )[0]
)
ModuleContent.objects.create(
    module=statistics, order=2,
    item=Text.objects.get_or_create(
        owner=statistics.course.owner,
        content="1 + 2 + 3 ⋍ 1 x 2 x 3.\nDo you know?",
        title="Multiply",
    )[0]
)
ModuleContent.objects.create(
    module=statistics, order=3,
    item=Text.objects.get_or_create(
        owner=statistics.course.owner,
        content="If one ship can cross the pacific in six days, what are the odds of six ships crossing the pacific?",
        title="Homework",
    )[0]
)

sets = Module.objects.get_or_create(course=computer_science, title="Sets", order=1,
                                    description="I think this is a course we did last year")[0]
ModuleContent.objects.create(
    module=sets, order=1,
    item=Text.objects.get_or_create(
        owner=sets.course.owner,
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et"
                " dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut"
                " aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse"
                " cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa"
                " qui officia deserunt mollit anim id est laborum.",
        title="Latin",
    )[0]
)
ModuleContent.objects.create(
    module=sets, order=2,
    item=Text.objects.get_or_create(
        owner=sets.course.owner,
        content="I-Lorem ipsum dolor sit amet, i-consectetur adipiscing elit, i-sed tempor kunye namandla, ukuze"
                " umsebenzi kunye nosizi, izinto ezithile ezibalulekileyo zokwenza i-eiusmod. Ukutyhubela iminyaka,"
                " ndiza kuza, ngubani oya kuthi aphumeze ithuba lokuzilolonga, ukuze iinzame zokukhuthaza ukuba"
                " isithili sesikolo kunye nokuphila ixesha elide. Ufuna ukuba yintlungu kwi-cupidatat cillum ugxekiwe"
                " kwi-Duis et dolore magna abaleke ayivelisi siphumo sokonwaba. Ngaphandle kwekomityi emnyama"
                " abamnyama abekho ngaphandle, kuyathuthuzela emphefumlweni, oko kukuthi, bayekile imisebenzi yabo"
                " babekek 'ityala ngeengxaki zakho.",
        title="Xhosa",
    )[0]
)
ModuleContent.objects.create(
    module=sets, order=3,
    item=Text.objects.get_or_create(
        owner=sets.course.owner,
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed tempor and vitality, so that the labor"
                " and sorrow, some important things to do eiusmod. Over the years, I will come, who will nostrud"
                " aliquip out of her the advantage of exercise, so that stimulus efforts if the school district and"
                " longevity. Want to be a pain in the cupidatat cillum has been criticized in the Duis et dolore magna"
                " flee produces no resultant pleasure. Excepteur cupidatat blacks are not excepteur, is soothing to"
                " the soul, that is, they deserted the general duties of those who are to blame for your troubles.",
        title="English",
    )[0]
)
python = Module.objects.get_or_create(course=computer_science, title="Python", order=2,
                                      description="Can't remember what this even is")[0]
ModuleContent.objects.create(
    module=python, order=1,
    item=Video.objects.get_or_create(
        owner=python.course.owner,
        url="https://www.youtube.com/watch?v=0arsPXEaIUY",
        title="Snek"
    )[0]
)
java = Module.objects.get_or_create(course=computer_science, title="Python", order=3,
                                    description="I do like a good cup of coffee just before bed")[0]
databases = Module.objects.get_or_create(course=computer_science, title="Databases", order=4,
                                         description="I think databases are a myth")[0]
architecture = Module.objects.get_or_create(course=computer_science, title="Architecture", order=5,
                                            description="Ah yes! I definitely know this one ;)."
                                                        " No lies here :P. None XD")[0]

boglogy = Module.objects.get_or_create(course=natural_sciences, title="Boglogy", order=1,
                                       description="We did this in school")[0]
ModuleContent.objects.create(
    module=boglogy, order=1,
    item=Text.objects.get_or_create(
        owner=boglogy.course.owner,
        content="┬──┬ ノ( ͡° ل͜ ͡°ノ)\n（╯ ͡° ل͜ ͡°）╯︵ ┻━┻",
        title=".",
    )[0]
)
ModuleContent.objects.create(
    module=boglogy, order=2,
    item=Video.objects.get_or_create(
        owner=boglogy.course.owner,
        url="https://www.youtube.com/watch?v=0arsPXEaIUY",
        title="Important"
    )[0]
)
physik = Module.objects.get_or_create(course=natural_sciences, title="Physik", order=2,
                                      description="I think this is the hard one")[0]
ModuleContent.objects.create(
    module=physik, order=1,
    item=Text.objects.get_or_create(
        owner=physik.course.owner,
        content="Physik stronk. Physic hav POUweR",
        title="Physikk",
    )[0]
)
dru__ = Module.objects.get_or_create(course=natural_sciences, title="Dru**", order=3,
                                     description="I think I misread something. Is that the police?")[0]
ModuleContent.objects.create(
    module=dru__, order=1,
    item=Text.objects.get_or_create(
        owner=dru__.course.owner,
        content="I think I'm going to jail for this",
        title="umm...",
    )[0]
)
ModuleContent.objects.create(
    module=dru__, order=1,
    item=Text.objects.get_or_create(
        owner=dru__.course.owner,
        content="[REDACTED][REDACTED][REDACTED]\n[REDACTED]\n[REDACTED][REDACTED]\n[REDACTED]\n[REDACTED]\n"
                "[REDACTED][REDACTED][REDACTED][REDACTED][REDACTED]",
        title="[REDACTED]",
    )[0]
)

astrophysics = Module.objects.get_or_create(course=theoretical_physics, title="Astrophysics", order=1,
                                            description="Modelling and understanding the wonders of the cosmos")[0]
ModuleContent.objects.create(
    module=astrophysics, order=1,
    item=Text.objects.get_or_create(
        owner=astrophysics.course.owner,
        content="Space: the final frontier. These are the voyages of the starship Enterprise. Its five-year mission:"
                " to explore strange new worlds; to seek out new life and new civilisations; to boldly go where no man"
                " has gone before.",
        title="Space",
    )[0]
)
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

fitness = Module.objects.get_or_create(
    course=fitness_gram, title="The Fitnessgram Pacer Test", order=1,
    description="The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more"
                " difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start."
                " The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A"
                " single lap should be completed each time you hear this sound. [ding] Remember to run in a straight"
                " line, and run as long as possible. The second time you fail to complete a lap before the sound, your"
                " test is over. The test will begin on the word start. On your mark, get ready, start.")[0]
ModuleContent.objects.create(
    module=fitness, order=1,
    item=Video.objects.get_or_create(
        owner=fitness.course.owner,
        url="https://www.youtube.com/watch?v=Y82jDHRrswc",
        title="The fitnessgram pacer test"
    )[0]
)
ModuleContent.objects.create(
    module=fitness, order=2,
    item=Text.objects.get_or_create(
        owner=fitness.course.owner,
        content="The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more"
                " difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start."
                " The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A"
                " single lap should be completed each time you hear this sound. [ding] Remember to run in a straight"
                " line, and run as long as possible. The second time you fail to complete a lap before the sound, your"
                " test is over. The test will begin on the word start. On your mark, get ready, start.",
        title="FitnessGram Pacer Test",
    )[0]
)

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
ModuleContent.objects.create(
    module=summit, order=2,
    item=Text.objects.get_or_create(
        owner=summit.course.owner,
        content="The FitnessGram™ Pacer Test is not a multistage aerobic capacity test that progressively gets more"
                " difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start."
                " The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A"
                " single lap should be completed each time you hear this sound. [ding] Remember to run in a straight"
                " line, and run as long as possible. The second time you fail to complete a lap before the sound, your"
                " test is over. The test will begin on the word start. On your mark, get ready, start.",
        title="FitnessGram Pacer Test",
    )[0]
)

knowledge = Module.objects.get_or_create(course=longest_word, title="Now You Know", order=1,
                                         description="Now you know the longest word")[0]
print("Created Modules")

# Assignment class DEPENDS ON module
# AssignmentContent class DEPENDS ON assignment
# Text class DEPENDS ON User
AssignmentContent.objects.all().delete()
arithmetic_a1 = Assignment.objects.get_or_create(module=arithmetic, title="Basic sums", order=1,
                                                 description="Answer the following and submit in a text document.")[0]
arithmetic_a2 = Assignment.objects.get_or_create(module=arithmetic, title="Less basic sums", order=2,
                                                 description="What is 69 - 420?")[0]
arithmetic_a3 = Assignment.objects.get_or_create(module=arithmetic, title="Lesserer basic sums", order=2,
                                                 description="What is 4(92-36(528*14-1+1)-(16+2e))+1?")[0]
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
arithmetic_q1 = Quiz.objects.get_or_create(module=arithmetic, title="Also Basic sums",
                                           description="Answer the following")[0]
q = Question.objects.get_or_create(quiz=arithmetic_q1, number=1, question_text="What is 420 - 69")[0]
Choice.objects.get_or_create(question=q, choice_text="Nice", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="Noice", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="351", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Niiiiiiiiice", correct_answer=False)
q = Question.objects.get_or_create(quiz=arithmetic_q1, number=2, question_text="What is 8000000 + 8135")[0]
Choice.objects.get_or_create(question=q, choice_text="8008135", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="The funny number", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="Immature", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Nice?", correct_answer=False)
arithmetic_q2 = Quiz.objects.get_or_create(module=arithmetic, title="Numericalifiers",
                                           description="Do thu numburials")[0]
q = Question.objects.get_or_create(quiz=arithmetic_q2, number=1, question_text="What is fourteen")[0]
Choice.objects.get_or_create(question=q, choice_text="number", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="number", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="nubmer", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="number", correct_answer=False)
q = Question.objects.get_or_create(quiz=arithmetic_q2, number=2, question_text="How old am I")[0]
Choice.objects.get_or_create(question=q, choice_text="1", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="2", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="4", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="4", correct_answer=False)

trigonometry_a1 = Assignment.objects.get_or_create(module=trigonometry, title="Pythagoras", order=1,
                                                   description="What is Pythagoras' theorem?")[0]
trigonometry_a2 = Assignment.objects.get_or_create(module=trigonometry, title="Basic Trig", order=1,
                                                   description="Answer the ")[0]
AssignmentContent.objects.create(
    assignment=trigonometry_a2, order=1,
    item=Text.objects.get_or_create(
        owner=trigonometry_a2.module.course.owner,
        content="QUESTIoN",
        title=""
    )[0]
)
trigonometry_q1 = Quiz.objects.get_or_create(module=trigonometry, title="TRIANGLE",
                                           description="I want TRIANGLE")[0]
q = Question.objects.get_or_create(quiz=trigonometry_q1, number=1,
                                   question_text="Sorry, I'm running out of ideas for this sample data.")[0]
Choice.objects.get_or_create(question=q, choice_text="yes", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="no", correct_answer=False)

algebra_a1 = Assignment.objects.get_or_create(module=algebra, title="Simple algebra", order=1,
                                              description="Given x = 20y - 4 and y = 16x, find x.")[0]
AssignmentContent.objects.create(
    assignment=algebra_a1, order=1,
    item=Text.objects.get_or_create(
        owner=algebra_a1.module.course.owner,
        content="not a job for one man alone. In basically one sitting.",
        title="This sample data is"
    )[0]
)
AssignmentContent.objects.create(
    assignment=algebra_a1, order=2,
    item=Text.objects.get_or_create(
        owner=algebra_a1.module.course.owner,
        content="should learn from this.",
        title="I"
    )[0]
)
AssignmentContent.objects.create(
    assignment=algebra_a1, order=3,
    item=Text.objects.get_or_create(
        owner=algebra_a1.module.course.owner,
        content="hapse I can add this to my reflective report?",
        title="Per"
    )[0]
)
AssignmentContent.objects.create(
    assignment=algebra_a1, order=4,
    item=Text.objects.get_or_create(
        owner=algebra_a1.module.course.owner,
        content="I already finished that.",
        title="Nah!"
    )[0]
)

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
                                              description="Do it good.")[0]
AssignmentContent.objects.create(
    assignment=fitness_a1, order=1,
    item=Text.objects.get_or_create(
        owner=fitness_a1.module.course.owner,
        content="Back flips are dangerouse. Do a front fliip instead!",
        title="Maybe not"
    )[0]
)
AssignmentContent.objects.create(
    assignment=fitness_a1, order=2,
    item=Text.objects.get_or_create(
        owner=fitness_a1.module.course.owner,
        content="Maybe do a little flair in the process. For the flex.",
        title="Extension"
    )[0]
)
fitness_a2 = Assignment.objects.get_or_create(module=fitness, title="Do a back flip", order=2,
                                              description="These are perfectly safe")[0]
AssignmentContent.objects.create(
    assignment=fitness_a2, order=1,
    item=Text.objects.get_or_create(
        owner=fitness_a2.module.course.owner,
        content="I am certified to say how safe this is. My mother said so.",
        title="Certification"
    )[0]
)
fitness_q1 = Quiz.objects.get_or_create(module=fitness, title="Personal questions",
                                       description="These are life's most personal questions")[0]
q = Question.objects.get_or_create(quiz=fitness_q1, number=1, question_text="What is your name?")[0]
Choice.objects.get_or_create(question=q, choice_text="Fransözich", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Froderickson", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Frodd", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Fredrikorisonicus III IVI IX", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="Frambulia", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Froomoonuliolicus", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Fred", correct_answer=False)
q = Question.objects.get_or_create(quiz=fitness_q1, number=1, question_text="How old are you?")[0]
Choice.objects.get_or_create(question=q, choice_text="yes", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="no", correct_answer=False)
q = Question.objects.get_or_create(quiz=fitness_q1, number=1, question_text="What is your first pet's name?")[0]
Choice.objects.get_or_create(question=q, choice_text="Ben", correct_answer=True)
q = Question.objects.get_or_create(quiz=fitness_q1, number=1, question_text="What is your mothers maiden name?")[0]
Choice.objects.get_or_create(question=q, choice_text="Mother", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="Mom", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Mum", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Mam", correct_answer=False)

summit_a1 = Assignment.objects.get_or_create(module=summit, title="Do a funny dance", order=1,
                                             description="Make me laugh.")[0]
summit_q1 = Quiz.objects.get_or_create(module=summit, title="Difficult questions",
                                       description="These are life's most difficult questions")[0]
q = Question.objects.get_or_create(quiz=summit_q1, number=1, question_text="What is the meaning of liff")[0]
Choice.objects.get_or_create(question=q, choice_text="42", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="A book, the contents of which are totally belied by its cover",
                             correct_answer=True)
q = Question.objects.get_or_create(quiz=summit_q1, number=2, question_text="What is love?")[0]
Choice.objects.get_or_create(question=q, choice_text="Chemicals 'n stuff", correct_answer=False)
Choice.objects.get_or_create(question=q, choice_text="Baby don't hurt me", correct_answer=True)
Choice.objects.get_or_create(question=q, choice_text="The feeling I get when I look at beer", correct_answer=False)

knowledge_a1 = Assignment.objects.get_or_create(module=knowledge, title="Know", order=1,
                                                description="Show you know what you know.")[0]
print("Created Assignments")

# Grade class DEPENDS ON User, Assignment
Grade.objects.all().delete()
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
