# Cafe & WiFi API

A Flask REST API for discovering and managing cafes with detailed information about amenities like WiFi, power outlets, seating, and more. Perfect for remote workers and digital nomads looking for the ideal workspace.

## Features

- 🔍 **Search cafes** by location
- 🎲 **Random cafe discovery** for spontaneous visits
- 📝 **Add new cafes** with comprehensive details
- 💰 **Update pricing** information
- 🗑️ **Remove closed cafes** (admin only)
- 📊 **JSON API** responses for easy integration

## Tech Stack

- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   # Windows
   python -m pip install -r requirements.txt
   
   # macOS/Linux
   pip3 install -r requirements.txt
   ```

## Usage

Start the development server:
```bash
python main.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### GET Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `GET /` | Welcome page with documentation | `http://127.0.0.1:5000/` |
| `GET /random` | Get a random cafe | `http://127.0.0.1:5000/random` |
| `GET /all` | Get all cafes (sorted by name) | `http://127.0.0.1:5000/all` |
| `GET /search?loc=<location>` | Search cafes by location | `http://127.0.0.1:5000/search?loc=Peckham` |

### POST Endpoints

| Endpoint | Description | Required Fields |
|----------|-------------|-----------------|
| `POST /add` | Add a new cafe | name, map_url, img_url, loc, sockets, toilet, wifi, calls, seats, coffee_price |

### PATCH Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `PATCH /update-price/<cafe_id>` | Update cafe coffee price | `new_price` (query parameter) |

### DELETE Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `DELETE /report-closed/<cafe_id>` | Remove a closed cafe | `api-key=TopSecretAPIKey` (query parameter) |

## Data Model

Each cafe includes:
- **Basic Info**: name, location, map URL, image URL
- **Amenities**: WiFi, power sockets, toilets, phone call friendly
- **Details**: seating capacity, coffee price

## Example Response

```json
{
  "cafe": {
    "id": 1,
    "name": "Science Museum Cafe",
    "location": "South Kensington",
    "map_url": "https://goo.gl/maps/...",
    "img_url": "https://example.com/image.jpg",
    "has_wifi": true,
    "has_sockets": true,
    "has_toilet": true,
    "can_take_calls": false,
    "seats": "50-100",
    "coffee_price": "£3.50"
  }
}
```

## Error Handling

- **404 Not Found**: Cafe or location not found
- **403 Forbidden**: Invalid API key for protected operations

## Security

DELETE operations require an API key (`TopSecretAPIKey`) to prevent unauthorized cafe removal.

## Documentation

Full API documentation is available via Postman: [View Documentation](https://documenter.getpostman.com/view/2568017/TVRhd9qR)
