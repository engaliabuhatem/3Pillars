from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.bd.views import DownloadLeadCreateView, EnquiryCreateView, ProposalRequestCreateView
from apps.careers.api import ApplicationCreateView, JobViewSet
from apps.content import views as content
from apps.core import views as core

router = SimpleRouter(trailing_slash=True)
router.register("services", content.ServiceViewSet, basename="service")
router.register("sectors", content.SectorViewSet, basename="sector")
router.register("projects", content.ProjectViewSet, basename="project")
router.register("insights", content.InsightViewSet, basename="insight")
router.register("team", content.TeamViewSet, basename="team")
router.register("offices", content.OfficeViewSet, basename="office")
router.register("certifications", content.CertificationViewSet, basename="certification")
router.register("downloads", content.DownloadViewSet, basename="download")
router.register("pillars", content.PillarViewSet, basename="pillar")
router.register("approach-stages", content.LifecycleStageViewSet, basename="approach-stage")
router.register("pages", core.PageViewSet, basename="page")
router.register("jobs", JobViewSet, basename="job")

urlpatterns = [
    path("site-settings/", core.SiteSettingsView.as_view(), name="site-settings"),
    path("navigation/", core.NavigationView.as_view(), name="navigation"),
    path("home/", core.HomeView.as_view(), name="home"),
    path("redirects/", core.RedirectListView.as_view(), name="redirects"),
    path("sitemap/", core.sitemap, name="sitemap"),
    path("health/", core.health, name="health"),
    path("enquiries/", EnquiryCreateView.as_view(), name="enquiry-create"),
    path("proposal-requests/", ProposalRequestCreateView.as_view(), name="proposal-create"),
    path("applications/", ApplicationCreateView.as_view(), name="application-create"),
    path("downloads/<int:pk>/lead/", DownloadLeadCreateView.as_view(), name="download-lead"),
    *router.urls,
]
