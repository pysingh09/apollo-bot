from ibm_watson.views import WatsonDashboard
from django.conf.urls import url, include

urlpatterns = [
    url('watson/', WatsonDashboard.as_view(), name='watson')
]
