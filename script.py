import csv
import time
import requests
from instagrapi import Client
from io import BytesIO
from PIL import Image

cl = Client()

# Login to Instagram
cl.login(username='instagram_username', password='instagram_password')

# Path to your CSV file
csv_file_path = 'PATH TO CSV'

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

# Function to enhance title (simplified version)
def enhance_title_with_emojis(title):
    return f"{title.capitalize()}"

# Open and read the CSV file, handle BOM
with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    # Print the headers to check for issues
    headers = reader.fieldnames
    print(f"Headers found: {headers}")
    
    for row in reader:
        try:
            # Access the CSV columns, ensuring they exist and stripping any potential whitespace
            image_url = row['Media URL'].strip() if 'Media URL' in row else None
            title = row['Title'].strip() if 'Title' in row else None
            affiliate_link = row['Link'].strip() if 'Link' in row else None
            keywords = row.get('Keywords', '').strip()  # Use .get to handle missing keywords
            
            # Verify that all required fields are present
            if not image_url or not title or not affiliate_link:
                print(f"Missing required fields in row: {row}")
                continue
            
            # Create hashtags from keywords
            hashtags = create_hashtags(keywords)
            
            # Enhance the title (simplified)
            enhanced_title = enhance_title_with_emojis(title)
            
            # Add emojis around the affiliate link
            affiliate_link_with_emojis = f"👉 {affiliate_link} 👈"
            
            # Additional promotional text
            promo_text = (
                "🔥 Get 30% OFF Now! 🔥"
            )
            
            # Compose the full caption with priority: affiliate link (with emojis), formatted title, hashtags, and promo text
            caption = f"{affiliate_link_with_emojis}\n\n{enhanced_title}\n\n{hashtags}\n\n{promo_text}"
            
            # Print the caption and image path for debugging purposes
            print(f"Uploading: {image_url} with caption: {caption}")
            
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
                
                # Introduce a delay between posts
                time.sleep(20)  # Increase delay to 20 seconds
                
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
