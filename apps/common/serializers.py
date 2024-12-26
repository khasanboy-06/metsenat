from rest_framework import serializers
from .models import Sponsor, Student, StudentSponsor
from django.db.models import Sum
from rest_framework.exceptions import ValidationError

class SponsorSerializer(serializers.ModelSerializer):
    sponsor_type = serializers.ChoiceField(choices=["physical_person", "legal_entity"], required=True)
    organization_name = serializers.CharField(required=False, allow_blank=True)
    total_allocated_amount = serializers.SerializerMethodField()
    class Meta:
        model = Sponsor
        fields = ('id', 
                  'full_name', 
                  'phone_number', 
                  'amount', 
                  'total_allocated_amount', 
                  'created_at', 
                  'sponsor_type', 
                  'organization_name'
                  )
        

    def validate(self, attrs):
        if attrs.get("sponsor_type") == "physical_person" and attrs.get("organization_name"):
            raise serializers.ValidationError
        if attrs.get("sponsor_type") == "legal_entity" and not attrs.get("organization_name"):
            raise serializers.ValidationError({
                "organization_name": "Organization name maydoni legal entity uchun majburiy."
            })
        return attrs
    
    def get_total_allocated_amount(self, obj):
        total_allocated = StudentSponsor.objects.filter(sponsor=obj).aggregate(
            total_allocated=Sum('allocated_amount')
        )['total_allocated']
        return total_allocated or 0


class StudentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = ('id', 
                  'sponsor', 
                  'student', 
                  'allocated_amount')

    def validate(self, attrs):
        sponsor = attrs.get('sponsor', None)
        student = attrs.get('student', None)
        allocated_amount = attrs.get('allocated_amount', None)

        sponsor_spend_money = sponsor.studentsponsor_set.aggregate(total_amount=Sum('allocated_amount'))['total_amount'] or 0
        sponsor_remain_money = sponsor.amount - sponsor_spend_money

        if sponsor_remain_money  < allocated_amount:
            raise serializers.ValidationError(detail={'sponsor': "Not enough money"})
        
        student_contract_amount = student.contract_amount
        if allocated_amount > student_contract_amount:
            raise serializers.ValidationError(detail={'allocated_amount': "Student contract amount is less than allocated amount"})
        
        total_allocated = StudentSponsor.objects.filter(student=student).aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
        total_allocated += allocated_amount
        if total_allocated > student_contract_amount:
            raise serializers.ValidationError(detail={'allocated_amount': "Student contract is full"})
        
        sponsor_status = sponsor.status
        if sponsor_status != "confirmed":
            raise serializers.ValidationError(detail={'sponsor': "Sponsor is not confirmed"})

        return attrs


class StudentSponsor1Serializer(serializers.ModelSerializer):
    sponsor = serializers.CharField(source='sponsor.full_name', read_only=True)
    class Meta:
        model = StudentSponsor
        fields = ('id', 
                'sponsor', 
                'allocated_amount')

class StudentSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='university.name', read_only=True)
    allocated_amount = serializers.SerializerMethodField()
    studentsponsor_set = StudentSponsor1Serializer(many=True)

    class Meta:
        model = Student
        fields = ('id', 
                'full_name', 
                'phone_number', 
                'university', 
                'student_type', 
                'contract_amount', 
                'allocated_amount', 
                'studentsponsor_set')
        
    def get_allocated_amount(self, obj):
        total_allocated = StudentSponsor.objects.filter(student=obj).aggregate(
            total_allocated=Sum('allocated_amount')
        )['total_allocated']
        return total_allocated or 0
    

class StudentSponsorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = ('id', 
                'sponsor', 
                'allocated_amount'
                )

    def update(self, instance, validated_data):
        new_sponsor = validated_data.get('sponsor', instance.sponsor)
        new_allocated_amount = validated_data.get('allocated_amount', instance.allocated_amount)
        new_sponsor_spent_amount = new_sponsor.studentsponsor_set.aggregate(
            total_allocated_amount=Sum('allocated_amount')
        )['total_allocated_amount'] or 0

        remaining_amount = new_sponsor.amount - new_sponsor_spent_amount


        if remaining_amount < new_allocated_amount:
            raise serializers.ValidationError({
                "allocated_amount": "Sponsor's remaining amount is not enough."
            })

        instance.sponsor = new_sponsor
        instance.allocated_amount = new_allocated_amount
        instance.save()

        return instance

class DashboardSerializer(serializers.Serializer):
    sponsor_count = serializers.IntegerField()
    month = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['student_count'] = Student.objects.filter(created_at__month=instance['month'].month).count()
        return data
