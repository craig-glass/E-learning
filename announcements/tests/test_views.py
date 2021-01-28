from django.test import TestCase
from django.urls import reverse


class AnnouncementListTest(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/announcements/view/')
        self.assertEquals(response.status_code, 200)

    def test_announcements_view_template(self):
        response = self.client.get('/announcements/view/')
        self.assertTemplateUsed(response, 'announcements.html')

    def test_add_announcements_page_status_code(self):
        response = self.client.get('/announcements/add/')
        self.assertEquals(response.status_code, 200)

    def test_add_announcement_uses_correct_template(self):
        response = self.client.get('/announcements/add/')
        self.assertTemplateUsed(response, 'add_announcement.html')
