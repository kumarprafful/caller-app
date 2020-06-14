from django.db.models import Func
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from contacts.models import Contact
from contacts.serializers import ContactDetailSerializer, ContactSerializer


@api_view(['POST'])
def report_spam(request):
    try:
        data = JSONParser().parse(request)
        contacts = Contact.objects.filter(mobile=data.get('mobile'))
        for contact in contacts:
            contact.report_spam(request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response({'status':'success', 'data': serializer.data }, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)
    

@api_view(['GET'])
def search_user_by_name(request):
    try:
        search_name = request.GET.get('name')
        contacts = Contact.objects.filter(full_name__icontains=search_name)
        start_list = []
        mid_list = []
        for c in contacts:
            if c.full_name.lower().find(search_name.lower()) == 0:
                start_list.append(c)
            else:
                mid_list.append(c)
        contacts = start_list + mid_list

        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_contacts = paginator.paginate_queryset(contacts, request)
        serializer = ContactSerializer(paginated_contacts, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)


@api_view(['GET'])
def search_by_phone_number(request):
    try:
        search_number = request.GET.get('mobile')
        contacts = Contact.objects.filter(mobile=search_number)
        if contacts.exclude(owner=None):
            contacts = contacts.exclude(owner=None)
            serializer = ContactSerializer(contacts, many=True)
            return Response({'status':'success', 'data': serializer.data}, status=200)

        serializer = ContactSerializer(contacts, many=True)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_contacts = paginator.paginate_queryset(contacts, request)
        serializer = ContactSerializer(paginated_contacts, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)


@api_view(['GET'])
def contact_details(request):
    try:
        contact_id = request.GET.get('contact_id')
        contact = Contact.objects.get(id=contact_id)
        serializer = ContactDetailSerializer(contact, context={'request': request})
        return Response({'status':'success', 'data': serializer.data}, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)
