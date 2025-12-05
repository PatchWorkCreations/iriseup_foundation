"""
Management command to set images for Hero and About sections.

Usage:
    python manage.py set_section_images --hero-image=path/to/hero.jpg --about-image=path/to/about.jpg
    python manage.py set_section_images --hero-asset-id=5 --about-asset-id=10
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from myApp.models import MediaAsset, Hero, About
from myApp.utils.cloudinary_utils import upload_to_cloudinary
from myApp.utils.local_file_utils import process_local_image


class Command(BaseCommand):
    help = 'Set images for Hero and About sections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hero-image',
            type=str,
            help='Path to image file for hero section'
        )
        parser.add_argument(
            '--about-image',
            type=str,
            help='Path to image file for about section'
        )
        parser.add_argument(
            '--hero-asset-id',
            type=int,
            help='MediaAsset ID to use for hero section'
        )
        parser.add_argument(
            '--about-asset-id',
            type=int,
            help='MediaAsset ID to use for about section'
        )
        parser.add_argument(
            '--hero-url',
            type=str,
            help='Direct URL to use for hero section'
        )
        parser.add_argument(
            '--about-url',
            type=str,
            help='Direct URL to use for about section'
        )

    def handle(self, *args, **options):
        hero_image_path = options.get('hero_image')
        about_image_path = options.get('about_image')
        hero_asset_id = options.get('hero_asset_id')
        about_asset_id = options.get('about_asset_id')
        hero_url = options.get('hero_url')
        about_url = options.get('about_url')

        # Handle Hero section
        if hero_url:
            hero_url_final = hero_url
        elif hero_asset_id:
            try:
                asset = MediaAsset.objects.get(id=hero_asset_id)
                hero_url_final = asset.get_image_url()
                self.stdout.write(self.style.SUCCESS(f'Found hero image: {asset.title}'))
            except MediaAsset.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'MediaAsset with ID {hero_asset_id} not found'))
                return
        elif hero_image_path:
            hero_url_final = self._upload_and_get_url(hero_image_path, 'hero')
        else:
            hero_url_final = None

        # Handle About section
        if about_url:
            about_url_final = about_url
        elif about_asset_id:
            try:
                asset = MediaAsset.objects.get(id=about_asset_id)
                about_url_final = asset.get_image_url()
                self.stdout.write(self.style.SUCCESS(f'Found about image: {asset.title}'))
            except MediaAsset.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'MediaAsset with ID {about_asset_id} not found'))
                return
        elif about_image_path:
            about_url_final = self._upload_and_get_url(about_image_path, 'about')
        else:
            about_url_final = None

        # Update Hero section
        if hero_url_final:
            hero, created = Hero.objects.get_or_create(page='home')
            hero.background_image_url = hero_url_final
            hero.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Hero section updated with image: {hero_url_final[:60]}...'))
        else:
            self.stdout.write(self.style.WARNING('No hero image provided'))

        # Update About section
        if about_url_final:
            about, created = About.objects.get_or_create(page='home')
            about.image_url = about_url_final
            about.save()
            self.stdout.write(self.style.SUCCESS(f'✓ About section updated with image: {about_url_final[:60]}...'))
        else:
            self.stdout.write(self.style.WARNING('No about image provided'))

        self.stdout.write(self.style.SUCCESS('\n✅ Sections updated successfully!'))

    def _upload_and_get_url(self, image_path, folder_name):
        """Upload an image and return its URL"""
        try:
            # Convert to absolute path if relative
            if not os.path.isabs(image_path):
                image_path = os.path.join(settings.BASE_DIR, image_path)
            
            if not os.path.exists(image_path):
                self.stdout.write(self.style.ERROR(f'File not found: {image_path}'))
                return None

            filename = os.path.basename(image_path)
            self.stdout.write(f'Uploading {filename}...')

            # Check if this file is already a MediaAsset (by checking if path matches)
            # Get relative path from MEDIA_ROOT
            media_root = str(settings.MEDIA_ROOT)
            if image_path.startswith(media_root):
                rel_path = os.path.relpath(image_path, media_root).replace('\\', '/')
                existing_asset = MediaAsset.objects.filter(
                    image_file__icontains=os.path.basename(rel_path)
                ).first()
                
                if existing_asset:
                    url = existing_asset.get_image_url()
                    self.stdout.write(self.style.SUCCESS(f'  Found existing MediaAsset ID: {existing_asset.id}'))
                    return url

            # Read file data
            with open(image_path, 'rb') as f:
                file_data = f.read()

            # Determine content type
            ext = os.path.splitext(filename)[1][1:].lower() or 'jpeg'
            content_type_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp',
                'avif': 'image/avif',
            }
            content_type = content_type_map.get(ext, 'image/jpeg')

            # Create InMemoryUploadedFile
            uploaded_file = InMemoryUploadedFile(
                BytesIO(file_data),
                None,
                filename,
                content_type,
                len(file_data),
                None
            )

            # Process and upload
            processed = process_local_image(uploaded_file, folder=folder_name)

            # Save to database
            media_asset = MediaAsset.objects.create(
                title=os.path.splitext(filename)[0],
                image_file=processed['image_file'],
                folder=folder_name,
                width=processed['width'],
                height=processed['height'],
                format=processed['format'],
                file_size=processed['file_size'],
                storage_type='local',
            )

            url = media_asset.get_image_url()
            self.stdout.write(self.style.SUCCESS(f'  Uploaded as MediaAsset ID: {media_asset.id}'))
            return url

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error uploading {image_path}: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            return None
