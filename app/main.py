"""
Export GeoConfirmed events from BigQuery.

Cloud Function that queries the geoconfirmed_events table and returns
events from the last N hours.
"""

from google.cloud import bigquery
from loguru import logger as log


def parse_hours(hours_raw: str) -> int:
    """Parse and validate hours parameter."""
    try:
        hours = int(hours_raw)
        if hours < 1:
            raise ValueError("hours must be at least 1")
        if hours > 8760:  # 1 year max
            raise ValueError("hours cannot exceed 8760 (1 year)")
        return hours
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"hours must be an integer, got: {hours_raw}") from e
        raise


def fetch_geoconfirmed(hours: int) -> list[dict]:
    """
    Fetch GeoConfirmed events from BigQuery.

    Args:
        hours: Number of hours to look back

    Returns:
        List of event dictionaries
    """
    client = bigquery.Client()

    query = """
        SELECT
            id,
            CAST(date AS STRING) AS date,
            CAST(date_created AS STRING) AS date_created,
            description,
            longitude,
            latitude,
            original_source,
            geolocation,
            origin,
            tweeted,
            eor_tracking,
            plus_code,
            ingested_at
        FROM
            `soldier-tracker.geolocations.geoconfirmed_events`
        WHERE
            ingested_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @hours HOUR)
        ORDER BY
            ingested_at DESC
    """

    params = [
        bigquery.ScalarQueryParameter("hours", "INT64", hours),
    ]

    job_config = bigquery.QueryJobConfig(query_parameters=params)
    results = client.query(query, job_config=job_config).result()

    log.debug(f"Fetched {results.total_rows} GeoConfirmed events from last {hours} hours")

    # Convert to list of dicts, handling REPEATED fields
    events = []
    for row in results:
        event = dict(row)
        # Convert ingested_at to ISO string for JSON serialization
        if event.get("ingested_at"):
            event["ingested_at"] = event["ingested_at"].isoformat()
        events.append(event)

    return events


def main(request):
    """
    Cloud Function entry point.

    Query parameters:
        hours: Number of hours to look back (required, 1-8760)

    Returns:
        List of GeoConfirmed events or error response
    """
    try:
        hours_raw = request.args.get("hours")
        if not hours_raw:
            return {"error": "Missing 'hours' query parameter"}, 400

        hours = parse_hours(hours_raw)
        data = fetch_geoconfirmed(hours)

        log.info(f"Returning {len(data)} events for last {hours} hours")
        return data

    except ValueError as ve:
        log.warning(f"Validation error: {ve}")
        return {"error": str(ve)}, 400

    except Exception as e:
        log.error(f"Unhandled error: {e}")
        return {"error": "Internal server error"}, 500


if __name__ == "__main__":
    # Local testing
    class MockRequest:
        args = {"hours": "24"}

    result = main(MockRequest())
    print(f"Result: {result}")
