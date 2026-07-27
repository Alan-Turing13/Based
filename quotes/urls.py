from django.urls import path, include

from quotes import views

app_name = 'quotes'
urlpatterns = [
    path('', views.QuoteList.as_view(), name='quote_list'),
    path('quote/<int:pk>', views.QuoteDetail.as_view(), name='quote_detail'),
    path('add', views.QuoteCreate.as_view(), name='quote_add'),
    path('add-author', views.add_author, name='add_author'),
    path('author/<int:pk>/', views.AuthorDetail.as_view(), name='author_detail'),
    path('subject/<str:subject>/', views.SubjectDetail.as_view(), name='subject_detail'),
    path('quote/<int:pk>/edit', views.QuoteEdit.as_view(), name='quote_edit'),
    path('quote/<int:pk>/delete', views.QuoteDelete.as_view(), name='quote_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('accounts/confirm/<uuid:token>/', views.confirm_email, name='confirm_email'),
    path('search/', views.QuoteSearch.as_view(), name='quote_search'),
]