"""
Management command to upload images to the MediaAsset system.
This allows uploading images without using the dashboard interface.

Usage:
    python manage.py upload_images path/to/image1.jpg path/to/image2.png
    python manage.py upload_images path/to/image.jpg --folder=events --title="Event Photo"
    python manage.py upload_images path/to/image.jpg --storage-type=cloudinary
    python manage.py upload_images path/to/*.jpg --folder=gallery
"""

import os
import glob
from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from myApp.models import MediaAsset
from myApp.utils.cloudinary_utils import upload_to_cloudinary
from myApp.utils.local_file_utils import process_local_image


class Command(BaseCommand):
    help = 'Upload one or more images to the MediaAsset system'

    def add_arguments(self, parser):
        parser.add_argument(
            'image_paths',
            nargs='+',
            type=str,
            help='Path(s) to image file(s) to upload'
        )
        parser.add_argument(
            '--folder',
            type=str,
            default='iriseup',
            help='Folder name for organizing images (default: iriseup)'
        )
        parser.add_argument(
            '--title',
            type=str,
            default='',
            help='Title for the image(s). If not provided, filename will be used.'
        )
        parser.add_argument(
            '--storage-type',
            type=str,
            choices=['local', 'cloudinary'],
            default='local',
            help='Storage type: local or cloudinary (default: local)'
        )

    def handle(self, *args, **options):
        image_paths = options['image_paths']
        folder = options['folder']
        title = options['title']
        storage_type = options['storage_type']

        self.stdout.write(self.style.SUCCESS(f'Starting image upload(s)...'))
        self.stdout.write(f'Storage type: {storage_type}')
        self.stdout.write(f'Folder: {folder}')
        self.stdout.write('')

        success_count = 0
        error_count = 0

        for image_path in image_paths:
            try:
                # Expand wildcards if needed (for Windows compatibility)
                if '*' in image_path or '?' in image_path:
                    expanded_paths = glob.glob(image_path)
                    if not expanded_paths:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ No files found matching: {image_path}')
                        )
                        continue
                    # Process each expanded path
                    for expanded_path in expanded_paths:
                        result = self._upload_single_image(
                            expanded_path, folder, title, storage_type
                        )
                        if result:
                            success_count += 1
                        else:
                            error_count += 1
                else:
                    result = self._upload_single_image(
                        image_path, folder, title, storage_type
                    )
                    if result:
                        success_count += 1
                    else:
                        error_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error processing {image_path}: {str(e)}')
                )
                error_count += 1

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Upload complete!'))
        self.stdout.write(f'  Success: {success_count}')
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f'  Errors: {error_count}'))

    def _upload_single_image(self, image_path, folder, title, storage_type):
        """Upload a single image file"""
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                self.stdout.write(
                    self.style.ERROR(f'  ✗ File not found: {image_path}')
                )
                return False

            # Get filename for title if not provided
            filename = os.path.basename(image_path)
            image_title = title or os.path.splitext(filename)[0]

            self.stdout.write(f'  Uploading: {filename}...', ending='')

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
            }
            content_type = content_type_map.get(ext, 'image/jpeg')

            if storage_type == 'cloudinary':
                # Upload to Cloudinary - needs a file-like object
                file_obj = BytesIO(file_data)
                file_obj.name = filename
                
                upload_result = upload_to_cloudinary(file_obj, folder=folder)

                # Save to database
                media_asset = MediaAsset.objects.create(
                    title=image_title,
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

                self.stdout.write(
                    self.style.SUCCESS(
                        f' ✓ (ID: {media_asset.id}, URL: {media_asset.original_url[:50]}...)'
                    )
                )
            else:
                # Local file storage
                # Create InMemoryUploadedFile for process_local_image
                uploaded_file = InMemoryUploadedFile(
                    BytesIO(file_data),
                    None,
                    filename,
                    content_type,
                    len(file_data),
                    None
                )

                processed = process_local_image(uploaded_file, folder=folder)

                # Save to database
                media_asset = MediaAsset.objects.create(
                    title=image_title,
                    image_file=processed['image_file'],
                    folder=folder,
                    width=processed['width'],
                    height=processed['height'],
                    format=processed['format'],
                    file_size=processed['file_size'],
                    storage_type='local',
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f' ✓ (ID: {media_asset.id}, Size: {processed["width"]}x{processed["height"]})'
                    )
                )

            return True

        except Exception as e:
            self.stdout.write(self.style.ERROR(f' ✗ Error: {str(e)}'))
            return False
