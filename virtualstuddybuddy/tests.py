from django.test import TestCase, RequestFactory, Client
from django.db import DataError
from django.urls import reverse
from virtualstuddybuddy.models import Profile
from django.contrib.auth.models import User
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
		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")

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
	
class SignUpTests(TestCase):
	def setUp(self):
		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")

		self.response1 = self.client.post(reverse('signup'), {'name': 'test', 'gender': 'male', 'age': 21, 'major':'cs', 'description':'test descr'})
		self.response2 = self.client.post(reverse('signup'), {'name': 'empty', 'gender': '', 'age': 21, 'major':'cs', 'description':'test descr'})
		self.response3 = self.client.get(reverse('signup'))		

	def test_good_signup(self):
		p = Profile.objects.all()[0]
		self.assertEqual(p.name, 'test')
		self.assertEqual(p.gender, 'male')
		self.assertEqual(p.age, 21)
		self.assertEqual(p.major, 'cs')
		self.assertEqual(p.description, 'test descr')

	def test_bad_signup(self):
		self.assertEqual(self.response2.context['error_message'], 'Invalid Input')
	
	def test_get_profile(self):
		self.assertEqual(self.response3.url, "/virtualstudybuddy/profile/1/")

class EditProfileTests(TestCase):
	def setUp(self):
		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")
		self.client.post(reverse('signup'), {'name': 'test', 'gender': 'male', 'age': 21, 'major':'cs', 'description':'test descr'})

		self.response1 = self.client.post(reverse('editProfile'), {'name': 'test', 'gender': 'male', 'age': 21, 'major':'cs', 'description':'editted descr'})
		self.response2 = self.client.post(reverse('editProfile'), {'name': 'test', 'gender': '', 'age': 21, 'major':'cs', 'description':'test descr'})
		self.response3 = self.client.get(reverse('editProfile'))

	def test_good_edit(self):
		p = Profile.objects.all()[0]
		self.assertEqual(p.name, 'test')
		self.assertEqual(p.gender, 'male')
		self.assertEqual(p.age, 21)
		self.assertEqual(p.major, 'cs')
		self.assertEqual(p.description, 'editted descr')
	
	def test_bad_edit(self):
		self.assertEqual(self.response2.context['error_message'], 'Invalid Input')

	def test_get_editProfile(self):
		self.assertEqual(str(self.response3.context['profile']), "test test male cs 21 editted descr")
		#print("response3",self.response3.wsgi_request)
		self.assertEqual(str(self.response3.wsgi_request), "<WSGIRequest: GET '/virtualstudybuddy/editProfile/'>")
		self.assertTemplateUsed(self.response3, 'virtualstuddybuddy/editProfile.html')
		self.assertEqual(self.response3.status_code, 200)

