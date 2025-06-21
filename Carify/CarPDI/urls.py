from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.customer_view, name='form_customer'),
    path('vehicle/', views.vehicle_view, name='form_vehicle'),
    path('obdreading/', views.obdreading_view, name='form_obdreading'),
    path('systemcheck/', views.systemcheck_view, name='form_systemcheck'),
    path('networksystem/', views.networksystem_view, name='form_networksystem'),
    path('liveparameters/', views.liveparameters_view, name='form_liveparameters'),
    path('performancecheck/', views.performancecheck_view, name='form_performancecheck'),
    path('fluidlevel/', views.fluidlevel_view, name='form_fluidlevel'),
    path('tyrecondition/', views.tyrecondition_view, name='form_tyrecondition'),
    path('paintfinish/', views.paintfinish_view, name='form_paintfinish'),
    path('flushgap/', views.flushgap_view, name='form_flushgap'),
    path('rubbercomponent/', views.rubbercomponent_view, name='form_rubbercomponent'),
    path('glasscomponent/', views.glasscomponent_view, name='form_glasscomponent'),
    path('interiorcomponent/', views.interiorcomponent_view, name='form_interiorcomponent'),
    path('form/documentation/', views.documentation_view, name='form_documentation'),

]
