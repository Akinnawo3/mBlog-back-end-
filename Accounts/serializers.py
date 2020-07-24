from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q



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

    def validate(self, data):
        email = data["email"]
        user_qs= User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError("A user with this email already exist")
        return data

    def validate_Confirm_email(self,value):  
        # the value parameter provides the function with the value of 'Confirm_email' field automatically
        # the get_initial() function provides the function with all the value of the items in the serializer
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






class AccountLoginSerializer(serializers.ModelSerializer):
    token= serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields  = ["username", "email", 'password','token']
    extra_kwargs = { 
                            "password":
                                        {"write_only":True}
                            }

    def validate(self, data):
        user_obj = None


        email = data["email"]
        username = data["username"]
        password = data["password"]
        if not email and not username:
            raise serializers.ValidationError("A Username or email must be provided to login")
        user = User.objects.filter(
                                    Q(email = email)|
                                    Q(username = username)
                                     ).distinct()
        # user = user.exclude(email__isnull=True).exclude(email__iexact="")
        if user.exists() and user.count()==1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("The Username or Email is not Valid")
        
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError(" Incorrect Password")
        
        data["token"] = "SOME RANDOM TOKEN"
   
        return data