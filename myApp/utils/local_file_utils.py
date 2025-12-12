import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.conf import settings
import sys

# Maximum file size (10MB)
MAX_BYTES = 10 * 1024 * 1024
TARGET_BYTES = int(MAX_BYTES * 0.93)  # 9.3MB target after compression


def smart_compress_image(image_file, target_bytes=TARGET_BYTES, max_quality=85, min_quality=60):
    """
    Compress an image to target size while maintaining quality.
    Uses binary search to find optimal quality.
    
    Returns: (compressed_file, format_type)
    """
    try:
        # Open image
        img = Image.open(image_file)
        
        # Get original format
        original_format = img.format or 'JPEG'
        
        # Convert RGBA to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # If image is already small enough, return as-is
        output = BytesIO()
        img.save(output, format=original_format, quality=max_quality, optimize=True)
        if len(output.getvalue()) <= target_bytes:
            output.seek(0)
            return output, original_format
        
        # Binary search for optimal quality
        low_quality = min_quality
        high_quality = max_quality
        best_output = None
        best_quality = min_quality
        
        while low_quality <= high_quality:
            mid_quality = (low_quality + high_quality) // 2
            output = BytesIO()
            
            try:
                img.save(output, format=original_format, quality=mid_quality, optimize=True)
                size = len(output.getvalue())
                
                if size <= target_bytes:
                    best_output = output.getvalue()
                    best_quality = mid_quality
                    low_quality = mid_quality + 1
                else:
                    high_quality = mid_quality - 1
            except Exception:
                high_quality = mid_quality - 1
        
        if best_output:
            return BytesIO(best_output), original_format
        
        # If we couldn't compress enough, return minimum quality
        output = BytesIO()
        img.save(output, format=original_format, quality=min_quality, optimize=True)
        return output, original_format
        
    except Exception as e:
        raise Exception(f"Error compressing image: {str(e)}")


def process_local_image(image_file, folder='iriseup'):
    """
    Process and save a local image file.
    
    Args:
        image_file: Django UploadedFile object
        folder: Optional folder name for organization
    
    Returns:
        dict with image_file, width, height, format, file_size
    """
    try:
        # Check file size
        file_size = image_file.size
        
        # Compress if needed
        if file_size > TARGET_BYTES:
            image_file.seek(0)
            compressed_data, format_type = smart_compress_image(image_file)
            compressed_data.seek(0)
            
            # Create a new file-like object
            filename = os.path.splitext(image_file.name)[0] + f'.{format_type.lower()}'
            image_file = ContentFile(compressed_data.read(), name=filename)
        else:
            image_file.seek(0)
            format_type = os.path.splitext(image_file.name)[1][1:].upper() or 'JPEG'
        
        # Get image dimensions
        img = Image.open(image_file)
        width, height = img.size
        image_file.seek(0)
        
        # Get final file size
        if hasattr(image_file, 'size'):
            final_size = image_file.size
        else:
            image_file.seek(0, 2)
            final_size = image_file.tell()
            image_file.seek(0)
        
        return {
            'image_file': image_file,
            'width': width,
            'height': height,
            'format': format_type,
            'file_size': final_size,
        }
        
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")


def delete_local_image(image_path):
    """
    Delete a local image file.
    
    Args:
        image_path: Path to the image file relative to MEDIA_ROOT
    """
    try:
        full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    except Exception as e:
        raise Exception(f"Error deleting local image: {str(e)}")





