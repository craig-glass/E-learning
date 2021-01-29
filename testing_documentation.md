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

views.py: Test all URLs work correctly, and the correct template is
used for each page. URLs may also be specific to each user and there are
certain permissions required to enter a page, some users may not have.
These must be tested to ensure users get redirected to the correct page.

To ensure that the tests are written correctly, and it tests exactly
what was intended, I ran the server and tested the site as if I was a
user (student, staff and admin login) to see if the permissions each user
have are working as they should.



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


test_views.py: 




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
  

test_views.py: Classes Tested : AnnouncementList, GetAnnouncementsAjax

- Tested all announcements' URLs - all passed with response status 
  code 200
  If the URL '/announcements/add/' is visited signed out, an error 
  occurs as the user is not permitted to add announcements without login
  error with the result:
  
```
TypeError: 'AnonymousUser' object is not iterable
```
  
  


### Courses:


test_models.py: Class Tested : Subject, Course, Module, Assignment,
TextField, Quiz, Question, Choice, Grade

- Created test objects for each class and ran similar tests to
  accounts and announcements - all passed.
  
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


test_views.py: 




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
