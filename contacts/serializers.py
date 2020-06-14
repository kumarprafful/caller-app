from rest_framework import serializers

from contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'mobile', 'spam_count']


class ContactDetailSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['full_name', 'mobile', 'spam_count', 'email']

    def get_email(self, obj):
        try:
            # email only returned if the person is registered and the searching user is in the person's contact list
            if obj.owner:
                request = self.context.get('request')
                if obj.owner.contacts.get(owner=request.user):
                   return obj.owner.email
        except Exception as e:
            return None
