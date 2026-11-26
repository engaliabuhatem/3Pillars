"""
Write endpoints. Each returns `{"ok": true}` and nothing else: echoing a
submission back is of no use to the site and turns the endpoint into a
reflector.
"""

from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.content.models import Download

from .serializers import ConsultationRequestSerializer, DownloadLeadSerializer, EnquirySerializer, download_target
from .services import notify


class FormView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forms"


class EnquiryCreateView(FormView):
    def post(self, request):
        serializer = EnquirySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        enquiry = serializer.save()
        notify("enquiry", enquiry, admin_path=reverse("admin:bd_enquiry_change", args=[enquiry.pk]),
               summary=f"{enquiry.who} — {enquiry.get_area_of_interest_display()}")
        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class ConsultationRequestCreateView(FormView):
    def post(self, request):
        serializer = ConsultationRequestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        consultation = serializer.save()
        notify("consultation", consultation,
               admin_path=reverse("admin:bd_proposalrequest_change", args=[consultation.pk]),
               summary=f"{consultation.who} — {consultation.get_area_of_interest_display()}, {consultation.project_type}")
        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class DownloadLeadCreateView(FormView):
    def post(self, request, pk: int):
        download = get_object_or_404(Download.objects.approved(), pk=pk)
        serializer = DownloadLeadSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        lead = serializer.save(download=download)
        return Response({"ok": True, "url": download_target(download, lead.locale, request)},
                        status=status.HTTP_201_CREATED)
