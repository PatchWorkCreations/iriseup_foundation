from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
import json

from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Program,
    FeaturedStory, Retreat, Testimonial, ImpactStory, CallToAction,
    Contact, ContactInfo, SocialLink, Footer, Event
)
from .utils.cloudinary_utils import upload_to_cloudinary, delete_from_cloudinary
from .utils.local_file_utils import process_local_image, delete_local_image


# Authentication Views
def dashboard_login(request):
    """Dashboard login page"""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            return render(request, 'dashboard/login.html', {
                'error': 'Invalid username or password'
            })
    
    return render(request, 'dashboard/login.html')


@login_required
def dashboard_logout(request):
    """Dashboard logout"""
    logout(request)
    return redirect('dashboard:login')


# Dashboard Home
@login_required
def dashboard_home(request):
    """Main dashboard page"""
    stats = {
        'total_images': MediaAsset.objects.count(),
        'total_programs': Program.objects.filter(is_active=True).count(),
        'total_testimonials': Testimonial.objects.filter(is_active=True).count(),
        'total_events': Event.objects.filter(is_active=True).count(),
    }
    # Get impact statistics for display
    impact_stats = Stat.objects.filter(is_active=True).order_by('sort_order')[:4]
    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'impact_stats': impact_stats
    })


# Image Upload and Gallery
@login_required
@require_http_methods(["POST"])
def upload_image(request):
    """Upload image - supports both local file storage and Cloudinary"""
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)
        
        image_file = request.FILES['image']
        folder = request.POST.get('folder', 'iriseup')
        title = request.POST.get('title', '')
        storage_type = request.POST.get('storage_type', 'local')  # 'local' or 'cloudinary'
        
        if storage_type == 'cloudinary':
            # Upload to Cloudinary
            upload_result = upload_to_cloudinary(image_file, folder=folder)
            
            # Save to database
            media_asset = MediaAsset.objects.create(
                title=title or image_file.name,
                original_url=upload_result['original_url'],
                web_url=upload_result['web_url'],
                thumbnail_url=upload_result['thumbnail_url'],
                cloudinary_public_id=upload_result['public_id'],
                folder=folder,
                width=upload_result['width'],
                height=upload_result['height'],
                format=upload_result['format'],
                file_size=upload_result['file_size'],
                storage_type='cloudinary',
            )
            
            return JsonResponse({
                'success': True,
                'id': media_asset.id,
                'original_url': media_asset.original_url,
                'web_url': media_asset.web_url,
                'thumbnail_url': media_asset.thumbnail_url,
            })
        else:
            # Local file storage
            processed = process_local_image(image_file, folder=folder)
            
            # Save to database
            media_asset = MediaAsset.objects.create(
                title=title or image_file.name,
                image_file=processed['image_file'],
                folder=folder,
                width=processed['width'],
                height=processed['height'],
                format=processed['format'],
                file_size=processed['file_size'],
                storage_type='local',
            )
            
            return JsonResponse({
                'success': True,
                'id': media_asset.id,
                'original_url': media_asset.get_image_url(),
                'web_url': media_asset.get_image_url(),
                'thumbnail_url': media_asset.get_thumbnail_url(),
            })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def gallery(request):
    """Image gallery page"""
    images = MediaAsset.objects.all().order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        images = images.filter(Q(title__icontains=search_query) | Q(folder__icontains=search_query))
    
    # Pagination
    paginator = Paginator(images, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/gallery.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })


@login_required
@require_http_methods(["POST"])
def delete_image(request, image_id):
    """Delete image from storage (Cloudinary or local) and database"""
    try:
        media_asset = get_object_or_404(MediaAsset, id=image_id)
        
        # Delete from storage based on type
        if media_asset.storage_type == 'cloudinary' and media_asset.cloudinary_public_id:
            delete_from_cloudinary(media_asset.cloudinary_public_id)
        elif media_asset.storage_type == 'local' and media_asset.image_file:
            # Delete local file
            if media_asset.image_file:
                media_asset.image_file.delete(save=False)
        
        # Delete from database
        media_asset.delete()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# SEO Edit
@login_required
def seo_edit(request, page='home'):
    """Edit SEO metadata"""
    seo, created = SEO.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        seo.title = request.POST.get('title', '')
        seo.description = request.POST.get('description', '')
        seo.keywords = request.POST.get('keywords', '')
        seo.og_title = request.POST.get('og_title', '')
        seo.og_description = request.POST.get('og_description', '')
        seo.og_image = request.POST.get('og_image', '')
        seo.save()
        return redirect('dashboard:seo_edit', page=page)
    
    return render(request, 'dashboard/seo_edit.html', {'seo': seo, 'page': page})


# Navigation Management
@login_required
def navigation_edit(request):
    """Edit navigation menu"""
    nav_items = Navigation.objects.all()
    
    if request.method == 'POST':
        # Handle reordering
        if 'reorder' in request.POST:
            order_data = json.loads(request.POST.get('order', '[]'))
            for item in order_data:
                Navigation.objects.filter(id=item['id']).update(sort_order=item['order'])
            return JsonResponse({'success': True})
        
        # Handle add/edit
        nav_id = request.POST.get('id')
        if nav_id:
            nav = get_object_or_404(Navigation, id=nav_id)
        else:
            nav = Navigation()
        
        nav.label = request.POST.get('label', '')
        nav.url = request.POST.get('url', '')
        nav.is_active = request.POST.get('is_active') == 'on'
        nav.save()
        
        return redirect('dashboard:navigation_edit')
    
    return render(request, 'dashboard/navigation_edit.html', {'nav_items': nav_items})


@login_required
@require_http_methods(["POST"])
def navigation_delete(request, nav_id):
    """Delete navigation item"""
    nav = get_object_or_404(Navigation, id=nav_id)
    nav.delete()
    return redirect('dashboard:navigation_edit')


# Hero Edit
@login_required
def hero_edit(request, page='home'):
    """Edit hero section"""
    hero, created = Hero.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        hero.label = request.POST.get('label', '')
        hero.headline = request.POST.get('headline', '')
        hero.subtext = request.POST.get('subtext', '')
        hero.primary_button_text = request.POST.get('primary_button_text', '')
        hero.primary_button_url = request.POST.get('primary_button_url', '')
        hero.secondary_button_text = request.POST.get('secondary_button_text', '')
        hero.secondary_button_url = request.POST.get('secondary_button_url', '')
        hero.background_image_url = request.POST.get('background_image_url', '')
        hero.save()
        return redirect('dashboard:hero_edit', page=page)
    
    return render(request, 'dashboard/hero_edit.html', {'hero': hero, 'page': page})


# About Edit
@login_required
def about_edit(request, page='home'):
    """Edit about section"""
    about, created = About.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        about.label = request.POST.get('label', '')
        about.heading = request.POST.get('heading', '')
        about.description = request.POST.get('description', '')
        about.image_url = request.POST.get('image_url', '')
        about.save()
        return redirect('dashboard:about_edit', page=page)
    
    return render(request, 'dashboard/about_edit.html', {'about': about, 'page': page})


# Stats Management
@login_required
def stats_list(request):
    """List all stats"""
    stats = Stat.objects.all()
    return render(request, 'dashboard/stats_list.html', {'stats': stats})


@login_required
def stat_edit(request, stat_id=None):
    """Edit or create stat"""
    if stat_id:
        stat = get_object_or_404(Stat, id=stat_id)
    else:
        stat = Stat()
    
    if request.method == 'POST':
        stat.icon = request.POST.get('icon', '')
        stat.number = request.POST.get('number', '')
        stat.label = request.POST.get('label', '')
        stat.sort_order = int(request.POST.get('sort_order', 0))
        stat.is_active = request.POST.get('is_active') == 'on'
        stat.save()
        return redirect('dashboard:stats_list')
    
    return render(request, 'dashboard/stat_edit.html', {'stat': stat})


@login_required
@require_http_methods(["POST"])
def stat_delete(request, stat_id):
    """Delete stat"""
    stat = get_object_or_404(Stat, id=stat_id)
    stat.delete()
    return redirect('dashboard:stats_list')


# Programs Management
@login_required
def programs_list(request):
    """List all programs"""
    programs = Program.objects.all()
    return render(request, 'dashboard/programs_list.html', {'programs': programs})


@login_required
def program_edit(request, program_id=None):
    """Edit or create program"""
    if program_id:
        program = get_object_or_404(Program, id=program_id)
    else:
        program = Program()
    
    if request.method == 'POST':
        program.label = request.POST.get('label', '')
        program.title = request.POST.get('title', '')
        program.description = request.POST.get('description', '')
        program.icon = request.POST.get('icon', '')
        program.learn_more_url = request.POST.get('learn_more_url', '')
        program.sort_order = int(request.POST.get('sort_order', 0))
        program.is_active = request.POST.get('is_active') == 'on'
        program.save()
        return redirect('dashboard:programs_list')
    
    return render(request, 'dashboard/program_edit.html', {'program': program})


@login_required
@require_http_methods(["POST"])
def program_delete(request, program_id):
    """Delete program"""
    program = get_object_or_404(Program, id=program_id)
    program.delete()
    return redirect('dashboard:programs_list')


# Featured Story Edit
@login_required
def featured_story_edit(request, page='home'):
    """Edit featured story section"""
    story, created = FeaturedStory.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        story.label = request.POST.get('label', '')
        story.quote = request.POST.get('quote', '')
        story.quote_author = request.POST.get('quote_author', '')
        story.title = request.POST.get('title', '')
        story.description = request.POST.get('description', '')
        story.image_url = request.POST.get('image_url', '')
        story.primary_button_text = request.POST.get('primary_button_text', '')
        story.primary_button_url = request.POST.get('primary_button_url', '')
        story.secondary_button_text = request.POST.get('secondary_button_text', '')
        story.secondary_button_url = request.POST.get('secondary_button_url', '')
        story.save()
        return redirect('dashboard:featured_story_edit', page=page)
    
    return render(request, 'dashboard/featured_story_edit.html', {'story': story, 'page': page})


# Retreat Edit
@login_required
def retreat_edit(request, page='home'):
    """Edit retreat section"""
    retreat, created = Retreat.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        retreat.label = request.POST.get('label', '')
        retreat.title = request.POST.get('title', '')
        retreat.date_range = request.POST.get('date_range', '')
        retreat.location = request.POST.get('location', '')
        retreat.description = request.POST.get('description', '')
        retreat.background_image_url = request.POST.get('background_image_url', '')
        retreat.primary_button_text = request.POST.get('primary_button_text', '')
        retreat.primary_button_url = request.POST.get('primary_button_url', '')
        retreat.secondary_button_text = request.POST.get('secondary_button_text', '')
        retreat.secondary_button_url = request.POST.get('secondary_button_url', '')
        retreat.is_active = request.POST.get('is_active') == 'on'
        retreat.save()
        return redirect('dashboard:retreat_edit', page=page)
    
    return render(request, 'dashboard/retreat_edit.html', {'retreat': retreat, 'page': page})


# Testimonials Management
@login_required
def testimonials_list(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials_list.html', {'testimonials': testimonials})


@login_required
def testimonial_edit(request, testimonial_id=None):
    """Edit or create testimonial"""
    if testimonial_id:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    else:
        testimonial = Testimonial()
    
    if request.method == 'POST':
        testimonial.name = request.POST.get('name', '')
        testimonial.role = request.POST.get('role', '')
        testimonial.quote = request.POST.get('quote', '')
        testimonial.avatar_url = request.POST.get('avatar_url', '')
        testimonial.icon = request.POST.get('icon', '')
        testimonial.sort_order = int(request.POST.get('sort_order', 0))
        testimonial.is_active = request.POST.get('is_active') == 'on'
        testimonial.save()
        return redirect('dashboard:testimonials_list')
    
    return render(request, 'dashboard/testimonial_edit.html', {'testimonial': testimonial})


@login_required
@require_http_methods(["POST"])
def testimonial_delete(request, testimonial_id):
    """Delete testimonial"""
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    return redirect('dashboard:testimonials_list')


# Impact Stories Management
@login_required
def impact_stories_list(request):
    """List all impact stories"""
    stories = ImpactStory.objects.all()
    return render(request, 'dashboard/impact_stories_list.html', {'stories': stories})


@login_required
def impact_story_edit(request, story_id=None):
    """Edit or create impact story"""
    if story_id:
        story = get_object_or_404(ImpactStory, id=story_id)
    else:
        story = ImpactStory()
    
    if request.method == 'POST':
        story.title = request.POST.get('title', '')
        story.subtitle = request.POST.get('subtitle', '')
        story.description = request.POST.get('description', '')
        story.image_url = request.POST.get('image_url', '')
        story.icon = request.POST.get('icon', '')
        story.support_url = request.POST.get('support_url', '')
        story.sort_order = int(request.POST.get('sort_order', 0))
        story.is_active = request.POST.get('is_active') == 'on'
        
        # Handle impact points JSON
        impact_points = request.POST.get('impact_points', '')
        if impact_points:
            try:
                story.impact_points = json.loads(impact_points)
            except:
                story.impact_points = [p.strip() for p in impact_points.split('\n') if p.strip()]
        else:
            story.impact_points = []
        
        story.save()
        return redirect('dashboard:impact_stories_list')
    
    return render(request, 'dashboard/impact_story_edit.html', {'story': story})


@login_required
@require_http_methods(["POST"])
def impact_story_delete(request, story_id):
    """Delete impact story"""
    story = get_object_or_404(ImpactStory, id=story_id)
    story.delete()
    return redirect('dashboard:impact_stories_list')


# Call to Action Edit
@login_required
def cta_edit(request, page='home'):
    """Edit call to action section"""
    cta, created = CallToAction.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        cta.heading = request.POST.get('heading', '')
        cta.subtext = request.POST.get('subtext', '')
        cta.primary_button_text = request.POST.get('primary_button_text', '')
        cta.primary_button_url = request.POST.get('primary_button_url', '')
        cta.secondary_button_text = request.POST.get('secondary_button_text', '')
        cta.secondary_button_url = request.POST.get('secondary_button_url', '')
        cta.background_color = request.POST.get('background_color', 'navy')
        cta.save()
        return redirect('dashboard:cta_edit', page=page)
    
    return render(request, 'dashboard/cta_edit.html', {'cta': cta, 'page': page})


# Contact Management
@login_required
def contact_edit(request, page='contact'):
    """Edit contact section"""
    contact, created = Contact.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        contact.heading = request.POST.get('heading', '')
        contact.subtext = request.POST.get('subtext', '')
        contact.address = request.POST.get('address', '')
        contact.email = request.POST.get('email', '')
        contact.phone = request.POST.get('phone', '')
        contact.save()
        return redirect('dashboard:contact_edit', page=page)
    
    return render(request, 'dashboard/contact_edit.html', {'contact': contact, 'page': page})


@login_required
def contact_info_list(request):
    """List contact info items"""
    items = ContactInfo.objects.all()
    return render(request, 'dashboard/contact_info_list.html', {'items': items})


@login_required
def contact_info_edit(request, item_id=None):
    """Edit or create contact info item"""
    if item_id:
        item = get_object_or_404(ContactInfo, id=item_id)
    else:
        item = ContactInfo()
    
    if request.method == 'POST':
        item.label = request.POST.get('label', '')
        item.value = request.POST.get('value', '')
        item.icon = request.POST.get('icon', '')
        item.sort_order = int(request.POST.get('sort_order', 0))
        item.is_active = request.POST.get('is_active') == 'on'
        item.save()
        return redirect('dashboard:contact_info_list')
    
    return render(request, 'dashboard/contact_info_edit.html', {'item': item})


@login_required
@require_http_methods(["POST"])
def contact_info_delete(request, item_id):
    """Delete contact info item"""
    item = get_object_or_404(ContactInfo, id=item_id)
    item.delete()
    return redirect('dashboard:contact_info_list')


# Social Links Management
@login_required
def social_links_list(request):
    """List social links"""
    links = SocialLink.objects.all()
    return render(request, 'dashboard/social_links_list.html', {'links': links})


@login_required
def social_link_edit(request, link_id=None):
    """Edit or create social link"""
    if link_id:
        link = get_object_or_404(SocialLink, id=link_id)
    else:
        link = SocialLink()
    
    if request.method == 'POST':
        link.platform = request.POST.get('platform', '')
        link.url = request.POST.get('url', '')
        link.icon = request.POST.get('icon', '')
        link.sort_order = int(request.POST.get('sort_order', 0))
        link.is_active = request.POST.get('is_active') == 'on'
        link.save()
        return redirect('dashboard:social_links_list')
    
    return render(request, 'dashboard/social_link_edit.html', {'link': link})


@login_required
@require_http_methods(["POST"])
def social_link_delete(request, link_id):
    """Delete social link"""
    link = get_object_or_404(SocialLink, id=link_id)
    link.delete()
    return redirect('dashboard:social_links_list')


# Footer Edit
@login_required
def footer_edit(request, page='home'):
    """Edit footer section"""
    footer, created = Footer.objects.get_or_create(page=page)
    
    if request.method == 'POST':
        footer.about_text = request.POST.get('about_text', '')
        footer.copyright_text = request.POST.get('copyright_text', '')
        footer.save()
        return redirect('dashboard:footer_edit', page=page)
    
    return render(request, 'dashboard/footer_edit.html', {'footer': footer, 'page': page})


# Events Management
@login_required
def events_list(request):
    """List all events"""
    events = Event.objects.all()
    return render(request, 'dashboard/events_list.html', {'events': events})


@login_required
def event_edit(request, event_id=None):
    """Edit or create event"""
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    else:
        event = Event()
    
    if request.method == 'POST':
        event.title = request.POST.get('title', '')
        event.date_range = request.POST.get('date_range', '')
        event.location = request.POST.get('location', '')
        event.description = request.POST.get('description', '')
        event.image_url = request.POST.get('image_url', '')
        event.is_featured = request.POST.get('is_featured') == 'on'
        event.is_upcoming = request.POST.get('is_upcoming') == 'on'
        event.button_text = request.POST.get('button_text', '')
        event.button_url = request.POST.get('button_url', '')
        event.sort_order = int(request.POST.get('sort_order', 0))
        event.is_active = request.POST.get('is_active') == 'on'
        event.save()
        return redirect('dashboard:events_list')
    
    return render(request, 'dashboard/event_edit.html', {'event': event})


@login_required
@require_http_methods(["POST"])
def event_delete(request, event_id):
    """Delete event"""
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('dashboard:events_list')

