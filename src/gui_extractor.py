import logging
import os
import subprocess
import zipfile
from uuid import uuid4
from pypdf import PdfReader
from PIL import Image
import io
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
from utils import (
    generate_uuid_filename, 
    ensure_directory_exists,
    is_supported_format,
    get_file_info,
    convert_jp2_to_png,
    normalize_extension,
    calculate_progress,
    format_file_size,
    get_output_path,
    ImageProcessor
)

class ImageExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Extractor")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # متغیرها
        self.file_path = tk.StringVar()
        self.status_text = tk.StringVar(value="آماده")
        self.progress_value = tk.IntVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        # فریم اصلی
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # عنوان
        title_label = ttk.Label(main_frame, text="استخراج کننده تصاویر", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # انتخاب فایل
        file_frame = ttk.LabelFrame(main_frame, text="انتخاب فایل", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(file_frame, text="فایل:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(file_frame, text="مرور...", command=self.browse_file).grid(row=0, column=2)
        
        # اطلاعات پشتیبانی
        info_text = """
پشتیبانی از فرمت‌های زیر:
• PDF (.pdf)
• Word (.docx)  
• PowerPoint (.pptx)

تصاویر استخراج شده در پوشه extracted_images ذخیره می‌شوند.
        """
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # دکمه‌های عملیات
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Button(button_frame, text="استخراج تصاویر", command=self.start_extraction, style="Accent.TButton").grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="باز کردن پوشه خروجی", command=self.open_output_folder).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="خروج", command=self.root.quit).grid(row=0, column=2)
        
        # نوار پیشرفت
        progress_frame = ttk.LabelFrame(main_frame, text="پیشرفت", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_value, maximum=100)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(progress_frame, textvariable=self.status_text).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # لاگ
        log_frame = ttk.LabelFrame(main_frame, text="لاگ عملیات", padding="5")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # تنظیم وزن برای ریسایز
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def browse_file(self):
        file_types = [
            ("فایل‌های پشتیبانی شده", "*.pdf *.docx *.pptx"),
            ("فایل‌های PDF", "*.pdf"),
            ("فایل‌های Word", "*.docx"),
            ("فایل‌های PowerPoint", "*.pptx")
        ]
        
        filename = filedialog.askopenfilename(
            title="انتخاب فایل",
            filetypes=file_types
        )
        
        if filename:
            self.file_path.set(filename)
            self.log(f"فایل انتخاب شد: {filename}")
    
    def start_extraction(self):
        if not self.file_path.get():
            messagebox.showerror("خطا", "لطفاً یک فایل انتخاب کنید")
            return
        
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror("خطا", "فایل انتخاب شده وجود ندارد")
            return
        
        # اجرا در thread جداگانه برای جلوگیری از freeze شدن GUI
        thread = Thread(target=self.extract_images_thread)
        thread.daemon = True
        thread.start()
    
    def extract_images_thread(self):
        try:
            self.progress_value.set(0)
            self.status_text.set("در حال استخراج...")
            
            file_path = self.file_path.get()
            self.log(f"شروع استخراج از: {file_path}")
            
            # فراخوانی تابع استخراج اصلی
            success = self.extract_images(file_path)
            
            if success:
                self.progress_value.set(100)
                self.status_text.set("استخراج با موفقیت انجام شد")
                self.log("استخراج با موفقیت انجام شد")
                messagebox.showinfo("موفقیت", "تصاویر با موفقیت استخراج شدند")
            else:
                self.status_text.set("خطا در استخراج")
                messagebox.showerror("خطا", "خطایی در استخراج تصاویر رخ داد")
                
        except Exception as e:
            self.log(f"خطا: {str(e)}")
            self.status_text.set("خطا")
            messagebox.showerror("خطا", f"خطایی رخ داد: {str(e)}")
    
    def log(self, message):
        def update_log():
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)
            self.root.update()
        
        self.root.after(0, update_log)
    
    def open_output_folder(self):
        file_path = self.file_path.get()
        if file_path and os.path.exists(file_path):
            output_path = os.path.join(os.path.dirname(file_path), "extracted_images")
            if os.path.exists(output_path):
                try:
                    if sys.platform == "win32":
                        os.startfile(output_path)
                    elif sys.platform == "darwin":  # macOS
                        subprocess.run(["open", output_path])
                    else:  # linux
                        subprocess.run(["xdg-open", output_path])
                except Exception as e:
                    messagebox.showerror("خطا", f"نتوانست پوشه را باز کند: {str(e)}")
            else:
                messagebox.showwarning("هشدار", "پوشه خروجی هنوز وجود ندارد")
        else:
            messagebox.showwarning("هشدار", "لطفاً ابتدا یک فایل انتخاب کنید")
    
    # توابع استخراج (همان توابع قبلی با کمی تغییر)
    def generate_uuid_filename(self, extension):
        return f"{uuid4()}{extension.lower()}"
    
    def ensure_directory_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def extract_images(self, file_path: str):
        try:
            output_path = os.path.join(os.path.dirname(file_path), "extracted_images")
            _, file_extension = os.path.splitext(file_path)
            file_extension = file_extension.lower()
            
            self.log(f"در حال پردازش فایل با پسوند: {file_extension}")
            
            if file_extension == ".pdf":
                return self.extract_images_from_pdf(file_path, output_path)
            elif file_extension == ".docx":
                return self.extract_images_from_docx(file_path, output_path)
            elif file_extension == ".pptx":
                return self.extract_images_from_pptx(file_path, output_path)
            else:
                self.log(f"فرمت فایل پشتیبانی نمی‌شود: {file_extension}")
                return False
        except Exception as e:
            self.log(f"خطا در استخراج: {str(e)}")
            return False
    
    def extract_images_from_pdf(self, pdf_file_path: str, output_path: str):
        try:
            self.log("در حال خواندن فایل PDF...")
            reader = PdfReader(pdf_file_path)
            seen_images = set()
            self.ensure_directory_exists(output_path)
            
            total_pages = len(reader.pages)
            self.log(f"تعداد صفحات: {total_pages}")
            
            for i, page in enumerate(reader.pages):
                self.progress_value.set(int((i / total_pages) * 100))
                self.status_text.set(f"در حال پردازش صفحه {i+1} از {total_pages}")
                
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
                            self.log(f"خطا در تبدیل JP2 به PNG: {e}")
                            continue
                    
                    image_filename = self.generate_uuid_filename(ext)
                    file_path = os.path.join(output_path, image_filename)
                    with open(file_path, "wb") as fp:
                        fp.write(image_data)
                    
                    self.log(f"تصویر ذخیره شد: {image_filename}")
            
            self.log(f"تعداد تصاویر استخراج شده: {len(seen_images)}")
            return True
        except Exception as e:
            self.log(f"خطا در استخراج از PDF: {e}")
            return False
    
    def extract_images_from_docx(self, docx_file_path: str, output_path: str):
        try:
            self.ensure_directory_exists(output_path)
            self.log("در حال استخراج از فایل Word...")
            
            # استفاده از zipfile به جای unzip
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
                                    self.log(f"خطا در تبدیل JP2 به PNG: {e}")
                                    os.remove(original_path)
                                    continue
                            
                            new_filename = self.generate_uuid_filename(ext)
                            new_path = os.path.join(output_path, new_filename)
                            os.rename(original_path, new_path)
                            self.log(f"تصویر ذخیره شد: {new_filename}")
            
            return True
        except Exception as e:
            self.log(f"خطا در استخراج از Word: {e}")
            return False
    
    def extract_images_from_pptx(self, pptx_file_path: str, output_path: str):
        try:
            self.ensure_directory_exists(output_path)
            self.log("در حال استخراج از فایل PowerPoint...")
            
            # استفاده از zipfile به جای unzip
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
                                    self.log(f"خطا در تبدیل JP2 به PNG: {e}")
                                    os.remove(original_path)
                                    continue
                            
                            if ext.lower() in valid_extensions:
                                new_filename = self.generate_uuid_filename(ext)
                                new_path = os.path.join(output_path, new_filename)
                                os.rename(original_path, new_path)
                                self.log(f"تصویر ذخیره شد: {new_filename}")
                            else:
                                os.remove(original_path)
            
            return True
        except Exception as e:
            self.log(f"خطا در استخراج از PowerPoint: {e}")
            return False

def main():
    # ایجاد پنجره اصلی
    root = tk.Tk()
    
    # تنظیم تم تاریک (اختیاری)
    style = ttk.Style()
    style.theme_use('clam')
    
    # ایجاد برنامه
    app = ImageExtractorGUI(root)
    
    # اجرای حلقه اصلی
    root.mainloop()

if __name__ == "__main__":
    main()