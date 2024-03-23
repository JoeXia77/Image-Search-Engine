import os
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
import boto3
import json
import uuid

# Example function to get embedding
def get_embedding(client, text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    embedding_result = client.embeddings.create(input=[text], model=model)
    return embedding_result.data[0].embedding


def query_image_urls(index, embedding, query_size = 6):
    query_result = index.query(
            #### change after re-embedding all pictures
            vector=embedding,
            top_k=query_size,
            include_values=False,
            include_metadata=True
        )
    
    # Extract URLs from the metadata of the results
    urls = []
    for match in query_result.get('matches', []):
        metadata = match.get('metadata', {})
        url = metadata.get('url')
        image_original_url = metadata.get('image_original_url')
        urls.append((image_original_url, url))
    return urls


# Function to generate HTML content with image URLs directly
def generate_html_content(urls):

    images_section_1 = ''.join(f'<a href="{source_link}" target="_blank"><img src="{image_url}" alt="Image" /></a>' for image_url, source_link in urls[0:3])
    images_section_2 = ''.join(f'<a href="{source_link}" target="_blank"><img src="{image_url}" alt="Image" /></a>' for image_url, source_link in urls[3:6])
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
<title>Image Viewer</title>
<style>
    .image-row {{
        display: flex;
        justify-content: center;
    }}
    .image-row img {{
        width: auto;
        height: 600px;
        padding: 10px;
    }}
</style>
</head>
<body>
    <div class="image-row">
        {images_section_1}
    </div>
    <div class="image-row">
        {images_section_2}
    </div>
</body>
</html>
""".format(images_section_1=images_section_1, images_section_2=images_section_2)
    return html_content
    
    
# Function to save HTML to S3
def save_html_to_s3(bucket, key, html_content):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=html_content, ContentType='text/html')
    print('HTML file saved to S3')

def generate_public_url(bucket_name, file_name):
    url = f'https://{bucket_name}.s3.us-east-2.amazonaws.com/{file_name}'
    return url


# Lambda handler function
def lambda_handler(event, context):
    
    openai_api_key = os.environ['OPENAI_API_KEY']
    pinecone_api_key = os.environ['PINECONE_API_KEY']

    """
    if "receivedEvent" not in event:
        raise ValueError(f"event do not include receivedEvent, event value: {json.dumps(event)}")
    receivedEvent = event["receivedEvent"]
    
    parameters = receivedEvent.get("queryStringParameters")
    description = parameters.get("description")
    
    if not description:
        # Raise an exception if description is not provided
        event_json = json.dumps(parameters)
        raise ValueError(f"Missing required parameter: description. Received parameters: {event_json}")
    """
    ## raise ValueError(f"the event is: {json.dumps(event)}")
    description = event["queryStringParameters"]["description"]
    print("#######################")
    print(description)
    
    ## description = "There is a book on the grassland"
    

    
    client = OpenAI(api_key=openai_api_key)
    embedding = get_embedding(client, description, model='text-embedding-3-small')

    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index('image-descriptions')
    
    urls = query_image_urls(index, embedding, query_size = 6)

    # Generate the HTML content
    html_content = generate_html_content(urls)
    
    # Define your bucket and HTML file name
    bucket = 'test20240306-image-search-engine'
    html_file_name = f'image-viewer-{uuid.uuid4()}.html'

    # Save the HTML content to S3
    save_html_to_s3(bucket, html_file_name, html_content)
    
    public_url = generate_public_url(bucket, html_file_name)
    
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'public_url': public_url
        })
    }

    return response
    
    
    
    
    
