from rest_framework import serializers
from .models import StoredWebPages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .exceptions import BadInputDataException, AddressAlreadyCheckedException
from .dictionaries import BAD_INPUT, ALREADY_CHECKED


class StoredWebPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredWebPages
        fields = '__all__'


class StoredWebPagesDetailsSerializer(serializers.ModelSerializer):
    content_files = serializers.SerializerMethodField()

    def get_content_files(self, instance):
        return instance.content_files

    class Meta:
        model = StoredWebPages
        fields = ['address', 'content_files']


class InputStoredWebPagesSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    address = serializers.CharField(label='URL address to get content from', max_length=128, allow_blank=False)

    def validate(self, data):

        address = data['address']

        addresses = StoredWebPages.objects.filter(address=address)
        if addresses.exists():
            raise AddressAlreadyCheckedException(ALREADY_CHECKED)

        not_an_url = False
        '''
        adding protocol part if not there - for validation purposes
        '''
        if 'http' not in address:
            address = 'http://' + address

        try:
            URLValidator()(address)
        except ValidationError as e:
            not_an_url = True

        if not_an_url:
            raise BadInputDataException(BAD_INPUT)

        return data
