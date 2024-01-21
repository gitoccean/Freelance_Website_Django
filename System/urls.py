from django.urls import path
from . import views
# for forgot password, using by default django views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path("home/", views.home, name='home'),
    path("fake/", views.fake_data, name='fake'),
    path("delete/<int:id>", views.delete, name='delete'),
    # path("edit/<int:id>", views.edit, name='edit'),
    path("edit/<slug:slug>/", views.edit, name='edit'),
    path("my_login/", views.my_login, name='my_login'),
    path("my_logout/", views.my_logout, name='my_logout'),
    path("my_signup", views.my_signup, name='my_signup'),
    path("activation/<str:id>/", views.activation, name='activation'),

    path('reset', PasswordResetView.as_view(template_name='password_reset_view.html'), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(template_name='password_reset_done_view.html'),name='password_reset_done'),
    path('password_confirm/<uidb64>/<token>',PasswordResetConfirmView.as_view(template_name='password_reset_confirm_view.html'),name='password_reset_confirm'),
    path('password_complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete_view.html'), name='password_reset_complete'),

    path('book', views.book_form, name='book_form'),
    path("", views.base, name='base'),

    path('jobdata_api/<int:id>/', views.jobdata_api, name='jobdata_api'),
    path('bookdata_api/', views.bookdata_api, name='bookdata_api'),

    path('picpage/', views.picpage, name='picpage'),

    path('blog/', views.upload_blog, name='upload_blog'),
]

