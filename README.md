# Trip Planner API

A FastAPI-based backend for generating and editing travel itineraries based on user preferences, using MongoDB Atlas and the Gemini API.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/trip-planner.git
cd trip-planner
```

### 2. Install Dependencies
```bash
# Create and activate a virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```plaintext
MONGO_URI=<your_mongodb_atlas_connection_string>
GEMINI_API_KEY=<your_google_gemini_api_key>
```

### 4. Set Up MongoDB Database
- Ensure MongoDB Atlas is running.
- Add a unique index to the `pois` collection:
  ```javascript
  db.pois.createIndex({"city": 1, "name": 1}, {unique: true})
  ```

### 5. Populate the Database with POIs
```bash
cd backend
python tag_pois_daily.py
```

## Running the Application

Start the FastAPI server:
```bash
cd backend
uvicorn main:app --reload
```
The server runs on `http://localhost:8000`. Access API docs at `http://localhost:8000/docs`.

## API Endpoints

### 1. Generate a Travel Plan
- **Endpoint**: `POST /generate-plan`
- **Request**:
  ```bash
  curl -X POST http://localhost:8000/generate-plan \
  -H "Content-Type: application/json" \
  -d '{"location": "Paris", "start_date": "2025-05-01", "days": 3, "interests": {"Historical": 0.8, "Art & Culture": 0.5}, "budget": 200}'
  ```

### 2. Edit an Existing Plan
- **Endpoint**: `POST /edit-plan`
- **Request**:
  ```bash
  curl -X POST http://localhost:8000/edit-plan?plan_id=67f5b33158367d260334d4f2 \
  -H "Content-Type: application/json" \
  -d '{"location": "Paris", "start_date": "2025-05-02", "days": 2, "interests": {"Nature": 0.7, "Relaxing": 0.6}, "budget": 150}'
  ```

### 3. Search Hotels (Mock)
- **Endpoint**: `GET /hotels/search`
- **Request**:
  ```bash
  curl "http://localhost:8000/hotels/search?location=Paris&checkin=2025-05-01&checkout=2025-05-04"
  ```

### 4. Health Check
- **Endpoint**: `GET /health`
- **Request**:
  ```bash
  curl http://localhost:8000/health
  ```

## Testing
Test the endpoints using Postman, cURL, or Swagger UI (`/docs`). If you encounter errors like duplicate POIs, clear and repopulate the database:
```javascript
db.pois.drop()
```
```bash
cd backend
python tag_pois_daily.py
```
