# NIQ Innovation Enablement - Challenge 1 (Object Counting)

## Task 1: Add New Service Endpoint
1. Added a new service endpoint to receive an image and the desired threshold, returning a list of predictions.
2. The endpoint `object-counter-pg` is added in `counter/entrypoints/webapp.py`.
3. Implemented proper error handling for the endpoint.

## Task 2: Add New Adapter for Postgres DB
1. Created a new adapter for PostgreSQL to store captured metadata.
2. **Table Details:**
   - **Table Name:** `object_counts`
   - **Columns:**
     - `id` (Primary Key)
     - `object_class` (VARCHAR)
     - `count` (INTEGER)
     - `updated_at` (TIMESTAMP)
3. The `count` column updates if the same `object_class` is detected in another image.
4. The adapter is responsible for:
   - Upserting captured metadata into the table.
   - Retrieving metadata from the table.

## Task 3: Code Review and Improvements

### Code Review
- The code follows **Hexagonal Architecture**.

### Improvements
1. Add an **admin endpoint** to provide a holistic view of all detected objects --- Implemented
2. Improve **error handling** --- Implemented
3. Implement **Streamlit** as a user-friendly interface for the API. ---- Implemented
4. Reduce **manual setup effort** for the project. --- Implemeted (Added MAKE file)
5. Implement **batch processing** to allow multiple images for object detection. --- Implemented
6. Introduce **API authentication** using a JWT token. 
7. Store **model inference metadata** including detection time.
