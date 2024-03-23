import requests
import json
import os
import time

    
    
    
    
    
    
def get_collcetion_info(page_i, per_page = 80):
    # Set up the URL and headers
    url = "https://api.pexels.com/v1/collections/featured"
    headers = {
        "Authorization": "O958Y..."
    }
    
    # Set the parameters for the request
    params = {
        "page" : page_i,
        "per_page": per_page
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Print the response text (or you can process it)
        return response.text
    else:
        return 0
    


def query_keyword(keyword, page_i, per_page):
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": "O958Y..."
    }
    
    # Set the parameters for the request
    params = {
        "query": keyword,
        "page" : page_i,
        "per_page": per_page
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Print the response text (or you can process it)
        return response.text
    else:
        return 0
    
def save_to_json_file(collections, filename):
    with open(filename, 'w') as file:
        json.dump(collections, file, indent=4)



def set_download_goal(keyword, download_amount):
    ## output a list of dicts, with information that should be downloaded
    print(keyword, download_amount)
    per_page = 80
    query_times = download_amount // per_page
    remains = download_amount % per_page
    
    info_list = []
    
    last_page = 0
    valid_count = 0
    for page_i in range(1, query_times+1):
        query_result = query_keyword(keyword, page_i, per_page)
        ## api has limit of 200 call per hour
        time.sleep(40)
        print("######################")
        print(keyword, page_i, per_page, query_result)
        if type(query_result) == type("abc") and len(query_result)>0:
            query_result = json.loads(query_result)
            info_list += query_result['photos']
            valid_count+=1
        last_page = page_i
    
    if remains and last_page!=-1:
        print(2)
        query_result = query_keyword(keyword, last_page+1, remains)
        if type(query_result) == type("abc") and len(query_result)>0:
            query_result = json.loads(query_result)
            info_list += query_result['photos']
            valid_count+=1
    print(keyword, f'number of pictures found: {valid_count}')
    
    
    return info_list

## given a keyword, with number of pictures want to download
## query informatino for those images
## decide whether to download it
## download it and write the info to an txt file




    
def download_images(download_goal):
    output_folder = "Images"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    start_i = 0
    length = len(download_goal)
    for i in range(start_i,length):
        print(f'Image: {i}')
        item = download_goal[i]
        url = item['src']["original"]

        # Extract image ID and type from URL
        image_id = item['id']
        image_type = url.split('.')[-1]
        
        if len(image_type) > 7:
            raise ValueError(f"Unexpected image type length for URL {url}")

        # Path for the image and metadata file
        image_path = os.path.join(output_folder, f"{image_id}.{image_type}")
        metadata_path = os.path.join(output_folder, f"{image_id}.txt")

        # Check if the image already exists, if not, download it
        if not os.path.exists(image_path):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad status codes

                # Write the image data to a file
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                print(f"Image {image_id} downloaded.")
            except requests.RequestException as e:
                print(f"Error downloading {url}: {e}")

        # Save the metadata
        with open(metadata_path, 'w') as file:
            json.dump(item, file)
        print(f"Metadata for image {image_id} saved.")



keywords = []

"""

for keyword in ["Travel","Cities","Architecture","aquatic", "drone view"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 1800)
    download_images(download_goal)
    



for keyword in ["Relax","Transportation","Animals","Food","vintage","spring","summer","autumn","winter","hiking","adventure","cozy","design"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 1200)
    download_images(download_goal)


for keyword in ["Buildings","People","Urban Living","Vintage","Wildlife"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 1050)
    download_images(download_goal)




for keyword in ["Bright Colours", "One Color", "Tourists", "Nature Wallpapers",
                "Portraits", "Textures", "PC Wallpapers", "Beach", "Cosplay",
                "Graffiti", "Spooky", "Rooms", "Office Life", "Cute Animal Wallpapers",
                "Tasty Food", "Cars", "Portraits in monochrome", "Classrooms", "Smile",
                "Night", "Roads", "Neon Wallpapers", "Digital Devices", "Flowers",
                "Wedding Dresses", "Robots", "dog", "Eating", "Markets", "Hotels",
                "Chairs", "drink", "cup", "lake", "family", "food photography", "disease", "mask", "money", "shopping"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 800)
    download_images(download_goal)





for keyword in ["Tables", "Bikes", "Office Space", "Living in Luxury", "Luxury",
                "Road Trip", "Simple Backgrounds", "Space Wallpapers", "Autumn Wallpapers",
                "Pastel Backgrounds", "Winter Wallpapers", "Pursuit of Portraits",
                "Painting", "Christmas Wallpapers", "cafe", "Astrophotography", "Desks",
                "Bookshelves", "Mental health & wellbeing", "Country Roads", "Cyberpunk",
                "Weight Loss", "Sea", "Ocean life", "Seascapes", "Oceans", "Ocean Backgrounds",
                "At The Beach", "Coastal Life", "Beach Life", "Beautiful Beaches",
                "Sailboats For Mary", "Marine Life", "Boats", "The Earth", "Ships", "Islands",
                "The Mediterranean", "Skylines", "Night Time", "Lights & Shadows",
                "Night Lights", "People At Night", "Motorcycles", "Starry Skies", "Night Skies",
                "Blue Skies", "Aurora", "Rain", "Rain Backgrounds", "sky", "Stormy Weather",
                "Clouds", "Morning Sun", "Rainbow", "Street Photography", "Paris", "Beijing",
                "Rome", "New York City", "Cusco", "Agra", "Arizona", "Sydney", "Dubai",
                "Santorini", "Niagara", "Tokyo", "London", "Yellowstone", "Wiltshire",
                "Rio de Janeiro", "Cairo", "Athens", "Venice", "Amsterdam", "Doors", "Piano",
                "Bars", "Stage", "Crowds", "Real Estate", "Highways", "Technology",
                "Take A Walk With Me", "Still Life", "Self Care", "Cheers", "LOVE", "Health",
                "Holding Hands", "Life At Home", "Socials", "Lonely", "Happy", "Peace", "Dream",
                "Happy Kids", "Dark & Moody", "Cities At Night", "Neon Lights", "Streets At Night",
                "Bonfire Night", "Cozy Fires", "Glasses", "Retro Dreams", "Neon Signs", "Smoke",
                "Light Leaks", "Champagne", "Lightning", "Abstract", "Write It Down", "Ascend",
                "Studying", "Papers", "Sports", "Run", "Law", "Freedom", "Minimalism", "Education",
                "Girl power", "Fantasy", "Golf", "Coding", "Electricity", "Roller skates", "Cycling"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 400)
    download_images(download_goal)


"""

for keyword in ["Blue Skies", "Aurora", "Rain", "Rain Backgrounds", "sky", "Stormy Weather",
                "Clouds", "Morning Sun", "Rainbow", "Street Photography", "Paris", "Beijing",
                "Rome", "New York City", "Cusco", "Agra", "Arizona", "Sydney", "Dubai",
                "Santorini", "Niagara", "Tokyo", "London", "Yellowstone", "Wiltshire",
                "Rio de Janeiro", "Cairo", "Athens", "Venice", "Amsterdam", "Doors", "Piano",
                "Bars", "Stage", "Crowds", "Real Estate", "Highways", "Technology",
                "Take A Walk With Me", "Still Life", "Self Care", "Cheers", "LOVE", "Health",
                "Holding Hands", "Life At Home", "Socials", "Lonely", "Happy", "Peace", "Dream",
                "Happy Kids", "Dark & Moody", "Cities At Night", "Neon Lights", "Streets At Night",
                "Bonfire Night", "Cozy Fires", "Glasses", "Retro Dreams", "Neon Signs", "Smoke",
                "Light Leaks", "Champagne", "Lightning", "Abstract", "Write It Down", "Ascend",
                "Studying", "Papers", "Sports", "Run", "Law", "Freedom", "Minimalism", "Education",
                "Girl power", "Fantasy", "Golf", "Coding", "Electricity", "Roller skates", "Cycling"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 400)
    download_images(download_goal)





for keyword in ["White", "Dark Colours", "Blue", "Colorful", "Soothing Colours",
                "Red", "Purple", "Black", "Neon Colors", "Pink", "Green", "New York",
                "Abstract Art Backgrounds", "LGBT Wallpapers", "Headshots", "Old Photos",
                "Living Rooms", "Studio", "Home Office", "Bathrooms", "Box", "Take A Walk With Me",
                "Still Life", "T-shirts", "Peaceful", "Strike A Pose", "Female Empowerment",
                "Wellness", "Thumbs Up", "Go To Sleep", "Stress", "Casual Clothes", "Dance",
                "Sad", "Meditation", "Skin Care", "Tiredness", "Massages", "Shake Hands",
                "Yoga", "Virtual Reality", "Laptops", "Butterflies", "Chinese New Year", "Clocks",
                "Earth Day", "Concerts", "Tasty Desserts", "Meat", "Breakfast", "Christmas Time",
                "Christmas Cakes", "Christmas Decorations", "Christmas Gifts", "Christmas",
                "Halloween", "Halloween Costumes", "Halloween Pumpkins"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 300)
    download_images(download_goal)


for keyword in ["Cafe Culture", "Side Profiles", "Frames", "Kitchen Interiors",
                "Work From Home", "Living in Luxury", "Luxury", "Computers", "Gaming",
                "Libraries", "Notebooks", "Call Center", "Pretty Flowers", "Wild Flowers",
                "Flowers in a vase", "One Flower", "White Flowers", "Autumn Flowers",
                "Blue Flowers", "Flower Gardens", "Purple Flowers", "Lotus Flowers",
                "Violets", "Beautiful Bouquets", "Sunflowers", "Pink Roses", "Roses",
                "Poppy Fields", "Tulips", "Roses Are Red", "Toys", "Diet", "Lions",
                "Cute Animals", "Wolves", "Birds", "Cats", "Cute Cats", "Farm Animals",
                "Babies", "Black Cats", "Army", "Horses", "Eagles", "Reptiles", "Cows",
                "Team Work", "Skulls", "Teamwork", "Groups", "Puppies", "Chickens",
                "Monkeys", "Elephants", "Lizards", "Pet Friends", "Deer", "Football Fans",
                "Healthy Food", "Bread", "Veggies", "Dinner", "Chocolate", "Pizza", "Milk",
                "Rice", "Breakfast", "Honey", "Fresh Fruit", "Burgers", "Pasta", "Apples",
                "Bananas"]:
    print(f'######### {keyword} #######')
    keywords.append(keyword)
    download_goal = set_download_goal(keyword, 150)
    download_images(download_goal)

