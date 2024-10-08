from rest_framework import serializers
from home.models import Person, Color
from django.contrib.auth.models import User



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("username is taken")
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("email is taken")
        return data

    def create(self, validated_data):
        user = User.objects.create(username = validated_data["username"], email = validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField() 


# class ColorSerializer(serializers.ModelSerializer):

#     class Meta():
#         model = Color
#         fields = ['color_name']


class PersonSerializer(serializers.ModelSerializer):

    #color = ColorSerializer()
    #color_info = serializers.SerializerMethodField()
    class Meta():
        model = Person
        fields = '__all__'
        #depth = 1 # depth=1 will return all the fields of the foreignkey

    # def get_color_info(self, obj): #function name should be get_xxx serializer method field name
    #     color_obj = Color.objects.get(id = obj.color.id)
    #     return {'color_name': color_obj.color_name, 'hex_code':'#001' }

    def validate(self, data):
        special_characters = "!@#$%^&*()_+-=?</"
        # Validate 'name' field only if it is present in the request data
        if 'name' in data:
            if any(c in special_characters for c in data[ 'name']):
                raise serializers.ValidationError( "name cannot contain special chars" )

        # Validate 'age' field only if it is present in the request data
        if 'age' in data:
            if data['age'] < 18:
                raise serializers.ValidationError("age should be above 18years")
        return data

    # #below code can also perform same as above code but having some issues needs to be fixed
    # def validate_age(self, value):  #Pass the actual attribute name after the validate it will pick it
    #     print("Validating age:", value)  # Debugging statement
    #     if value < 18:
    #         raise serializers.ValidationError("Age should be above 18 years")
    #     # Return the validated value
    #     print("Validating age:", value)  # Debugging statement
    #     return value

    # def validate(self, data):
    #     special_characters = "!@#$%^&*()_+-=?</"
    #     if any(c in special_characters for c in data[ 'name']):
    #         raise serializers.ValidationError( "name cannot contain special chars" )
