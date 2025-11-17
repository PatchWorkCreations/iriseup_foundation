from django.urls import path
from . import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', dashboard_views.dashboard_login, name='login'),
    path('logout/', dashboard_views.dashboard_logout, name='logout'),
    
    # Dashboard Home
    path('', dashboard_views.dashboard_home, name='index'),
    
    # Image Management
    path('gallery/', dashboard_views.gallery, name='gallery'),
    path('upload-image/', dashboard_views.upload_image, name='upload_image'),
    path('delete-image/<int:image_id>/', dashboard_views.delete_image, name='delete_image'),
    
    # SEO
    path('seo/<str:page>/', dashboard_views.seo_edit, name='seo_edit'),
    
    # Navigation
    path('navigation/', dashboard_views.navigation_edit, name='navigation_edit'),
    path('navigation/delete/<int:nav_id>/', dashboard_views.navigation_delete, name='navigation_delete'),
    
    # Hero
    path('hero/<str:page>/', dashboard_views.hero_edit, name='hero_edit'),
    
    # About
    path('about/<str:page>/', dashboard_views.about_edit, name='about_edit'),
    
    # Stats
    path('stats/', dashboard_views.stats_list, name='stats_list'),
    path('stats/edit/', dashboard_views.stat_edit, name='stat_edit'),
    path('stats/edit/<int:stat_id>/', dashboard_views.stat_edit, name='stat_edit'),
    path('stats/delete/<int:stat_id>/', dashboard_views.stat_delete, name='stat_delete'),
    
    # Programs
    path('programs/', dashboard_views.programs_list, name='programs_list'),
    path('programs/edit/', dashboard_views.program_edit, name='program_edit'),
    path('programs/edit/<int:program_id>/', dashboard_views.program_edit, name='program_edit'),
    path('programs/delete/<int:program_id>/', dashboard_views.program_delete, name='program_delete'),
    
    # Featured Story
    path('featured-story/<str:page>/', dashboard_views.featured_story_edit, name='featured_story_edit'),
    
    # Retreat
    path('retreat/<str:page>/', dashboard_views.retreat_edit, name='retreat_edit'),
    
    # Testimonials
    path('testimonials/', dashboard_views.testimonials_list, name='testimonials_list'),
    path('testimonials/edit/', dashboard_views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/edit/<int:testimonial_id>/', dashboard_views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/delete/<int:testimonial_id>/', dashboard_views.testimonial_delete, name='testimonial_delete'),
    
    # Impact Stories
    path('impact-stories/', dashboard_views.impact_stories_list, name='impact_stories_list'),
    path('impact-stories/edit/', dashboard_views.impact_story_edit, name='impact_story_edit'),
    path('impact-stories/edit/<int:story_id>/', dashboard_views.impact_story_edit, name='impact_story_edit'),
    path('impact-stories/delete/<int:story_id>/', dashboard_views.impact_story_delete, name='impact_story_delete'),
    
    # Call to Action
    path('cta/<str:page>/', dashboard_views.cta_edit, name='cta_edit'),
    
    # Contact
    path('contact/<str:page>/', dashboard_views.contact_edit, name='contact_edit'),
    path('contact-info/', dashboard_views.contact_info_list, name='contact_info_list'),
    path('contact-info/edit/', dashboard_views.contact_info_edit, name='contact_info_edit'),
    path('contact-info/edit/<int:item_id>/', dashboard_views.contact_info_edit, name='contact_info_edit'),
    path('contact-info/delete/<int:item_id>/', dashboard_views.contact_info_delete, name='contact_info_delete'),
    
    # Social Links
    path('social-links/', dashboard_views.social_links_list, name='social_links_list'),
    path('social-links/edit/', dashboard_views.social_link_edit, name='social_link_edit'),
    path('social-links/edit/<int:link_id>/', dashboard_views.social_link_edit, name='social_link_edit'),
    path('social-links/delete/<int:link_id>/', dashboard_views.social_link_delete, name='social_link_delete'),
    
    # Footer
    path('footer/<str:page>/', dashboard_views.footer_edit, name='footer_edit'),
    
    # Events
    path('events/', dashboard_views.events_list, name='events_list'),
    path('events/edit/', dashboard_views.event_edit, name='event_edit'),
    path('events/edit/<int:event_id>/', dashboard_views.event_edit, name='event_edit'),
    path('events/delete/<int:event_id>/', dashboard_views.event_delete, name='event_delete'),
]

