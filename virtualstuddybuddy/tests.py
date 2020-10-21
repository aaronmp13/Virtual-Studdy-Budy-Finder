from django.test import TestCase, RequestFactory
from django.db import DataError
from django.urls import reverse
from virtualstuddybuddy.models import Profile
# Create your tests here.

class ProfileTestCases(TestCase):
	def setUp(self):
		Profile.objects.create() #pk=1, default
		Profile.objects.create(username="Case1") #pk=2, invalid input
		Profile.objects.create(name="This_input_is_too_long_for_the_field_This_input_is_too_long_for_the_field_This_input_is_too_long_for_the_field_This_input_is_too_long_for_the_field") #pk=3, invalid input
		Profile.objects.create(name="") #pk=4, second default

	## Equivalence Tests
	def test_equivalence(self):
		default = Profile.objects.get(pk=1)
		newProf = Profile()
		self.assertEqual(default.__str__(), newProf.__str__())

	def test_non_equivalence(self):
		default = Profile.objects.get(pk=1)
		case_1 = Profile.objects.get(pk=2)
		self.assertNotEqual(default.__str__(), case_1.__str__())

	## Boundary Tests
	def test_invalid_name(self):
		name = Profile.objects.get(pk=3)
		self.assertEqual("This_input_is_too_long_for_the_field_This_input_is_too_long_for_the_field_This_input_is_too_long_for_the_field_This_input_is_too_long_for_the_field", name.name)
		# Name defaults if there is an invalid entry

	def test_invalid_gender(self):
		name = Profile.objects.get(pk=4)
		self.assertEqual("", name.name)

	## Exception Tests
	def test_exception_age(self):
		with self.assertRaises(ValueError):
			Profile.objects.create(age="invalid")


class ProfileViewTestCases(TestCase):
	def setUp(self):
		Profile.objects.create() #pk=1, default

	## Test Signup Template/URL
	def test_signup(self):
		response = self.client.post(reverse('signup'))
		self.assertEqual(response.status_code, 200)	
	
	def test_signup_template(self):
		response = self.client.post(reverse('signup'))
		self.assertTemplateUsed(response, 'virtualstuddybuddy/signup.html')

	## Test Main Page Template/URL
	def test_main_page(self):
		response = self.client.post(reverse('index'))
		self.assertEqual(response.status_code, 200)
	
	def test_main_page_template(self):
		response = self.client.post(reverse('index'))
		self.assertTemplateUsed(response, 'virtualstuddybuddy/index.html')

	## Test Profile Template/URL
	def test_profile(self):
		default = Profile.objects.get(pk=1)
		response = self.client.get('http://caamcomputing.herokuapp.com/virtualstudybuddy/profile/1/')
		self.assertEqual(response.status_code, 200)
	def test_profile_template(self):
		response = self.client.get('http://caamcomputing.herokuapp.com/virtualstudybuddy/profile/1/')
		self.assertTemplateUsed(response, 'virtualstuddybuddy/profile.html')
