"""
Content helpers for converting database models to JSON format for templates.
This allows the frontend to use the same structure whether data comes from
database or JSON files.
"""

from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Program,
    FeaturedStory, Retreat, Testimonial, ImpactStory, CallToAction,
    Contact, ContactInfo, SocialLink, Footer, Event
)


def get_homepage_content_from_db():
    """
    Convert database models to JSON format for homepage template.
    Returns a dictionary matching the structure expected by templates.
    """
    content = {}
    
    # SEO
    try:
        seo = SEO.objects.get(page='home')
        content['seo'] = {
            'title': seo.title,
            'description': seo.description,
            'keywords': seo.keywords,
            'og_title': seo.og_title,
            'og_description': seo.og_description,
            'og_image': seo.og_image,
        }
    except SEO.DoesNotExist:
        content['seo'] = {}
    
    # Navigation
    nav_items = Navigation.objects.filter(is_active=True).order_by('sort_order')
    content['navigation'] = [
        {
            'label': item.label,
            'url': item.url,
        }
        for item in nav_items
    ]
    
    # Hero
    try:
        hero = Hero.objects.get(page='home')
        content['hero'] = {
            'label': hero.label,
            'headline': hero.headline,
            'subtext': hero.subtext,
            'primary_button': {
                'text': hero.primary_button_text,
                'url': hero.primary_button_url,
            },
            'secondary_button': {
                'text': hero.secondary_button_text,
                'url': hero.secondary_button_url,
            },
            'background_image': hero.background_image_url,
        }
    except Hero.DoesNotExist:
        content['hero'] = {}
    
    # About
    try:
        about = About.objects.get(page='home')
        content['about'] = {
            'label': about.label,
            'heading': about.heading,
            'description': about.description,
            'image': about.image_url,
        }
    except About.DoesNotExist:
        content['about'] = {}
    
    # Stats
    stats = Stat.objects.filter(is_active=True).order_by('sort_order')
    content['stats'] = [
        {
            'icon': stat.icon,
            'number': stat.number,
            'label': stat.label,
        }
        for stat in stats
    ]
    
    # Programs
    programs = Program.objects.filter(is_active=True).order_by('sort_order')
    content['programs'] = [
        {
            'label': program.label,
            'title': program.title,
            'description': program.description,
            'icon': program.icon,
            'learn_more_url': program.learn_more_url,
        }
        for program in programs
    ]
    
    # Featured Story
    try:
        story = FeaturedStory.objects.get(page='home')
        content['featured_story'] = {
            'label': story.label,
            'quote': story.quote,
            'quote_author': story.quote_author,
            'title': story.title,
            'description': story.description,
            'image': story.image_url,
            'primary_button': {
                'text': story.primary_button_text,
                'url': story.primary_button_url,
            },
            'secondary_button': {
                'text': story.secondary_button_text,
                'url': story.secondary_button_url,
            },
        }
    except FeaturedStory.DoesNotExist:
        content['featured_story'] = {}
    
    # Retreat
    try:
        retreat = Retreat.objects.get(page='home', is_active=True)
        content['retreat'] = {
            'label': retreat.label,
            'title': retreat.title,
            'date_range': retreat.date_range,
            'location': retreat.location,
            'description': retreat.description,
            'background_image': retreat.background_image_url,
            'primary_button': {
                'text': retreat.primary_button_text,
                'url': retreat.primary_button_url,
            },
            'secondary_button': {
                'text': retreat.secondary_button_text,
                'url': retreat.secondary_button_url,
            },
        }
    except Retreat.DoesNotExist:
        content['retreat'] = {}
    
    # Testimonials
    testimonials = Testimonial.objects.filter(is_active=True).order_by('sort_order')
    content['testimonials'] = [
        {
            'name': testimonial.name,
            'role': testimonial.role,
            'quote': testimonial.quote,
            'avatar': testimonial.avatar_url,
            'icon': testimonial.icon,
        }
        for testimonial in testimonials
    ]
    
    # Impact Stories
    stories = ImpactStory.objects.filter(is_active=True).order_by('sort_order')
    content['impact_stories'] = [
        {
            'title': story.title,
            'subtitle': story.subtitle,
            'description': story.description,
            'image': story.image_url,
            'icon': story.icon,
            'impact_points': story.impact_points or [],
            'support_url': story.support_url,
        }
        for story in stories
    ]
    
    # Call to Action
    try:
        cta = CallToAction.objects.get(page='home')
        content['cta'] = {
            'heading': cta.heading,
            'subtext': cta.subtext,
            'primary_button': {
                'text': cta.primary_button_text,
                'url': cta.primary_button_url,
            },
            'secondary_button': {
                'text': cta.secondary_button_text,
                'url': cta.secondary_button_url,
            },
            'background_color': cta.background_color,
        }
    except CallToAction.DoesNotExist:
        content['cta'] = {}
    
    # Footer
    try:
        footer = Footer.objects.get(page='home')
        content['footer'] = {
            'about_text': footer.about_text,
            'copyright_text': footer.copyright_text,
        }
    except Footer.DoesNotExist:
        content['footer'] = {}
    
    # Contact Info
    contact_items = ContactInfo.objects.filter(is_active=True).order_by('sort_order')
    content['contact_info'] = [
        {
            'label': item.label,
            'value': item.value,
            'icon': item.icon,
        }
        for item in contact_items
    ]
    
    # Social Links
    social_links = SocialLink.objects.filter(is_active=True).order_by('sort_order')
    content['social_links'] = [
        {
            'platform': link.platform,
            'url': link.url,
            'icon': link.icon,
        }
        for link in social_links
    ]
    
    return content


def get_contact_page_content_from_db():
    """Get contact page content from database"""
    content = {}
    
    try:
        contact = Contact.objects.get(page='contact')
        content['contact'] = {
            'heading': contact.heading,
            'subtext': contact.subtext,
            'address': contact.address,
            'email': contact.email,
            'phone': contact.phone,
        }
    except Contact.DoesNotExist:
        content['contact'] = {}
    
    # Contact Info
    contact_items = ContactInfo.objects.filter(is_active=True).order_by('sort_order')
    content['contact_info'] = [
        {
            'label': item.label,
            'value': item.value,
            'icon': item.icon,
        }
        for item in contact_items
    ]
    
    # Social Links
    social_links = SocialLink.objects.filter(is_active=True).order_by('sort_order')
    content['social_links'] = [
        {
            'platform': link.platform,
            'url': link.url,
            'icon': link.icon,
        }
        for link in social_links
    ]
    
    return content


def get_events_page_content_from_db():
    """Get events page content from database"""
    upcoming_events = Event.objects.filter(is_active=True, is_upcoming=True).order_by('-is_featured', 'sort_order', '-created_at')
    past_events = Event.objects.filter(is_active=True, is_upcoming=False).order_by('-created_at')
    
    return {
        'upcoming_events': [
            {
                'title': event.title,
                'date_range': event.date_range,
                'location': event.location,
                'description': event.description,
                'image': event.image_url,
                'is_featured': event.is_featured,
                'button_text': event.button_text,
                'button_url': event.button_url,
            }
            for event in upcoming_events
        ],
        'past_events': [
            {
                'title': event.title,
                'date_range': event.date_range,
                'location': event.location,
                'description': event.description,
                'image': event.image_url,
                'button_text': event.button_text,
                'button_url': event.button_url,
            }
            for event in past_events
        ],
    }

