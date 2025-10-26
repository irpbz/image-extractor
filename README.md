# 🖼️ Image Extractor
A powerful and user-friendly Python application for extracting images from PDF, Word, and PowerPoint files with both graphical and command-line interfaces.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macOS-lightgrey)

## ✨ Features

- **📁 Multi-format Support**: Extract images from PDF, Word (.docx), and PowerPoint (.pptx) files
- **🎯 Smart Processing**: Automatic format conversion and duplicate detection
- **💻 Dual Interface**: Both GUI and CLI versions included
- **🖼️ Format Conversion**: Automatic JP2 to PNG conversion with RGB optimization
- **🔒 Unique Naming**: UUID-based filenames to prevent conflicts
- **📊 Progress Tracking**: Real-time progress updates in GUI version
- **🔄 Batch Ready**: Command-line interface suitable for batch processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/irpbz/image-extractor.git
   cd image-extractor

### Install dependencies:
pip install -r requirements.txt

### Usage
#### Graphical User Interface (Recommended for beginners):

python src/gui_extractor.py

#### Command Line Interface (For advanced users & automation):

#### Basic usage
python src/cli_extractor.py "path/to/your/file.pdf"

#### Example with different file types
python src/cli_extractor.py "document.docx"

python src/cli_extractor.py "presentation.pptx"



   # 🖼️ استخراج کننده تصاویر

یک برنامه پایتون قدرتمند و کاربرپسند برای استخراج تصاویر از فایل‌های PDF، Word و PowerPoint با رابط گرافیکی و خط فرمان.

![نسخه پایتون](https://img.shields.io/badge/python-3.8%2B-blue)
![لایسنس](https://img.shields.io/badge/license-MIT-green)
![پلتفرم](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macOS-lightgrey)

## ✨ ویژگی‌ها

- **📁 پشتیبانی چندفرمت**: استخراج تصاویر از فایل‌های PDF، Word و PowerPoint
- **🎯 پردازش هوشمند**: تبدیل خودکار فرمت و تشخیص تصاویر تکراری
- **💻 رابط دوگانه**: نسخه گرافیکی و خط فرمان
- **🖼️ تبدیل فرمت**: تبدیل خودکار JP2 به PNG با بهینه‌سازی RGB
- **🔒 نام‌گذاری یکتا**: نام فایل‌های مبتنی بر UUID برای جلوگیری از تداخل
- **📊 ردیابی پیشرفت**: نمایش پیشرفت عملیات در نسخه گرافیکی
- **🔄 آماده پردازش گروهی**: رابط خط فرمان مناسب برای پردازش دسته‌ای

## 🚀 شروع سریع

### پیش‌نیازها

- پایتون ۳.۸ یا بالاتر
- pip (مدیریت بسته‌های پایتون)

### نصب

۱. **دانلود مخزن**:
   ```bash
   git clone https://github.com/irpbz/image-extractor.git
   cd image-extractor


   نصب وابستگی‌ها:

pip install -r requirements.txt

# نحوه استفاده
:رابط گرافیکی (توصیه شده برای کاربران مبتدی)

python src/gui_extractor.py

# رابط خط فرمان (برای کاربران حرفه‌ای و اتوماسیون): 

# استفاده پایه
python src/cli_extractor.py "مسیر/فایل/شما.pdf"

# مثال با انواع مختلف فایل
python src/cli_extractor.py "document.docx"
python src/cli_extractor.py "presentation.pptx"
