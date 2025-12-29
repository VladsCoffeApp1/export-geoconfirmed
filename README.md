# GeoConfirmed Export Cloud Function

A Google Cloud Function that exports GeoConfirmed events from BigQuery. Returns events from the last N hours as JSON.

## Features

- Query GeoConfirmed events from BigQuery
- Configurable time window via `hours` parameter
- Returns events with full details including coordinates, sources, and metadata
- Fast, on-demand queries

## Prerequisites

- **Runtime:** Python 3.12+
- **Cloud Provider:** Google Cloud Platform
- **Cloud SDK:** `gcloud` CLI installed and configured
- **Authentication:** Application Default Credentials configured

## Configuration

### Environment Variables

Set these in `project.env` or as environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PROJECT_ID` | Yes | - | GCP project ID |
| `REGION` | Yes | - | GCP region for deployment |
| `SERVICE_NAME` | Yes | - | Cloud Function name |
| `RUNTIME` | Yes | `python312` | Python runtime version |
| `TIMEOUT` | Yes | `60` | Function timeout in seconds |
| `RUNTIME_SERVICE_ACCOUNT_EMAIL` | Yes | - | Service account for function execution |
| `BQ_DATASET` | No | `geolocations` | BigQuery dataset name |
| `BQ_TABLE` | No | `geoconfirmed_events` | BigQuery table name |

### BigQuery Source

- **Project:** `soldier-tracker`
- **Dataset:** `geolocations`
- **Table:** `geoconfirmed_events`

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd export-geoconfirmed

# Install dependencies with uv
uv sync

# For development dependencies
uv sync --group dev
```

## Local Development

```bash
# Run locally (requires GCP credentials)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
cd app
python main.py
```

Or use the functions framework:

```bash
functions-framework --target=main --debug
```

Then call:
```bash
curl "http://localhost:8080/?hours=24"
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v
```

## Deployment

### Manual Deployment

```bash
gcloud functions deploy export-geoconfirmed \
  --gen2 \
  --runtime=python312 \
  --region=europe-west3 \
  --source=./app \
  --entry-point=main \
  --trigger-http \
  --memory=512MB \
  --timeout=60s \
  --service-account=container-telethon-bot@soldier-tracker.iam.gserviceaccount.com
```

### CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) for automated deployment on push to main.

## API Usage

### HTTP Request

```bash
# Get events from last 24 hours
curl "https://<function-url>?hours=24"

# Get events from last week
curl "https://<function-url>?hours=168"
```

### Response

Success:
```json
[
  {
    "id": "12345",
    "date": "2024-01-15",
    "date_created": "2024-01-15",
    "description": "Equipment spotted near...",
    "longitude": 37.123,
    "latitude": 48.456,
    "original_source": ["https://example.com/source1"],
    "geolocation": ["https://example.com/geo1"],
    "origin": "UA",
    "tweeted": true,
    "eor_tracking": null,
    "plus_code": "8GWM4WXX+XX",
    "ingested_at": "2024-01-15T10:30:00+00:00"
  }
]
```

Error:
```json
{"error": "Missing 'hours' query parameter"}
```

## Schema

Events are returned with these fields:

| Field | Type | Description |
|-------|------|-------------|
| id | STRING | Unique event ID from GeoConfirmed |
| date | STRING | Event date (YYYY-MM-DD) |
| date_created | STRING | Date event was created |
| description | STRING | Event description |
| longitude | FLOAT64 | Longitude coordinate |
| latitude | FLOAT64 | Latitude coordinate |
| original_source | ARRAY | List of source URLs |
| geolocation | ARRAY | List of geolocation URLs |
| origin | STRING | Origin/country |
| tweeted | BOOL | Whether event was tweeted |
| eor_tracking | STRING | EOR tracking ID |
| plus_code | STRING | Plus code location |
| ingested_at | STRING | When the record was ingested (ISO format) |

## Project Structure

```
export-geoconfirmed/
├── app/
│   ├── __init__.py
│   ├── main.py              # Cloud Function entry point
│   └── config.py            # Pydantic settings
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── deploy.yml
├── project.env              # Environment configuration
├── pyproject.toml           # Dependencies & tools config
└── README.md
```

## License

SPDX-License-Identifier: LicenseRef-NonCommercial-Only
