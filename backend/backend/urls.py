from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return HttpResponse("""<title>Boom Django ⚙️</title>
      <style>
      body {
        display: flex;
        height: 100vh;
        align-items: center;
        justify-content: center;
        background: #f5f5f5;
        font-family: Arial, sans-serif;
      }
      h1 {
        color: #0078d7;
      }
    </style>
    <h1>⚙️ Django backend is running ✅</h1>""")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # Tracker App Routes
    path('api/', include('tracker.urls')),
    
    # JWT auth endpoints 🔑
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Testing
    path('api/hello/', lambda request: JsonResponse({"message": "Hello from Django!"})),
]