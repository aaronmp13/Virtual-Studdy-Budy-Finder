from django.test import TestCase, RequestFactory, Client, TransactionTestCase
from django.db import DataError, IntegrityError, transaction
from django.urls import reverse
from django.core.exceptions import ValidationError
from virtualstuddybuddy.models import Profile, StudyGroup, GroupInbox, UserInbox, UserMessage, GroupMessage
from virtualstuddybuddy.forms import ProfileForm, MeetForm, GroupForm
from django.contrib.auth.models import User
from virtualstuddybuddy import googleMeet
# Create your tests here.

class ProfileTestCases(TransactionTestCase):
	def setUp(self):
		Profile.objects.create() #pk=1, default
		Profile.objects.create(username="Case1") #pk=2, invalid input
	## NonEquivalence Tests
	def test_non_equivalence(self):
		p = Profile()
		p2 = Profile(username="Case 1")
		self.assertNotEqual(p.__str__(), p2.__str__())

	## Exception Tests
	def test_exception(self):

		with self.assertRaises(ValueError):
			Profile.objects.create(age="invalid")

		
		try:
			with transaction.atomic():
				Profile.objects.create()
			self.fail('Duplicate question allowed.')
		except IntegrityError:
			pass

		try:
			Profile.objects.create(username="1")
		except:
			pass

		try:
			Profile.objects.create(username="overthemaxlimit_overthemaxlimit_overthemaxlimit_overthemaxlimit_overthemaxlimit")
			self.fail('Invalid Username')
		except:
			pass


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

		self.response1 = self.client.post(reverse('signup'), {'username':'test','name': 'test', 'gender': 'male', 'age': 21, 'major':'cs', 'description':'test descr', 'coursework': "test cw", 'classOf': 2023})
		self.response2 = self.client.post(reverse('signup'), {'username':'test','name': 'empty', 'gender': '', 'age': 21, 'major':'cs', 'description':'test descr',  'coursework': "test cw", 'classOf': 2023})
		self.response3 = self.client.get(reverse('signup'))		

		# print(self.response1.context['form'].errors.as_data())

	def test_bad_signup(self):
		self.assertEqual(str(self.response2.context['form'].errors.as_data()['gender']), "[ValidationError(['This field is required.'])]")
	
	# def test_get_profile(self):
	# 	self.assertEqual(self.response3.url, "/virtualstudybuddy/profile/1/")

	def test_response_url(self):
		response = self.client.post(reverse('signup'), {'username':'test','name': 'test', 'gender': 'male', 'age': 21, 'major':'cs', 'description':'test descr', 'coursework': "test cw", 'classOf': 2023})
		self.assertEqual(response.status_code, 200)

class EditProfileTests(TestCase):
	def setUp(self):
		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")
		self.client.post(reverse('signup'),  {'username':'test', 'name': 'test', 'gender': 'male', 'age': 21, 'major':'cs', 'description':'test descr', 'coursework': "test cw", 'classOf': 2023})


class ProfileFormTestCases(TestCase):
	def setUp(self):
		Profile.objects.create(username="test")
		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")

	def test_isValid(self):
		form_data = {'name': "test"}
		form = ProfileForm(data=form_data)
		self.assertFalse(form.is_valid())


class MeetFormTestCases(TestCase):
	def setUp(self):
		Profile.objects.create(username="test")
		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")

	def test_badForm(self):
		form = MeetForm({})
		self.assertFalse(form.is_valid())

class GroupFormTestCases(TestCase):
	def setUp(self):
		StudyGroup.objects.create()

	def test_badForm(self):
		form = GroupForm({})
		self.assertFalse(form.is_valid())

class CreateMeetingTestCases(TestCase):
	def test_setup(self):
		g = "vsb test"
		emails = ["mtmenon123@gmail.com"]
		date = "2020-12-12"
		startTime = "10:00:00"
		endTime = "14:00:00"
		m = googleMeet.createMeeting(g, emails, date, startTime, endTime)

		self.assertEqual(m, googleMeet.createMeeting("vsb test", ["mtmenon123@gmail.com"], "2020-12-12", "10:00:00", "14:00:00"))

	def valid_input(self):
		g = "vsb test"
		emails = "mtmenon123@gmail.com"
		date = "2020-11-14"
		startTime = "10:00:00"
		endTime = "14:00:00"
		try:
			googleMeet.createMeeting(g, emails, date, startTime, endTime)
			self.fail('Invalid Emails')
		except:
			pass

class StudyGroupTestCases(TestCase):
	def setUp(self):
		StudyGroup.objects.create() #pk=1, default
		StudyGroup.objects.create(group_name="Case1") #pk=2, invalid input

	## Equivalence Tests
	def test_equivalence(self):
		default = StudyGroup.objects.get(pk=1)
		newGroup = StudyGroup()
		self.assertEqual(default.__str__(), newGroup.__str__())

	def test_non_equivalence(self):
		default = StudyGroup.objects.get(pk=1)
		case_1 = StudyGroup.objects.get(pk=2)
		self.assertNotEqual(default.__str__(), case_1.__str__())

	## Exception Tests
	def invalid_entry(self):
		with self.assertRaises(ValidationError):
			StudyGroup.objects.create(group_name="123456789101234567891012345678910123456789101234567891012345678910")

class StudyGroupViewsTestCases(TestCase):
	def setUp(self):
		Profile.objects.create()
		Profile.objects.create(username="test")
		StudyGroup.objects.create() #pk=1, default
		GroupInbox.objects.create(group=StudyGroup.objects.get(pk=1))

		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")

	def test_myGroups(self):
		response = self.client.post(reverse('mygroups'))
		self.assertEqual(response.status_code, 200)	
	
	def test_myGroups_template(self):
		response = self.client.post(reverse('mygroups'))
		self.assertTemplateUsed(response, 'virtualstuddybuddy/myGroups.html')

	def test_group(self):
		response = self.client.get('http://caamcomputing.herokuapp.com/virtualstudybuddy/group/1/')
		self.assertEqual(response.status_code, 200)	
	
	def test_group_template(self):
		response = self.client.get('http://caamcomputing.herokuapp.com/virtualstudybuddy/group/1/')
		self.assertTemplateUsed(response, 'virtualstuddybuddy/group.html')

	def test_creategroup(self):
		response = self.client.post(reverse('creategroup'))
		self.assertEqual(response.status_code, 200)	
	
	def test_creategroup_template(self):
		response = self.client.post(reverse('creategroup'))
		self.assertTemplateUsed(response, 'virtualstuddybuddy/creategroup.html')

	def test_meetgroup(self):
		response = self.client.get('http://caamcomputing.herokuapp.com/virtualstudybuddy/meetgroup/1/')
		self.assertEqual(response.status_code, 200)	
	
	def test_meetgroup_template(self):
		response = self.client.get('http://caamcomputing.herokuapp.com/virtualstudybuddy/meetgroup/1/')
		self.assertTemplateUsed(response, 'virtualstuddybuddy/meetgroup.html')

class UserMessageTests(TestCase):
	def setUp(self):
		Profile.objects.create(username="test")
		Profile.objects.create(username="test2")
		UserInbox.objects.create(profile=Profile.objects.get(pk=1))
		UserInbox.objects.create(profile=Profile.objects.get(pk=2))


		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")

	def test_equiv(self):
		mess = UserMessage.objects.create()
		self.assertEquals(mess.sender_username, "")
		self.assertEquals(mess.subject,"")
		self.assertEquals(mess.recipient_username, "")
		self.assertEquals(mess.message,"")
		self.assertEquals(mess.userinbox, None)

	def test_inbox_created(self):
		inbox = UserInbox.objects.get(pk=1)
		mess = UserMessage.objects.create(sender_username="test", subject="", userinbox=inbox)
		self.assertEquals(inbox.profile, Profile.objects.get(pk=1))

class UserMessageExceptionTests(TransactionTestCase):
	def test_bound(self):
		try:
			mess = UserMessage.objects.create(subject="OVERTHELIMOVERTHELIMOVERTHELIMOVERTHELIMOVERTHELIMOVERTHELIMOVERTHELIMOVERTHELIMOVERTHELIM")
			self.fail("Invalid")
		except:
			pass

class GroupMessageTests(TestCase):
	def setUp(self):
		StudyGroup.objects.create(group_name="test")
		StudyGroup.objects.create(group_name="test group")
		GroupInbox.objects.create(group=StudyGroup.objects.get(pk=1))

		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()
		self.client.login(username="test", password="test")

	def test_equiv(self):
		mess = GroupMessage.objects.create()
		self.assertEquals(mess.sender_username, "")
		self.assertEquals(mess.recipient_group, "")
		self.assertEquals(mess.message,"")
		self.assertEquals(mess.groupinbox, None)

	def test_inbox_created(self):
		inbox = GroupInbox.objects.get(pk=1)
		mess = GroupMessage.objects.create(sender_username="test", groupinbox=inbox)
		self.assertEquals(inbox.group, StudyGroup.objects.get(pk=1))

class GroupMessageExceptionTests(TransactionTestCase):
	def test_bound(self):
		try:
			mess = GroupMessage.objects.create(message="O")
			self.fail("Invalid")
		except:
			pass

class FindBuddiesTests(TestCase):
	def setUp(self):
		Profile.objects.create(username="test")
		user = User.objects.create(username="test")
		user.set_password("test")
		user.is_active = True
		user.save()

		Profile.objects.create(username="test2")
		user2 = User.objects.create(username="test2")
		user2.set_password("test2")
		user2.is_active = True
		user2.save()

		self.client.login(username="test", password="test")
		self.client.post(reverse('signup'), {'name': 'test', 'gender': 'male', 'age': 21, 'major':'cs', 'description':'test descr'})

		self.client.login(username="test2", password="test2")
		self.client.post(reverse('signup'), {'name': 'test2', 'gender': 'male2', 'age': 212, 'major':'cs2', 'description':'test2 descr'})

		self.response1 = self.client.get(reverse('manualMatch', args = [1]))

	def test_HTML(self):
		self.assertEqual(str(self.response1.context['matchee']), "test    20   2023")
		self.assertEqual(str(self.response1.context['matcher']), "test2    20   2023")
		self.assertEqual(str(self.response1.wsgi_request), "<WSGIRequest: GET '/virtualstudybuddy/match/1'>")
		self.assertTemplateUsed(self.response1, 'virtualstuddybuddy/match.html')
		self.assertEqual(self.response1.status_code, 200)
