## Testing documentation


###Test plan -

To test every class within an app for its functionality and purpose
and ensure all code works the way it was intended to.

### Accounts -

_models_: 2 fails with date and time
_views_: fails with 'userid' in url + ajax tests

### Announcements - 

Tested announcements urls with its corresponding
HTML page, and the announcements staff can post
on the website.

_models_: fails with date and time

### Courses -

_models_: fails date and time and class 'ItemBase' cannot be tested
_views_: Permission required urls fail
_forms_: small test

### Event Calendar -

Tested calendar functionality (correct month and
days are displayed) and its events to be 
displayed.

_forms_: possible tests

### Home -

Tested homepage URLs and search bar

### Students -

_models_: fails date and time
_views_: urls tests require pk
