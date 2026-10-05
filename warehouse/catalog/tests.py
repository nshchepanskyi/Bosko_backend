from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from .models import Product


class ProductListTests(TestCase):
    def test_empty_database_shows_empty_state(self):
        response = self.client.get(reverse('catalog:product_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Товарів поки немає')

    def test_products_are_listed(self):
        Product.objects.create(name='Борошно', price=Decimal('45.90'), quantity=10)

        response = self.client.get(reverse('catalog:product_list'))

        self.assertContains(response, 'Борошно')
        self.assertContains(response, '45.90 грн')

    def test_product_name_is_escaped_not_executed(self):
        """Урок 1: Django autoescape не дає виконати HTML із назви товару."""
        Product.objects.create(
            name='<script>alert(1)</script>',
            price=Decimal('12.50'),
            quantity=1,
        )

        response = self.client.get(reverse('catalog:product_list'))

        self.assertNotContains(response, '<script>alert(1)</script>', html=False)
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;', html=False)


class ProductCreateTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.url = reverse('catalog:product_create')
        self.data = {
            'name': 'Кава',
            'description': 'Арабіка',
            'price': '249.90',
            'quantity': '5',
        }

    def test_form_page_contains_csrf_token(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_post_without_csrf_token_is_rejected(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Product.objects.count(), 0)

    def test_valid_post_redirects_and_message_is_shown_once(self):
        token = self.client.get(self.url).cookies['csrftoken'].value

        response = self.client.post(
            self.url,
            {**self.data, 'csrfmiddlewaretoken': token},
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertRedirects(
            response,
            reverse('catalog:product_list'),
            fetch_redirect_response=False,
        )
        self.assertEqual(Product.objects.count(), 1)

        listed = self.client.get(response.url)
        self.assertContains(listed, 'Товар «Кава» додано.')

        refreshed = self.client.get(response.url)
        self.assertNotContains(refreshed, 'Товар «Кава» додано.')

    def test_invalid_post_redisplays_form_with_errors(self):
        token = self.client.get(self.url).cookies['csrftoken'].value

        response = self.client.post(
            self.url,
            {**self.data, 'csrfmiddlewaretoken': token, 'name': '', 'price': 'abc'},
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')
        self.assertEqual(Product.objects.count(), 0)


class UahFilterTests(TestCase):
    def test_formats_price(self):
        from .templatetags.catalog_extras import uah

        self.assertEqual(uah(Decimal('1234.5')), '1,234.50 грн')
        self.assertEqual(uah(Decimal('12.5')), '12.50 грн')

    def test_passes_through_unparsable_value(self):
        from .templatetags.catalog_extras import uah

        self.assertEqual(uah(''), '')
        self.assertIsNone(uah(None))