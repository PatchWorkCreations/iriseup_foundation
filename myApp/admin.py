from django.contrib import admin
from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Program,
    FeaturedStory, Retreat, Testimonial, ImpactStory, CallToAction,
    Contact, ContactInfo, SocialLink, Footer, Event
)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'folder', 'format', 'file_size', 'created_at']
    list_filter = ['folder', 'format', 'created_at']
    search_fields = ['title', 'folder', 'cloudinary_public_id']
    readonly_fields = ['original_url', 'web_url', 'thumbnail_url', 'cloudinary_public_id', 
                      'width', 'height', 'format', 'file_size', 'created_at', 'updated_at']


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'updated_at']
    search_fields = ['page', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ['label', 'url', 'sort_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['label', 'url']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['page', 'headline', 'updated_at']
    search_fields = ['page', 'headline', 'subtext']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['page', 'heading', 'updated_at']
    search_fields = ['page', 'heading', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label', 'sort_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['label', 'number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_order', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description', 'label']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FeaturedStory)
class FeaturedStoryAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'updated_at']
    search_fields = ['page', 'title', 'quote', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Retreat)
class RetreatAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_range', 'location', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'sort_order', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'role', 'quote']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ImpactStory)
class ImpactStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'sort_order', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ['page', 'heading', 'updated_at']
    search_fields = ['page', 'heading', 'subtext']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['page', 'email', 'phone', 'updated_at']
    search_fields = ['page', 'email', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'sort_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['label', 'value']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'sort_order', 'is_active']
    list_filter = ['is_active', 'platform']
    search_fields = ['platform', 'url']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['page', 'updated_at']
    search_fields = ['page', 'about_text', 'copyright_text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_range', 'location', 'is_featured', 'is_upcoming', 'is_active', 'updated_at']
    list_filter = ['is_featured', 'is_upcoming', 'is_active']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
