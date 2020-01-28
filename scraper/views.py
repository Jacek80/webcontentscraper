from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import StoredWebPagesSerializer, InputStoredWebPagesSerializer, StoredWebPagesDetailsSerializer
from .service.webscraperservice import WebScraperService
from .service.storageservice import StorageService
from .models import StoredWebPages
from django_q.tasks import async_task


class ScraperViews(viewsets.ViewSet):
    service = WebScraperService()
    storage_service = StorageService()
    permission_classes = (IsAuthenticated,)
    serializer_class = InputStoredWebPagesSerializer

    def destroy(self, request, pk=None):
        pass

    def retrieve(self, request, pk=None):
        queryset = StoredWebPages.objects.all()
        data = get_object_or_404(queryset, pk=pk, status=True)
        data.content_files = self.storage_service.get_stored_content(pk)
        serializer = StoredWebPagesDetailsSerializer(data)
        return Response(serializer.data)

    def list(self, request):
        queryset = StoredWebPages.objects.all()
        serializer = StoredWebPagesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = InputStoredWebPagesSerializer(data=request.data)
        if serializer.is_valid():
            address = request.data.get('address')

            data = {
                'address': address,
                'text_length': 0,
                'images_number': 0,
                'status': False
            }

            serializer = StoredWebPagesSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()

                if settings.RUN_IN_ASYNC_MODE:
                    async_task('self.scrape_content', address, instance.id)
                else:
                    self.scrape_content(address, instance.id)

                return redirect('scraper-list')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def download(self, request, **kwargs):
        identifier = kwargs['identifier']
        type = kwargs['type']
        filename = kwargs['filename']

        response = self.storage_service.download(identifier=identifier, type=type, filename=filename)

        response = HttpResponse(response, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(kwargs['filename'])

        return response

    def scrape_content(self, address, object_id):
        response = self.service.scrape_content(address)

        StoredWebPages.objects.filter(
            id=object_id
        ).update(
            text_length=len(response['text']),
            images_number=len(response['images']),
            status=True
        )

        self.storage_service.store_text(response['text'], object_id)
        self.storage_service.store_images(response['images'], object_id)

        return True
