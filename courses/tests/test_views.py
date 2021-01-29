from django.contrib.auth.models import AnonymousUser
from django.db.models import Model
from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import Profile, ProfileManager
from courses import views
from courses.models import Module, Course
from courses.templatetags import course
from courses.views import ManageCourseListView, ModuleListView, ContentDeleteView, CourseCreateView


class ViewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Profile.objects.create_superuser(
            userid='test1',
            email='abc1@gmail.com',
            password='password'
        )

    def test_mine_page_status_code(self):
        request = self.factory.get('/course/mine/')
        request.user = self.user
        response = ManageCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/course/list.html')

    def test_response_with_anonymous_user(self):
        request = self.factory.get('/course/create/')
        request.user = AnonymousUser()
        response = CourseCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_create_page_status_code(self):
        request = self.factory.get('/course/create/')
        request.user = self.user
        response = CourseCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('courses/manage/course/form.html')

    def test_course_edit_status_code(self):
        url = self.factory.post(reverse('courses:course_edit', kwargs={'pk': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_content_delete_page_status_code(self):
        url = self.factory.get('/course/content/delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/course/delete.html')

    def test_course_module_update_page_status_code(self):
        url = self.factory.post(reverse('courses:course_module_update', kwargs={'pk': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/content/form.html')

    def test_module_content_create_page_status_code(self):
        url = self.factory.post(
            reverse('courses:module_content_create', kwargs={'module_id': 1, 'model_name': 'model'}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_module_content_update_page_status_code(self):
        url = self.factory.post(reverse('courses:module_content_update', kwargs={'module_id': 1, 'model_name': 'model',
                                                                                 'id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/module/formset.html')

    def test_module_content_delete_page_status_code(self):
        url = self.factory.post(reverse('courses:module_content_delete', kwargs={'id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_module_list_page_status_code(self):
        url = self.factory.post(reverse('courses:module_list', kwargs={'module_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/module/list.html')

    def test_module_content_list_page_status_code(self):
        url = self.factory.post(reverse('courses:module_content_list', kwargs={'module_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/module/content_list.html')

    def test_assignment_content_list_page_status_code(self):
        url = self.factory.post(reverse('courses:assignment_content_list', kwargs={'module_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/assignments/list.html')

    def test_course_assignment_update_page_status_code(self):
        url = self.factory.post(reverse('courses:course_assignment_update', kwargs={'module_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/assignments/formset.html')

    def test_assignment_update_page_status_code(self):
        url = self.factory.post(reverse('courses:assignment_update', kwargs={'module_id': 1, 'assignment_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/assignments/content-list.html')

    def test_assignment_content_create_page_status_code(self):
        url = self.factory.post(reverse('courses:assignment_content_create', kwargs={'module_id': 1, 'assignment_id': 1,
                                                                                     'model_name': 'model'}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/assignments/form.html')

    def test_quiz_list_view_status_code(self):
        url = self.factory.post(reverse('courses:quiz_list_view', kwargs={'module_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/quizzes/list.html')

    def test_quiz_create_page_status_code(self):
        url = self.factory.post(reverse('courses:quiz_create', kwargs={'module_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/quizzes/formset.html')

    def test_quiz_edit_page_status_code(self):
        url = self.factory.post(reverse('courses:quiz_edit', kwargs={'module_id': 1, 'quiz_id': 2}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/quizzes/content-list.html')

    def test_quiz_questions_create_page_status_code(self):
        url = self.factory.post(reverse('courses:quiz_questions_create', kwargs={'module_id': 1, 'quiz_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_edit_choices_page_status_code(self):
        url = self.factory.post(reverse('courses:edit_choices', kwargs={'module_id': 1, 'quiz_id': 1, 'question_id': 1}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/quizzes/choices/formset.html')

    def test_module_order_page_status_code(self):
        request = self.factory.get('/course/module/order')
        request.user = self.user
        response = ManageCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_content_order_page_status_code(self):
        request = self.factory.get('/course/content/order/')
        request.user = self.user
        response = ManageCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_all_page_status_code(self):
        request = self.factory.get('/course/all/')
        request.user = self.user
        response = ManageCourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('courses/manage/course/list.html')

    def test_course_detail_page_status_code(self):
        url = self.factory.post(reverse('courses:course_detail', kwargs={'slug': 'slug'}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

