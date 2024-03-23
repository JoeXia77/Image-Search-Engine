import os
import json
import concurrent.futures
## from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

class FileProcessor:
    def __init__(self):
        ## self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.pc = Pinecone(api_key='1e82...')
        self.index = self.pc.Index('image-descriptions')
        self.client = OpenAI(api_key="sk-sty...")

    # Example function to get embedding
    def get_embedding(self, text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        embedding_result = self.client.embeddings.create(input=[text], model=model)
        return embedding_result.data[0].embedding


    def process_files(self, files):
        for source_file_path, output_file_path in files:
            self.process_file(source_file_path, output_file_path)

    def process_file(self, source_file_path, output_file_path):
        ## from each file:
        ## get the description of the image
        ## calculate embedding
        ## upsert to database
        ## create a shadow copy in local
        
        with open(source_file_path, 'r') as file:
            content = json.loads(file.read())
        
        image_id = content['id']
        if "prompt" not in content:
            print("Error, file is missing 'prompt'")
            print(source_file_path)
            return
        prompt = content['prompt'].split(',')[0]
        alt = content['alt']
        
        metadata = {'url': content['url'], 'image_original_url': content['src']['original']}
        
        vector_values = []

        data_id = f'{image_id}_{2}'
        ## prompt_embedding = self.model.encode(prompt).tolist()
        ## alt_embedding = self.model.encode(alt).tolist()
        
        prompt_embedding = self.get_embedding(prompt)
        alt_embedding = self.get_embedding(alt)
        
        combined_embedding = [0.8 * a + 0.2 * b for a, b in zip(prompt_embedding, alt_embedding)]
        vector_values.append({'id': data_id, 'values': combined_embedding, 'metadata': metadata})
        
        self.index.upsert(vectors=vector_values)
        
        content['embeddings'] = vector_values
        
        with open(output_file_path, 'w') as outfile:
            json.dump(content, outfile)

def split_list_into_n_parts(lst, n):
    # Calculate the size of each sublist
    sublist_size = (len(lst) + n - 1) // n  # Ensures more even distribution

    # Initialize a list to hold the sublists
    sublists = []

    # Iterate and slice the list into sublists
    for i in range(0, len(lst), sublist_size):
        sublists.append(lst[i:i + sublist_size])

    return sublists

# Main script
source_path = "Output_description"
output_path = "Description_embeddings"
if not os.path.exists(output_path):
    os.makedirs(output_path)

## split files into n groups for multithread processing
all_files = [f for f in os.listdir(source_path) if f.endswith('.txt')]
file_parts = split_list_into_n_parts(all_files, 10)

# Prepare the file paths for processing
file_paths_for_processing = []
for part in file_parts:
    part_file_paths = []
    for filename in part:
        output_file_path = os.path.join(output_path, filename)
        if not os.path.exists(output_file_path):
            source_file_path = os.path.join(source_path, filename)
            part_file_paths.append((source_file_path, output_file_path))
    file_paths_for_processing.append(part_file_paths)

# Process each part in a separate thread
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    futures = []
    for file_group in file_paths_for_processing:
        processor = FileProcessor()
        futures.append(executor.submit(processor.process_files, file_group))

    # Wait for all threads to complete
    concurrent.futures.wait(futures)



