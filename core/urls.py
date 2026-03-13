from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('provider-dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('offline-provider-dashboard/', views.offline_provider_dashboard, name='offline_provider_dashboard'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('store/', views.products, name='products'),
    path('store/cart/', views.view_cart, name='view_cart'),
    path('store/cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('store/checkout/', views.checkout, name='checkout'),
    path('service/booking/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('local-services/', views.offline_services, name='offline_services'),
    path('local-services/<int:service_id>/book/', views.book_offline_service, name='book_offline_service'),
    path('popular-services/', views.popular_services, name='popular_services'),
    path('ai-assistant/', views.ai_assistant_mode, name='ai_assistant'),
    
    path('add-funds/', views.add_funds, name='add_funds'),
    path('promote/', views.promote_worker, name='promote_worker'),
    
    path('job/post/', views.post_job, name='post_job'),
    path('job/<int:job_id>/take/', views.take_job, name='take_job'),
    path('job/<int:job_id>/submit/', views.submit_work, name='submit_work'),
    path('job/<int:job_id>/approve/', views.approve_work, name='approve_work'),
    path('job/<int:job_id>/reject/', views.reject_work, name='reject_work'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/preview/', views.review_work_preview, name='review_work_preview'),
    path('job/<int:job_id>/assign/<str:username>/', views.assign_job, name='assign_job'),
    
    path('api/chat/', views.chat_api, name='chat_api'),
]
