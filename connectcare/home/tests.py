from django.test import TestCase
from django.urls import resolve
from django.contrib.auth import views as auth_views
import home.views as homeview

# Create your tests here.
class HomePageTest(TestCase):
    def test_mainurlresolve(self):
        found = resolve('/')
        self.assertEqual(found.func,auth_views.login)
