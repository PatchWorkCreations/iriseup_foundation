import cloudinary
import cloudinary.uploader
import cloudinary.api
from io import BytesIO
from PIL import Image
import os
from django.conf import settings

# Maximum file size (10MB)
MAX_BYTES = 10 * 1024 * 1024
TARGET_BYTES = int(MAX_BYTES * 0.93)  # 9.3MB target after compression


def smart_compress_to_bytes(image_file, target_bytes=TARGET_BYTES, max_quality=85, min_quality=60):
    """
    Compress an image to target size while maintaining quality.
    Uses binary search to find optimal quality.
    """
    try:
        # Open image
        img = Image.open(image_file)
        
        # Convert RGBA to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Get original format
        original_format = img.format or 'JPEG'
        
        # If image is already small enough, return as-is
        output = BytesIO()
        img.save(output, format=original_format, quality=max_quality, optimize=True)
        if len(output.getvalue()) <= target_bytes:
            output.seek(0)
            return output.getvalue(), original_format
        
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
            return best_output, original_format
        
        # If we couldn't compress enough, return minimum quality
        output = BytesIO()
        img.save(output, format=original_format, quality=min_quality, optimize=True)
        return output.getvalue(), original_format
        
    except Exception as e:
        raise Exception(f"Error compressing image: {str(e)}")


def upload_to_cloudinary(image_file, folder='iriseup', public_id=None, transformation=None):
    """
    Upload an image to Cloudinary with smart compression.
    
    Args:
        image_file: File object or BytesIO
        folder: Cloudinary folder path
        public_id: Optional public ID (auto-generated if not provided)
        transformation: Optional transformation string
    
    Returns:
        dict with original_url, web_url, thumbnail_url, public_id, width, height, format, file_size
    """
    try:
        # Check file size
        if hasattr(image_file, 'size'):
            file_size = image_file.size
        else:
            image_file.seek(0, 2)  # Seek to end
            file_size = image_file.tell()
            image_file.seek(0)  # Reset to beginning
        
        # Compress if needed
        if file_size > TARGET_BYTES:
            image_file.seek(0)
            compressed_data, format_type = smart_compress_to_bytes(image_file)
            image_file = BytesIO(compressed_data)
            image_file.name = f"image.{format_type.lower()}"
        
        # Upload to Cloudinary
        upload_options = {
            'folder': folder,
            'resource_type': 'image',
            'use_filename': True,
            'unique_filename': True,
            'overwrite': False,
        }
        
        if public_id:
            upload_options['public_id'] = public_id
        
        if transformation:
            upload_options['transformation'] = transformation
        
        # Perform upload
        result = cloudinary.uploader.upload(
            image_file,
            **upload_options
        )
        
        # Extract data
        public_id = result.get('public_id')
        secure_url = result.get('secure_url', '')
        width = result.get('width')
        height = result.get('height')
        format_type = result.get('format', '')
        bytes_size = result.get('bytes', 0)
        
        # Generate URL variants
        # Web-optimized version (WebP, quality 80, max width 1920)
        web_url = secure_url.replace("/upload/", "/upload/f_webp,q_80,w_1920/")
        
        # Thumbnail version (WebP, quality 70, width 400)
        thumbnail_url = secure_url.replace("/upload/", "/upload/f_webp,q_70,w_400/")
        
        return {
            'original_url': secure_url,
            'web_url': web_url,
            'thumbnail_url': thumbnail_url,
            'public_id': public_id,
            'width': width,
            'height': height,
            'format': format_type,
            'file_size': bytes_size,
        }
        
    except cloudinary.exceptions.Error as e:
        raise Exception(f"Cloudinary upload error: {str(e)}")
    except Exception as e:
        raise Exception(f"Upload error: {str(e)}")


def delete_from_cloudinary(public_id):
    """
    Delete an image from Cloudinary.
    
    Args:
        public_id: Cloudinary public ID
    
    Returns:
        dict with deletion result
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result
    except Exception as e:
        raise Exception(f"Error deleting from Cloudinary: {str(e)}")


def get_cloudinary_url(public_id, transformation=None):
    """
    Generate a Cloudinary URL from public_id.
    
    Args:
        public_id: Cloudinary public ID
        transformation: Optional transformation string
    
    Returns:
        Secure URL string
    """
    try:
        options = {'secure': True}
        if transformation:
            options['transformation'] = transformation
        
        url = cloudinary.utils.cloudinary_url(public_id, **options)[0]
        return url
    except Exception as e:
        raise Exception(f"Error generating URL: {str(e)}")

