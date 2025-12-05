from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import json

# JSONField is available in Django 3.1+ directly from django.db.models
try:
    from django.db.models import JSONField
except ImportError:
    # Fallback for older Django versions
    from django.contrib.postgres.fields import JSONField


class MediaAsset(models.Model):
    """Image assets - supports both Cloudinary URLs and local file storage"""
    title = models.CharField(max_length=200, blank=True)
    # Cloudinary fields (for remote storage)
    original_url = models.URLField(max_length=500, blank=True)
    web_url = models.URLField(max_length=500, blank=True)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    cloudinary_public_id = models.CharField(max_length=200, blank=True)
    # Local file storage
    image_file = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    storage_type = models.CharField(max_length=20, choices=[('cloudinary', 'Cloudinary'), ('local', 'Local')], default='local')
    folder = models.CharField(max_length=200, default='iriseup')
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Image {self.id}"
    
    def get_image_url(self):
        """Get the appropriate image URL based on storage type"""
        if self.storage_type == 'local' and self.image_file:
            return self.image_file.url
        return self.original_url or ''
    
    def get_thumbnail_url(self):
        """Get thumbnail URL - for local files, returns the same as image_url"""
        if self.storage_type == 'local' and self.image_file:
            return self.image_file.url
        return self.thumbnail_url or self.original_url or ''


class SEO(models.Model):
    """SEO metadata for pages"""
    page = models.CharField(max_length=100, unique=True, default='home')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SEO - {self.page}"


class Navigation(models.Model):
    """Navigation menu items"""
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.label


class Hero(models.Model):
    """Hero section content"""
    page = models.CharField(max_length=100, unique=True, default='home')
    label = models.CharField(max_length=100, blank=True)
    headline = models.CharField(max_length=500)
    subtext = models.TextField(blank=True)
    primary_button_text = models.CharField(max_length=100, blank=True)
    primary_button_url = models.CharField(max_length=200, blank=True)
    secondary_button_text = models.CharField(max_length=100, blank=True)
    secondary_button_url = models.CharField(max_length=200, blank=True)
    background_image_url = models.URLField(max_length=500, blank=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hero - {self.page}"


class About(models.Model):
    """About section content"""
    page = models.CharField(max_length=100, unique=True, default='home')
    label = models.CharField(max_length=100, blank=True)
    heading = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"About - {self.page}"


class Stat(models.Model):
    """Statistics/numbers for impact display"""
    icon = models.CharField(max_length=100, blank=True)  # FontAwesome icon class
    number = models.CharField(max_length=50)
    label = models.CharField(max_length=200)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.number} - {self.label}"


class Program(models.Model):
    """Programs/What We Do section"""
    label = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # FontAwesome icon class
    learn_more_url = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class FeaturedStory(models.Model):
    """Featured story section (e.g., Feed. Teach. Love.)"""
    page = models.CharField(max_length=100, unique=True, default='home')
    label = models.CharField(max_length=100, blank=True)
    quote = models.TextField(blank=True)
    quote_author = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    primary_button_text = models.CharField(max_length=100, blank=True)
    primary_button_url = models.CharField(max_length=200, blank=True)
    secondary_button_text = models.CharField(max_length=100, blank=True)
    secondary_button_url = models.CharField(max_length=200, blank=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Featured Story - {self.page}"


class Retreat(models.Model):
    """Retreat/Event highlight section"""
    page = models.CharField(max_length=100, unique=True, default='home')
    label = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    date_range = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    background_image_url = models.URLField(max_length=500, blank=True)
    primary_button_text = models.CharField(max_length=100, blank=True)
    primary_button_url = models.CharField(max_length=200, blank=True)
    secondary_button_text = models.CharField(max_length=100, blank=True)
    secondary_button_url = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Testimonials section"""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    quote = models.TextField()
    avatar_url = models.URLField(max_length=500, blank=True)
    icon = models.CharField(max_length=100, blank=True)  # FontAwesome icon class
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.name} - {self.role}"


class ImpactStory(models.Model):
    """Mission Accomplished / Impact Stories"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    icon = models.CharField(max_length=100, blank=True)  # FontAwesome icon class
    impact_points = JSONField(default=list, blank=True)  # List of impact metrics
    support_url = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name_plural = "Impact Stories"

    def __str__(self):
        return self.title


class CallToAction(models.Model):
    """Call to Action sections"""
    page = models.CharField(max_length=100, default='home')
    heading = models.CharField(max_length=200)
    subtext = models.TextField(blank=True)
    primary_button_text = models.CharField(max_length=100, blank=True)
    primary_button_url = models.CharField(max_length=200, blank=True)
    secondary_button_text = models.CharField(max_length=100, blank=True)
    secondary_button_url = models.CharField(max_length=200, blank=True)
    background_color = models.CharField(max_length=50, default='navy')
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CTA - {self.page}"


class Contact(models.Model):
    """Contact section"""
    page = models.CharField(max_length=100, unique=True, default='contact')
    heading = models.CharField(max_length=200, blank=True)
    subtext = models.TextField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contact - {self.page}"


class ContactInfo(models.Model):
    """Additional contact information items"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, blank=True)  # FontAwesome icon class
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return f"{self.label}: {self.value}"


class SocialLink(models.Model):
    """Social media links"""
    platform = models.CharField(max_length=100)  # facebook, instagram, twitter, etc.
    url = models.URLField(max_length=500)
    icon = models.CharField(max_length=100, blank=True)  # FontAwesome icon class
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.platform


class Footer(models.Model):
    """Footer content"""
    page = models.CharField(max_length=100, unique=True, default='home')
    about_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, default='© 2021–2025 iRiseUp Foundation. All rights reserved.')
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Footer - {self.page}"


class Event(models.Model):
    """Events page content"""
    title = models.CharField(max_length=200)
    date_range = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'sort_order', '-created_at']

    def __str__(self):
        return self.title
