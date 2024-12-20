from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import Count

from .models import Sponsor, Student, StudentSponsor
from .serializers import (SponsorSerializer, StudentSerializer, StudentSponsorSerializer,
                          StudentSponsorUpdateSerializer, DashboardSerializer)

from rest_framework import generics, filters
from rest_framework import pagination, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user 
        return Response({
            'username': user.username,
            'first_name': user.first_name
        })


# Sponsors ------------------------------------------------
class SponsorAPIView(generics.CreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticated]

class SponsorDetailAPIView(generics.RetrieveAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

class SponsorListAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['full_name'] 
    ordering_fields = ['amount']
    filterset_fields = ['status', 'amount', 'created_at']
    pagination_class = pagination.PageNumberPagination
    # permission_classes = [permissions.IsAuthenticated]


    

# Students ------------------------------------------------
class StudentCreateAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['full_name'] 
    ordering_fields = ['contract_amount']
    filterset_fields = ['student_type', 'contract_amount']
    pagination_class = pagination.PageNumberPagination
    # permission_classes = [permissions.IsAuthenticated]



# StudentSponsor-----------------------------------------
class StudentSponsorListAPIView(generics.ListAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['student__full_name', 'sponsor__full_name']
    filterset_fields = ['allocated_amount']
    # permission_classes = [permissions.IsAuthenticated]


class StudentSponsorCreateAPIView(generics.CreateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer


class StudentSponsorUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorUpdateSerializer


class StudentSponsorDestroyAPIView(generics.DestroyAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer

class DashboardStatisticAPIView(APIView):
    def get(self, request):
        total_amount_paid = Sponsor.objects.aggregate(total_paid = Sum('amount'))['total_paid'] or 0
        total_asked_amount = Student.objects.aggregate(total_asked_amount = Sum('contract_amount'))['total_asked_amount'] or 0
        remaining_amount = total_amount_paid - total_asked_amount

        return  Response({
            "total_amount_paid": total_amount_paid,
            "total_asked_amount": total_asked_amount,
            "remaining_amount": remaining_amount
        })
    
class DashboardGraphAPIView(APIView):
    def get(self, request):
        sponsors = Sponsor.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(
            sponsor_count=Count('id')).values('month', 'sponsor_count')
        
        serializer_data = DashboardSerializer(sponsors, many=True)

        return Response(data=serializer_data.data, status=status.HTTP_200_OK)
    



  
