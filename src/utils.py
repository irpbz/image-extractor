"""
Utility functions for Image Extractor
توابع کمکی برای استخراج کننده تصاویر
"""

import os
import logging
import zipfile
from uuid import uuid4
from pypdf import PdfReader
from PIL import Image
import io


def setup_logging():
    """تنظیمات پایه برای لاگینگ"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('image_extractor.log', encoding='utf-8')
        ]
    )


def generate_uuid_filename(extension):
    """
    تولید نام فایل تصادفی با UUID
    
    Args:
        extension (str): پسوند فایل (.jpg, .png, etc.)
    
    Returns:
        str: نام فایل تصادفی
    """
    return f"{uuid4()}{extension.lower()}"


def ensure_directory_exists(path):
    """
    اطمینان از وجود پوشه
    
    Args:
        path (str): مسیر پوشه
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_supported_formats():
    """
    دریافت لیست فرمت‌های پشتیبانی شده
    
    Returns:
        list: لیست فرمت‌های پشتیبانی شده
    """
    return ['.pdf', '.docx', '.pptx']


def is_supported_format(file_path):
    """
    بررسی اینکه آیا فرمت فایل پشتیبانی می‌شود یا نه
    
    Args:
        file_path (str): مسیر فایل
    
    Returns:
        bool: True اگر پشتیبانی می‌شود
    """
    _, ext = os.path.splitext(file_path)
    return ext.lower() in get_supported_formats()


def get_file_info(file_path):
    """
    دریافت اطلاعات فایل
    
    Args:
        file_path (str): مسیر فایل
    
    Returns:
        dict: اطلاعات فایل
    """
    if not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    _, ext = os.path.splitext(file_path)
    
    return {
        'path': file_path,
        'name': os.path.basename(file_path),
        'extension': ext.lower(),
        'size': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'modified': stat.st_mtime
    }


def convert_jp2_to_png(image_data):
    """
    تبدیل تصویر JP2 به PNG
    
    Args:
        image_data (bytes): داده‌های تصویر JP2
    
    Returns:
        tuple: (data, extension, success)
    """
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            if img.mode == "RGBA":
                img = img.convert("RGB")
            
            image_data_io = io.BytesIO()
            img.save(image_data_io, format="PNG")
            return image_data_io.getvalue(), ".png", True
    except Exception as e:
        logging.error(f"خطا در تبدیل JP2 به PNG: {e}")
        return image_data, ".jp2", False


def normalize_extension(ext):
    """
    نرمال‌سازی پسوند فایل
    
    Args:
        ext (str): پسوند فایل
    
    Returns:
        str: پسوند نرمال‌سازی شده
    """
    ext = ext.lower()
    if ext == ".jpeg":
        return ".jpg"
    return ext


def calculate_progress(current, total):
    """
    محاسبه درصد پیشرفت
    
    Args:
        current (int): مقدار فعلی
        total (int): مقدار کل
    
    Returns:
        int: درصد پیشرفت
    """
    if total == 0:
        return 0
    return int((current / total) * 100)


def format_file_size(size_bytes):
    """
    فرمت کردن سایز فایل برای نمایش خوانا
    
    Args:
        size_bytes (int): سایز فایل به بایت
    
    Returns:
        str: سایز فرمت شده
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"


def clean_filename(filename):
    """
    پاکسازی نام فایل از کاراکترهای غیرمجاز
    
    Args:
        filename (str): نام فایل
    
    Returns:
        str: نام فایل پاکسازی شده
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_output_path(input_file_path):
    """
    تولید مسیر خروجی برای تصاویر استخراج شده
    
    Args:
        input_file_path (str): مسیر فایل ورودی
    
    Returns:
        str: مسیر پوشه خروجی
    """
    base_dir = os.path.dirname(input_file_path)
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_dir_name = f"extracted_images_{clean_filename(file_name)}"
    return os.path.join(base_dir, output_dir_name)


class ImageProcessor:
    """کلاس برای پردازش تصاویر"""
    
    @staticmethod
    def is_valid_image(file_path):
        """
        بررسی معتبر بودن فایل تصویر
        
        Args:
            file_path (str): مسیر فایل تصویر
        
        Returns:
            bool: True اگر فایل معتبر باشد
        """
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_image_dimensions(file_path):
        """
        دریافت ابعاد تصویر
        
        Args:
            file_path (str): مسیر فایل تصویر
        
        Returns:
            tuple: (width, height) یا None در صورت خطا
        """
        try:
            with Image.open(file_path) as img:
                return img.size
        except Exception as e:
            logging.error(f"خطا در دریافت ابعاد تصویر {file_path}: {e}")
            return None
    
    @staticmethod
    def optimize_image(input_path, output_path, quality=85):
        """
        بهینه‌سازی تصویر
        
        Args:
            input_path (str): مسیر فایل ورودی
            output_path (str): مسیر فایل خروجی
            quality (int): کیفیت خروجی (0-100)
        """
        try:
            with Image.open(input_path) as img:
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                img.save(output_path, optimize=True, quality=quality)
                return True
        except Exception as e:
            logging.error(f"خطا در بهینه‌سازی تصویر {input_path}: {e}")
            return False