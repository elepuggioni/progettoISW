"""ScrumBoard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from ScrumBoard import views
from django.http import HttpResponse


def home(request):
    return HttpResponse('Home page')


urlpatterns = [
    path('', views.home, name='home-view'),
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path(r'dashboard/crea_board', views.crea_board, name='crea-board'),
    re_path(r'dashboard\/.*', views.dashboard, name='dashboard'),
    # board
    path(r'board/', views.board_vuota, name='show-board'),
    path(r'board/<board_id>/', views.showboard, name='show-board'),
    path(r'board/<board_id>/aggiungi_card', views.aggiungi_card, name='add-card'),
    path(r'board/<board_id>/aggiungi_colonna', views.aggiungi_colonna, name='add-column'),
    path(r'board/<board_id>/aggiungi_utente', views.aggiungi_utente, name='add-user'),
    # card
    path(r'card/<card_id>/', views.showcard, name='show-card'),
    path(r'modifica_card/<card_id>/', views.modifica_card, name='modifica-card'),
    path(r'modifica_card/', views.modifica_card_vuota, name='modifica-card'),
    path(r'cancella_card/<card_id>', views.cancella_card, name='cancella-card'),
    path(r'cancella_card/', views.cancella_card_vuota, name='cancella-card'),  # in caso non sia inserito un id nel url
    # colonna
    path(r'modifica_colonna/<column_id>', views.modifica_colonna, name='modifica-colonna'),
    re_path(r'modifica_colonna\/.*', views.colonna_vuota, name='modifica-colonna'),  # in caso non sia inserito un id nel url
    path(r'cancella_colonna/<column_id>/', views.cancella_colonna, name='cancella-colonna'),
    path(r'cancella_colonna/', views.cancella_colonna_vuota, name='cancella-colonna'), # in caso non sia inserito un id nel url
    # burndown
    path(r'burndown/<board_id>', views.burndown, name='burndown'),

    path('', include('Accounts.urls')),

    # test per la visualizzazione dei forms
    # path(r'test/crea_board/', views.crea_board, name='crea-board'),
    # path(r'test/crea_colonna/<board_id>/', views.aggiungi_colonna, name='aggiungi-colonna'),
    # path(r'test/crea_card/<board_id>/', views.aggiungi_card, name='aggiungi-card'),
    # path(r'test/modifica_board/<board_id>/', views.modifica_board, name='modifica-board'),
    # path(r'test/modifica_colonna/<colonna_id>', views.modifica_colonna, name='modifica-colonna'),
    # path(r'test/modifica_card/<card_id>/', views.modifica_card, name='modifica-card'),
]
