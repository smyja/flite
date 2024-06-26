from django.test import TestCase
from nose.tools import eq_
from flite.core.serializers import BudgetCategorySerializer, TransactionSerializer
from flite.core.models import BudgetCategory, Transaction
from flite.users.models import User

class TestBudgetCategorySerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category_data = {'name': 'Test Category', 'description': 'Test description', 'max_spend': 100.00}
        self.category = BudgetCategory.objects.create(owner=self.user, **self.category_data)
        self.serializer = BudgetCategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'max_spend'])

    def test_name_field_content(self):
        data = self.serializer.data
        eq_(data['name'], self.category_data['name'])

    def test_owner_field_is_read_only(self):
        data = {'name': 'Updated Category', 'description': 'Updated description', 'max_spend': 200.00, 'owner': self.user.id}
        serializer = BudgetCategorySerializer(instance=self.category, data=data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.owner, self.user)
        self.assertNotIn('owner', serializer.data)

class TestTransactionSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category = BudgetCategory.objects.create(name='Test Category', description='Test description', max_spend=100.00, owner=self.user)
        self.transaction_data = {
            'owner': self.user,
            'category': self.category,
            'amount': 50.00,
            'description': 'Test transaction'
        }
        self.transaction = Transaction.objects.create(**self.transaction_data)
        self.serializer = TransactionSerializer(instance=self.transaction)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'category', 'amount', 'description', 'date'])

    def test_amount_field_content(self):
        data = self.serializer.data
        eq_(float(data['amount']), self.transaction_data['amount'])

    def test_owner_field_is_read_only(self):
        data = {
            'category': self.category.id,
            'amount': 75.00,
            'description': 'Updated transaction',
            'owner': self.user.id
        }
        serializer = TransactionSerializer(instance=self.transaction, data=data)
        self.assertTrue(serializer.is_valid())
        transaction = serializer.save()
        self.assertEqual(transaction.owner, self.user)
        self.assertNotIn('owner', serializer.data)