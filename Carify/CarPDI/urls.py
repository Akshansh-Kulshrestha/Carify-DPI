from django.urls import path
from . import views

urlpatterns = [
    # path('', views.unified_form, name='unified_form'),
    path('customer/', views.customer_view, name='form_customer'),
    path('vehicle/', views.vehicle_view, name='form_vehicle'),
    path('form/obdreading/', views.obdreading_view, name='form_obdreading'),
#     path('form/systemcheck/', views.form_systemcheck, name='form_systemcheck'),
#     path('form/networksystem/', views.form_networksystem, name='form_networksystem'),
#     path('form/fluidlevel/', views.form_fluidlevel, name='form_fluidlevel'),
#     path('form/liveparameters/', views.form_liveparameters, name='form_liveparameters'),
#     path('form/performancecheck/', views.form_performancecheck, name='form_performancecheck'),
#     path('form/paintfinish/', views.form_paintfinish, name='form_paintfinish'),
#     path('form/tyrecondition/', views.form_tyrecondition, name='form_tyrecondition'),
#     path('form/flushgap/', views.form_flushgap, name='form_flushgap'),
#     path('form/rubbercomponent/', views.form_rubbercomponent, name='form_rubbercomponent'),
#     path('form/glasscomponent/', views.form_glasscomponent, name='form_glasscomponent'),
#     path('form/interiorcomponent/', views.form_interiorcomponent, name='form_interiorcomponent'),
#     path('form/documentation/', views.form_documentation, name='form_documentation'),
#     path('form/success/', views.success_view, name='success'),
# 
]
