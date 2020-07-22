from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()






class AccountCreateSerializer(serializers.ModelSerializer):
    # i had to overwrite the first_name, last_name , email field so as to make them required
    # by default, those fields are not compulsorily demanded(required)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    Confirm_email = serializers.EmailField()
    email = serializers.EmailField(label="Email Address")
    Confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields=['first_name',
                'last_name',
                'email',
                'Confirm_email',
                'username',
                'password',
                'Confirm_password',  
                ]
        extra_kwargs = { 
                        "password":
                                     {"write_only":True}
                         }

    def validate_Confirm_email(self,value):  
        # the value parameter provides the function with the value of 'Confirm_email' field automatically
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails does not match")
        # validation to make sure email doesnt exists already ; written below
        user_qs= User.objects.filter(email=email1)
        if user_qs.exists():
            raise serializers.ValidationError("A user with this email already exist")
        return value

    def validate_Confirm_password(self, value):
        data =self.get_initial()
        Initial_password = data.get('password')
        Password_confirmation = value
        if Initial_password != Password_confirmation:
            raise serializers.ValidationError("Passwords does not match")
        return value

    def create(self, validated_data):
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]
        user_instance = User(
                                first_name= first_name,
                                last_name= last_name,
                                email = email,
                                username=username
                                )
        user_instance.set_password(password)
        user_instance.save()
        return validated_data