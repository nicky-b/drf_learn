from rest_framework import serializers
from home.models import Person, Color


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField() 


class ColorSerializer(serializers.ModelSerializer):

    class Meta():
        model = Color
        fields = ['color_name']


class PersonSerializer(serializers.ModelSerializer):

    color = ColorSerializer()
    color_info = serializers.SerializerMethodField()
    class Meta():
        model = Person
        fields = '__all__'
        #depth = 1 # depth=1 will return all the fields of the foreignkey

    def get_color_info(self, obj): #function name should be get_xxx serializer method field name
        color_obj = Color.objects.get(id = obj.color.id)
        return {'color_name': color_obj.color_name, 'hex_code':'#001' }

    def validate(self, data):

        special_characters = "!@#$%^&*()_+-=?</"
        if any(c in special_characters for c in data[ 'name']):
            raise serializers.ValidationError( "name cannot contain special chars" )

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
