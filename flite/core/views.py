import logging
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import BudgetCategory, Transaction
from .serializers import BudgetCategorySerializer, TransactionSerializer
from rest_framework.permissions import AllowAny
from .utils import swagger_decorator

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@swagger_decorator(methods=['GET'], responses={200: BudgetCategorySerializer(many=True)})
@swagger_decorator(methods=['POST'], request_body=BudgetCategorySerializer, responses={201: BudgetCategorySerializer()})
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def budget_category_list(request):
    if request.method == 'GET':
        categories = BudgetCategory.objects.filter(owner=request.user)
        serializer = BudgetCategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BudgetCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_decorator(methods=['GET'], responses={200: BudgetCategorySerializer()})
@swagger_decorator(methods=['PUT'], request_body=BudgetCategorySerializer, responses={200: BudgetCategorySerializer()})
@swagger_decorator(methods=['DELETE'], responses={204: 'No Content'})
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def budget_category_detail(request, pk):
    try:
        category = BudgetCategory.objects.get(pk=pk, owner=request.user)
    except BudgetCategory.DoesNotExist:
        return Response(status=404)
    if request.method == 'GET':
        serializer = BudgetCategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BudgetCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)

@swagger_decorator(methods=['GET'], responses={200: TransactionSerializer(many=True)})
@swagger_decorator(methods=['POST'], request_body=TransactionSerializer, responses={201: TransactionSerializer()})
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transaction_list(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(owner=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@swagger_decorator(methods=['GET'], responses={200: TransactionSerializer()})
@swagger_decorator(methods=['PUT'], request_body=TransactionSerializer, responses={200: TransactionSerializer()})
@swagger_decorator(methods=['DELETE'], responses={204: 'No Content'})
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk, owner=request.user)
    except Transaction.DoesNotExist:
        return Response(status=404)
    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.info("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=204)