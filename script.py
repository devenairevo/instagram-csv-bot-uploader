import csv
import time
import requests
import random
from instagrapi import Client
from io import BytesIO
from PIL import Image

cl = Client()

# Login to Instagram
cl.login(username='YOUR_USERNAME', password='YOUR_PASSWORD')

# Path to your CSV file
csv_file_path = 'output.csv'

sliptime_min, sleeptime_max = 120, 300

# Function to create hashtags from keywords
def create_hashtags(keyword_string):
    keywords = keyword_string.split(',')
    hashtags = set()
    
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:
            words = keyword.split()
            for word in words:
                hashtags.add(f"#{word}")
            hashtags.add(f"#{keyword.replace(' ', '')}")
    
    return ' '.join(hashtags)

# Open and read the CSV file, handle BOM
with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    # Print the headers to check for issues
    headers = reader.fieldnames
    
    for row in reader:
        try:
            # Introduce a random delay between 2 to 4 minutes before processing each row
            sleep_time = random.randint(sliptime_min, sleeptime_max)
            print(f"Sleeping for {sleep_time} seconds before processing next post.")
            time.sleep(sleep_time)
            
            # Access the CSV columns, ensuring they exist and stripping any potential whitespace
            image_url = row['Media URL'].strip() if 'Media URL' in row else None
            title = row['Title'].strip().replace('"', '') if 'Title' in row else None
            affiliate_link = row['Link'].strip() if 'Link' in row else None
            keywords = row.get('Keywords', '').strip()  # Use .get to handle missing keywords
            
            # Verify that all required fields are present
            if not image_url or not title or not affiliate_link:
                print(f"Missing required fields in row: {row}")
                continue
            
            # Create hashtags from keywords
            hashtags = create_hashtags(keywords)
            
            # Keep the title as is without modification, removing quotes
            enhanced_title = title
            
            # Add emojis around the affiliate link
            affiliate_link_with_emojis = f"👉 {affiliate_link} 👈"
            
            # Additional promotional text
            promo_text = (
                "🔥 Get 30% OFF Now! 🔥\n"
                "- ℹ️ Discover unbeatable deals and elevate your style.\n"
                "- 🔎 Just search for 👉 acq885235 👈 in the Temu App and unlock exclusive savings.\n"
                "- 🔥 Don't miss out – this offer is available for a limited time! ⏱️\n\n"
                "*Affiliate"
            )
            
            # Compose the full caption with priority: affiliate link (with emojis), formatted title, hashtags, and promo text
            caption = f"{affiliate_link_with_emojis}\n\n{enhanced_title}\n\n{hashtags}" #f"{affiliate_link_with_emojis}\n\n{enhanced_title}\n\n{hashtags}\n\n{promo_text}"
            
            # Print the caption and image path for debugging purposes
            print(f"\nUploading: {image_url} with caption: {caption}")
            
            # Download the image from the URL
            response = requests.get(image_url)
            if response.status_code == 200:
                # Open the image using PIL
                image = Image.open(BytesIO(response.content))
                
                # Save the image to a temporary file
                temp_image_path = 'temp_image.' + image.format.lower()
                image.save(temp_image_path)

                # Upload the image with the caption
                cl.photo_upload(temp_image_path, caption)         
            else:
                print(f"Failed to download image: {image_url}")
        
        except KeyError as e:
            print(f"KeyError: {e}. Check if the CSV file contains the correct headers.")
            continue
        except Exception as ex:
            print(f"Error occurred: {str(ex)}")
            continue

# Logout after completing the posts
cl.logout()
