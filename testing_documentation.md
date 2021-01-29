# Testing documentation


##Test plan

To test every class within an app for its functionality and purpose
and ensure all code works the way it was intended to.
To create tests which will fail certain functions in order to raise
the errors.


##Testing Methodology

models.py: Test user input and website functionality by creating 
mock data for all objects within a class. E.g. creating a profile with
userid and password for accounts, to see if the class holds the data
correctly, and it displays the correct information.
Date and time tests are done to make sure that the date itself is correct
and that it is in the right format.

views.py: Test all URLs work correctly, and the correct template is
used for each page. URLs may also be specific to each user and there are
certain permissions required to enter a page, some users may not have.
These must be tested to ensure users get redirected to the correct page.
Also, page status codes must be tested as a superuser to ensure users
with permissions can go to the pages they want to.

To ensure that the tests are written correctly, and it tests exactly
what was intended, I ran the server and tested the site as if I was a
user (student, staff and admin login) to see if the permissions each 
user have are working as they should.
I also used the website to try raise an error on purpose, using 
different methods like trying to enter a page signed out and testing
course URLs before being assigned to a course.



## Completed Tests and Proof of Testing
### (Including erroneous behaviour and edge cases)


### Accounts:

test_models.py: Classes Tested : Profile, AccountSubmission 

- Created mock Profile objects (userid, email, first_name, last_name, 
  phone_number, term_address, date_joined) to see if they display the
  correct information on the website with the test objects - all passed.
  
- Created an error setup using the exact same userid which should not
be allowed as it must be unique - error with the results:

``` 
django.db.utils.IntegrityError: duplicate key value violates unique
constraint "accounts_profile_userid_key" 
DETAIL:  Key (userid)=(t123) already exists.
```

- Tested all max_length value of user input with self.assertEqual
  (max_length, n) - all passed

- Setup userid 60 characters long to check max length - error with:

```
django.db.utils.DataError: value too long for type character varying(50)
```


test_views.py: Class Tested : AccountDisplayView, AccountAnalyticsView,
CourseJoinView, AccountSettingsView

- Tested all accounts URLs logged in - pass with status code 200.
- Tested URLs as an anonymous user - pass with status code 302.
- If the 'course_id' of the URL is a string instead of an integer, an
error occurs with: 
  
```
django.urls.exceptions.NoReverseMatch: Reverse for 'course_register
_autocourse' with keyword arguments '{'course_id': 'str'}' not found.
1 pattern(s) tried: ['account/register/(?P<course_id>[0-9]+)$']
```

- Tested behaviour when user is signed out: page redirects to the 
  login page


### Announcements:

test_models.py: Class Tested : Announcement

- Created mock objects for user announcements (title, author, content,
  date_created, course) to see if they display the correct information
  on the website with the test objects - all passed.

- Max length tests - same with accounts.test_models

- Multiple fields required a profile instance (announcement.author and
  announcement.course.owner). I had to make sure unique fields were
  all created with different names, e.g. email and userid. Else error
  with the result:
  
```
django.db.utils.IntegrityError: duplicate key value violates unique
constraint "accounts_profile_email_key"
DETAIL:  Key (email)=() already exists.
```

- Similar to the above, the constraint 'course' has 2 ForeignKey object
  inside it. These must also be filled in with unique details or an 
  error occurs:
  
```
django.db.utils.IntegrityError: null value in column "subject_id" of
 relation "courses_course" violates not-null constraint
DETAIL:  Failing row contains (1, , , , 2021-01-29 10:34:03.789695+00,
 2, null).
```
  

test_views.py: Classes Tested : AnnouncementList, GetAnnouncementsAjax

- Tested all announcements' URLs while signed in - all passed with 
  response status code 200 
  
- If the URL '/announcements/add/' is visited signed out, an error 
  occurs as the user is not permitted to add announcements without login
  error with the result:
  
```
TypeError: 'AnonymousUser' object is not iterable
```

- Tests on add announcement page as a superuser passes with page status
  code 200
  


### Courses:


test_models.py: Classes Tested : Subject, Course, Module, Assignment,
TextField, Quiz, Question, Choice, Grade

- Created test objects for each class and ran similar tests to
  accounts and announcements - all passed.
- Exactly the same errors as previous test models where key constraints
  must be created and unique to others
  
- Tests for classes ItemBase and Content have no objects to create,
therefore returns with error:

```
AttributeError: type object 'ItemBase' has no attribute 'objects'
```

- Tested grade value for Grade class - when the grade is below 0,
error occurs with:
  
```
django.db.utils.IntegrityError: new row for relation "courses_grade" 
violates check constraint "courses_grade_grade_check" 
DETAIL:  Failing row contains (1, -5, 2, 4, 5, 2021-01-28 00:00:00+00,
 2021-01-28 00:00:00+00).
```
However, even if the grade is too high (over 100), the test brings up
no errors.



test_views.py: Classes Tested: OwnerCourseMixin, OwnerCourseEditMixin,
CourseListView, CourseDetailView, ManageCourseListView,
CourseCreateView, CourseUpdateView, CourseDeleteView, 
CourseModuleUpdateView, ContentCreateUpdateView, ContentDeleteView, 
ModuleListView, ModuleContentListView, AssignmentContentListView,
QuizListView, QuizAssignmentCreateView, QuizCreateView,
CourseAssignmentUpdateView, AssignmentUpdateView, QuizUpdateView,
QuizCreateUpdateView, AddChoiceView, AssignmentCreateUpdateView,
ModuleOrderView, ContentOrderView

- Tested all courses URLs while logged in and logged out: all passed
  with status code 200 if logged in and 302 if signed out.

- Tested erroneous behavior when loading pages that require certain
permissions as a user with no permissions:
  
```
raise PermissionDenied(self.get_permission_denied_message())
django.core.exceptions.PermissionDenied

```

- Same tests ran on URLs as other apps where kwargs must be specific
in the URL, such as 'quiz_id' must be an integer, or an error occurs.
  


### Event Calendar:


test_models.py: Class Tested : Event

- Created test objects for (title, description, start_time, end_time,
  course) and ran similar tests to accounts and announcements - all 
  passed.
  
- Had to create unique objects for course as the ForeignKey requires
  a not-null constraint - test with only the owner constraint resulted
  with the error:

```
django.db.utils.IntegrityError: null value in column "subject_id" of
relation "courses_course" violates not-null constraint
```

- Tested date and time was correct for posting an event on the calendar.
  The start time and end time passed with the right time and made error
  tests by setting the time delta backwards and forwards. - all passed
  

test_views.py: Class Tested : CalendarView

- Tested all event_calendar's URLs - all passed with response status 
  code 200. 
  However, when loading the calendar page while logged-out, your events
  may still show on the calendar, which, if pressed will result in an
  error due to user not being signed in.
  
- Same error message as accounts test where constraints such as 
  'module_id' in the URL cannot be a string, error if so.
  
- To create a new event, one must have permission to do so. Tests
  as a superuser all passed whereas an anonymous user got an error


### Home:

test_views.py: Class Tested : HomePageView, SearchView

- Tested homepage URLs - all passed with response status 
  code 200. 
  Both logged in and logged-out users are permitted on these URLs 

### Students:


test_models.py: Class Tested : AssignmentSubmission, QuizSubmission, 
QuizAnswer

- Created test objects for each class and ran similar tests to
  accounts and announcements - all passed.
  
- All objects with a unique ForeignKey needed different constraints, or 
  a not-null constraint error occurs.
  
- Date and time tests would fail as the quiz submissions recorded
  milliseconds which would differ from the time recorded in the test
  due to the processing speed.
  
- There is no maximum value for the score in QuizSubmission class
  which means score can be valued with any positive integer.
  

  
test_views.py: Class Tested : StudentRegistrationView, 
StudentCourseListView, StudentCourseDetailView, ModuleHomePageView,
StudentHomePageView, AssignmentListStudentView

- Tested students URLs - when user is logged out, it redirects them
  to the login page and therefore the response status code is 302 for
  the page user wants to visit.
  
- Same error tests ran on URLs as other apps where kwargs must be
  specific in the URL, or an error occurs.
