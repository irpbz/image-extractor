import logging
import os
import zipfile
from uuid import uuid4
from pypdf import PdfReader
from PIL import Image
import io
import sys

def generate_uuid_filename(extension):
    return f"{uuid4()}{extension.lower()}"

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_images(file_path: str):
    output_path = os.path.join(os.path.dirname(file_path), "extracted_images")
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == ".pdf":
        extract_images_from_pdf(file_path, output_path)
    elif file_extension == ".docx":
        extract_images_from_docx(file_path, output_path)
    elif file_extension == ".pptx":
        extract_images_from_pptx(file_path, output_path)
    else:
        print(f"❌ فرمت فایل پشتیبانی نمی‌شود: {file_extension}")

def extract_images_from_pdf(pdf_file_path: str, output_path: str):
    try:
        print("📖 در حال خواندن فایل PDF...")
        reader = PdfReader(pdf_file_path)
        seen_images = set()
        ensure_directory_exists(output_path)
        
        total_pages = len(reader.pages)
        print(f"📄 تعداد صفحات: {total_pages}")
        
        for i, page in enumerate(reader.pages):
            print(f"🔄 در حال پردازش صفحه {i+1} از {total_pages}")
            
            for image in page.images:
                image_data = image.data
                image_hash = hash(image_data)

                if image_hash in seen_images:
                    continue

                seen_images.add(image_hash)

                ext = os.path.splitext(image.name)[1].lower()
                if ext == ".jpeg":
                    ext = ".jpg"
                elif ext == ".jp2":
                    try:
                        with Image.open(io.BytesIO(image_data)) as img:
                            if img.mode == "RGBA":
                                img = img.convert("RGB")
                            ext = ".png"
                            image_data = io.BytesIO()
                            img.save(image_data, format="PNG")
                            image_data = image_data.getvalue()
                    except Exception as e:
                        print(f"❌ خطا در تبدیل JP2 به PNG: {e}")
                        continue

                image_filename = generate_uuid_filename(ext)
                file_path = os.path.join(output_path, image_filename)
                with open(file_path, "wb") as fp:
                    fp.write(image_data)
                
                print(f"✅ تصویر ذخیره شد: {image_filename}")
        
        print(f"🎉 استخراج کامل شد! تعداد تصاویر استخراج شده: {len(seen_images)}")
        
    except Exception as e:
        print(f"❌ خطا در استخراج از PDF: {e}")

def extract_images_from_docx(docx_file_path: str, output_path: str):
    try:
        ensure_directory_exists(output_path)
        print("📝 در حال استخراج از فایل Word...")
        
        with zipfile.ZipFile(docx_file_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.startswith('word/media/'):
                    zip_ref.extract(file_info, output_path)
                    filename = os.path.basename(file_info.filename)
                    original_path = os.path.join(output_path, filename)
                    
                    if os.path.exists(original_path):
                        _, ext = os.path.splitext(filename)
                        if ext.lower() == ".jpeg":
                            ext = ".jpg"
                        elif ext.lower() == ".jp2":
                            try:
                                with Image.open(original_path) as img:
                                    if img.mode == "RGBA":
                                        img = img.convert("RGB")
                                    ext = ".png"
                                    img.save(original_path, format="PNG")
                            except Exception as e:
                                print(f"❌ خطا در تبدیل JP2 به PNG: {e}")
                                os.remove(original_path)
                                continue

                        new_filename = generate_uuid_filename(ext)
                        new_path = os.path.join(output_path, new_filename)
                        os.rename(original_path, new_path)
                        print(f"✅ تصویر ذخیره شد: {new_filename}")
        
        print("🎉 استخراج از فایل Word کامل شد!")
        
    except Exception as e:
        print(f"❌ خطا در استخراج از Word: {e}")

def extract_images_from_pptx(pptx_file_path: str, output_path: str):
    try:
        ensure_directory_exists(output_path)
        print("🎨 در حال استخراج از فایل PowerPoint...")
        
        with zipfile.ZipFile(pptx_file_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.startswith('ppt/media/'):
                    zip_ref.extract(file_info, output_path)
                    filename = os.path.basename(file_info.filename)
                    original_path = os.path.join(output_path, filename)
                    
                    if os.path.exists(original_path):
                        _, ext = os.path.splitext(filename)
                        valid_extensions = {".jpg", ".jpeg", ".png", ".jp2"}
                        
                        if ext.lower() == ".jpeg":
                            ext = ".jpg"
                        elif ext.lower() == ".jp2":
                            try:
                                with Image.open(original_path) as img:
                                    if img.mode == "RGBA":
                                        img = img.convert("RGB")
                                    ext = ".png"
                                    img.save(original_path, format="PNG")
                            except Exception as e:
                                print(f"❌ خطا در تبدیل JP2 به PNG: {e}")
                                os.remove(original_path)
                                continue
                        
                        if ext.lower() in valid_extensions:
                            new_filename = generate_uuid_filename(ext)
                            new_path = os.path.join(output_path, new_filename)
                            os.rename(original_path, new_path)
                            print(f"✅ تصویر ذخیره شد: {new_filename}")
                        else:
                            os.remove(original_path)
        
        print("🎉 استخراج از فایل PowerPoint کامل شد!")
        
    except Exception as e:
        print(f"❌ خطا در استخراج از PowerPoint: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("💡 روش استفاده:")
        print("python cli_extractor.py <مسیر-فایل>")
        print("\nمثال:")
        print('python cli_extractor.py "C:\\Users\\user-name\\Documents\\document.pdf"')
        sys.exit(1)

    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ فایل پیدا نشد: {file_path}")
        sys.exit(1)
    
    extract_images(file_path)