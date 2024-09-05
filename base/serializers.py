from rest_framework import serializers
from .models import customUser, ROLE_CHOICES, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = customUser
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = customUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance



class TransactionSerializer_data(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'description', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        # Get the user from the context
        user = self.context['request'].user
        print('user----',user)
        validated_data.pop('user', None)
        # Create the transaction with the user and other validated data
        transaction = Transaction.objects.create(user=user, **validated_data)
        print('----',transaction)
        return transaction

class TransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'username', 'amount', 'description', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True}
        }

class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'