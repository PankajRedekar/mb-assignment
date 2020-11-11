from rest_framework import serializers
from api.models import Plan


class GenerateHashSerializer(serializers.Serializer):  
    """
    Generate Hash Key serializer
    """
    email = serializers.EmailField()
    firstname = serializers.CharField(max_length=200)
    txnid = serializers.CharField(max_length=200)
    amount = serializers.CharField(max_length=200)
    productinfo = serializers.CharField(max_length=200)

    def is_valid(self):
        valid = super(GenerateHashSerializer, self).is_valid()
        if not valid:
            return valid

        #Validate Plan amount and given amount
        try:
            plan = Plan.objects.get(title=self.data["productinfo"])
        except Plan.DoesNotExist:
            raise serializers.ValidationError({"plan":"Plan does not exist"})
        price = int(self.data["amount"])
        
        valid = price == plan.price
        if not valid:
            raise serializers.ValidationError({"amount":"Price missmatch with provided plan"})

        return True
