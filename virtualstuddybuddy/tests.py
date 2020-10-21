from django.test import TestCase


from virtualstuddybuddy.models import Profile
# Create your tests here.

class ProfileTestCases(TestCase):
	def setUp(self):
		Profile.objects.create() #pk=1, default

		Profile.objects.create(age="Invalid Input") #pk=2, invalid input
		Profile.objects.create(username="This_input_is_too_long_for_the_field") #pk=2, invalid input

	def test_invalid_input(self):
		exception = Profile.objects.get(pk=1)