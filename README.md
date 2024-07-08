# Instagram Post Automation Script

## Introduction

This simple script automates the process of uploading posts to Instagram with images, captions generated from a CSV file. It uses the `instagrapi` library for interacting with Instagram, and `requests` and `Pillow` libraries for handling images. You can modify Promo text inside the script in param name "promo_text"

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Install the Required Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```


3. **Configure Your Credentials**
   ```code
   cl.login(username='your_instagram_username', password='your_instagram_password')
   ```

4. **Specify the Path to Your CSV File**
   ```code
   csv_file_path = 'path/to/your/csvfile.csv'
   ```

4. **Run the script**
   ```code
   python script.py
   ```