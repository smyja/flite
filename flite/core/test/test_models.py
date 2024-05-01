from django.test import TestCase
from django.db.models import Sum
from flite.core.models import BudgetCategory, Transaction
from flite.users.models import User

class User(models.Model):
    # your fields here

    @property
    def total_amount(self):
        return self.transactions.aggregate(total=Sum('amount'))['total']

class TestBudgetCategoryModel(TestCase):
    def test_str_representation(self):
        category = BudgetCategory(name='Test Category', description='Test description', max_spend=100.00)
        self.assertEqual(str(category), 'Test Category')

class TestTransactionModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.category = BudgetCategory.objects.create(name='Test Category', description='Test description', max_spend=100.00)

    def test_total_amount(self):
        Transaction.objects.create(owner=self.user, category=self.category, amount=50.00, description='Test transaction 1')
        Transaction.objects.create(owner=self.user, category=self.category, amount=20.00, description='Test transaction 2')
        Transaction.objects.create(owner=self.user, category=self.category, amount=30.00, description='Test transaction 3')

        self.assertEqual(self.user.total_amount, 100.00)