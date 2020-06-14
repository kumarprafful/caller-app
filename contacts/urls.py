from django.urls import path

from contacts import views

urlpatterns = [
    path('report-spam/', views.report_spam, name='report-spam'),
    path('search-by-name/', views.search_user_by_name, name='search-user-by-name'),
    path('search-by-mobile/', views.search_by_phone_number, name='search-user-by-mobile'),
    path('details/', views.contact_details, name='contact-details'),
]
