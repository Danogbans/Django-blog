from django.test import TestCase  # Base class for creating tests in Django.
from django.urls import reverse  # Function to reverse URL names into URL paths.
from django.contrib.auth.models import User  # Django's built-in user model
from blog.models import Post # Post model from the blog app



# Create your tests here.
class PostListViewTest(TestCase):


    @classmethod
    def setUpTestData(cls): # Creates a user and multiple posts for testing.
        user = User.objects.create_user(username='testuser', password='12345') # Creates a test user.
        number_of_posts = 10
        for post_num in range(number_of_posts): # Creates test posts.
            Post.objects.create( 
                title=f'Test Post {post_num}',
                content='This is a test post.',
                author=user
            )


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/') # Simulates a GET request to the specified URL
        self.assertEqual(response.status_code, 200) #  Asserts that the status code is 200.


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('post_list')) # Uses the URL name to generate the URL.
        self.assertEqual(response.status_code, 200)

    
    def test_pagination_is_three(self): # Tests if the pagination is working correctly and shows 3 posts per page.
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['posts']), 3)


class PostSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 10 posts for search tests
        user = User.objects.create_user(username='testuser', password='12345')
        for post_num in range(10):
            Post.objects.create(
                title=f'Test Post {post_num}',
                content='This is a test post about travel.',
                author=user
            )


    def test_search_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/search/')
        self.assertEqual(response.status_code, 200)


    def test_search_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search'), {'query': 'travel'})
        self.assertEqual(response.status_code, 200)


    def test_search_functionality(self):
        response = self.client.get(reverse('search'), {'query': 'travel'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.context)
        self.assertEqual(len(response.context['results']), 10)
        for post in response.context['results']:
            self.assertIn('travel', post.content)
