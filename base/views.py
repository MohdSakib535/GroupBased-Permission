from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from .models import customUser,Transaction
from .serializers import *
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from base.decorator import check_permission
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import  IsAuthenticated

"""
    {
        "username": "ramesh",
        "email": "john2@example.com",
        "password": "sakib@123",
        "role": "user"

    }
"""


class UserCreateUpdateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user": UserSerializer(user).data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            user = customUser.objects.get(pk=pk)
        except customUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User updated successfully", "user": UserSerializer(user).data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CreateTransactionView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @check_permission('view', Transaction)
    def get(self, request):
        t1 = Transaction.objects.all()
        s1 = TransactionSerializers(t1, many=True)
        return Response(s1.data)

    """
    {
    "amount": "100.00",
    "description": "Payment for services rendered"
    }
    """

    @check_permission('add', Transaction)
    def post(self, request):
        # Get the authenticated user from the request
        user = request.user

        # Deserialize and validate the request data
        serializer = TransactionSerializer_data(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Create the transaction and associate it with the user
            transaction = serializer.save()
            return Response(TransactionSerializer_data(transaction).data, status=status.HTTP_201_CREATED)

        # Return validation errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    {
    "amount": "150.00",
    "description": "Updated description for the transaction"
    }
    """

    @check_permission('change', Transaction)
    def put(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            transaction = serializer.save()
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE /transactions/1/
    """

    @check_permission('delete', Transaction)
    def delete(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)