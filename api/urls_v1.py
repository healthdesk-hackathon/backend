from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from submission.views import SubmissionViewSet, PhoneViewSet, PersonalDataViewSet, \
    OverallWellbeingViewSet, CommonSymptomsViewSet, GradedSymptomsViewSet, RelatedConditionsViewSet, \
    MedicalCenterViewSet

from patient_tracker.views import AdmissionViewSet, HealthSnapshotViewSet, BedViewSet, BedTypeViewSet, \
    InitialHealthSnapshotViewSet

app_name = 'v1'

schema_view = get_schema_view(
    openapi.Info(
        title='Backend API',
        default_version='v1',
        description='You will find below all endpoints available for this API version',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

### SETUP YOUR API URLS HERE ### # noqa: E266

router.register('submission', SubmissionViewSet, basename='submission')
router.register('phone', PhoneViewSet, basename='phone')
router.register('personal-data', PersonalDataViewSet, basename='personal-data')
router.register('admission', AdmissionViewSet, basename='admission')
router.register('medical-center', MedicalCenterViewSet, basename='medical-center')

router.register('bed', BedViewSet, basename='bed')
router.register('bed-type', BedTypeViewSet, basename='bed-type')
router.register('initial-health-snapshot', InitialHealthSnapshotViewSet, basename='health-snapshot')


router.register('overall-wellbeing', OverallWellbeingViewSet, basename='overall-wellbeing')
router.register('common-symptoms', CommonSymptomsViewSet, basename='common-symptoms')
router.register('graded-symptoms', GradedSymptomsViewSet, basename='graded-symptoms')
router.register('related-conditions', RelatedConditionsViewSet, basename='related-conditions')

################################

urlpatterns = router.urls + [
    re_path(r'token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger related urls
    re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
