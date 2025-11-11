# AI WARRANTY CHECKER  
Automated Warranty Verification using AI & Computer Vision  

---

## 🎯 Project Overview  
**AI WARRANTY CHECKER** is a Python-based tool designed to streamline the process of verifying product warranties. It uses Optical Character Recognition (OCR) and computer vision techniques to extract warranty details (such as issuance date, serial number, model, and expiry) from invoices/receipts and cross-checks them against expected warranty parameters. Ideal for service centres, consumer-electronics resellers or any business that needs to expedite warranty verification at scale.

---

## 🔍 Features  
- Quickly scan invoice images (JPEG/PNG/PDF) and extract text using OCR.  
- Parse the extracted text to locate warranty‐relevant fields: serial number, issue date, expiry date, product model.  
- Automatically compute remaining warranty duration or detect expired warranties.  
- Batch-process multiple files to save time on manual verification.  
- Configurable: update patterns/regEx for different brands or invoice formats.  
- Lightweight and simple to deploy.

---

## 🧩 Project Structure  

---

## 🚀 Getting Started  

### Prerequisites  
- Python 3.8+  
- (Optional) Virtual environment tool like `venv` or `conda`.  

### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/Adarsh-Me/AI_WARRANTY_CHECKER.git
   cd AI_WARRANTY_CHECKER
OCR_API_KEY=your_api_key_here
LOG_LEVEL=INFO
