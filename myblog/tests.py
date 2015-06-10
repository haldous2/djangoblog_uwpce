import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import utc
from myblog.models import Post, Category

class PostTestCase(TestCase):

    fixtures = ['myblog_test_fixture.json', ]

    def setUp(self):
        self.user = User.objects.get(pk=1)

    ## returns unicode
    def test_unicode(self):
        expected = u"This is a title"
        p1 = Post(title=expected)
        actual = unicode(p1)
        self.assertEqual(expected, actual)

    ## page has functioning username
    def test_user_name_bug_to_feature(self):
        expected = u"Mr. Administrator"
        p1 = Post(author=self.user)
        actual = p1.author_name()
        self.assertEqual(expected, actual)

    ## test, test of test
    #def test_blah(self):
    #    self.assertEqual('joe', 'bob')

    ## page should not exist
    def test_non_existent_post_returns_404(self):
        resp = self.client.get('/post/9999')
        self.assertEqual(resp.status_code, 404)


class CategoryTestCase(TestCase):

    """test views provided in the front-end"""
    fixtures = ['myblog_test_fixture.json', ]

    ## Setup categories for testing
    ## Note: tests entries deleted when test completed
    def setUp(self):
        for count in range(1, 5):
            category = Category(name="Category %d" % count, description="This is the %d category." % count)
            category.save()

    ## returns unicode
    def test_unicode(self):
        expected = "A Category"
        c1 = Category(name=expected)
        actual = unicode(c1)
        self.assertEqual(expected, actual)

    ## page at /categories/ returns ok
    def test_category_list(self):
        resp = self.client.get('/categories/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("Category 1" in resp.content)
        self.assertTrue("Category 2" in resp.content)
        self.assertTrue("Category 3" in resp.content)
        self.assertTrue("Category 4" in resp.content)

    ## page at /category/x/ returns ok where x is numeric
    def test_category_detail(self):
        resp = self.client.get('/category/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("Category 1" in resp.content)
        self.assertTrue("This is the 1 category" in resp.content)

class FrontEndTestCase(TestCase):

    """test views provided in the front-end"""
    fixtures = ['myblog_test_fixture.json', ]

    def setUp(self):
        self.now = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.timedelta = datetime.timedelta(15)
        author = User.objects.get(pk=1)
        for count in range(1, 11):
            post = Post(title="Post %d Title" % count,
                        text="foo",
                        author=author)
            if count < 6:
                # publish the first five posts
                pubdate = self.now - self.timedelta * count
                post.published_date = pubdate
            post.save()

    def test_list_only_published(self):
        resp = self.client.get('/')
        self.assertTrue("Recent Posts" in resp.content)
        for count in range(1, 11):
            title = "Post %d Title" % count
            if count < 6:
                self.assertContains(resp, title, count=1)
            else:
                self.assertNotContains(resp, title)

    def test_details_only_published(self):
        for count in range(1, 11):
            title = "Post %d Title" % count
            post = Post.objects.get(title=title)
            resp = self.client.get('/posts/%d/' % post.pk)
            if count < 6:
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, title)
            else:
                self.assertEqual(resp.status_code, 404)

    # def test_category(self):
    #     resp = self.client.get('/categories/1/')
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTrue("Recent Posts" in resp.content)
