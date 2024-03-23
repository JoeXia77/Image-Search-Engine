# Image Search Engine

Semantic search for images: this project utilizes AI models to generate descriptions of images, employs semantic search to query appropriate images, and provides a user-friendly interaction experience using AWS and GPTs.

## Final Product

[https://chat.openai.com/g/g-r63fklZ0Y-image-search-engine](https://chat.openai.com/g/g-r63fklZ0Y-image-search-engine)

## Demo Video

Contains a step-by-step implementation of this project.

...

## Usage

- `Download_images.py`: Used to download images from Pexels. The images will be processed locally to generate their descriptions.

- `image_to_description.py`: Used to generate descriptions of images.

- `description_encode_upsert.py`: Converts the descriptions into sentence embeddings, then upserts them into a vector database.

- `Lambda.py`: Serves as the backend for user interactions, queries images according to user requests, and generates a user-friendly HTML page as an image viewer.

## Requirements

- A GPU is needed to generate descriptions of images.
- API keys are required from OpenAI, Pinecone, and Pexels.














