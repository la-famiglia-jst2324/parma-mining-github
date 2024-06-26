"""This module contains the AnalyticsClient class.

AnalyticsClient class is used to send data to the analytics service.
"""
import json
import logging
import os
import urllib.parse

import httpx
from dotenv import load_dotenv

from parma_mining.github.model import ResponseModel
from parma_mining.mining_common.const import HTTP_200, HTTP_201
from parma_mining.mining_common.exceptions import AnalyticsError

logger = logging.getLogger(__name__)


class AnalyticsClient:
    """AnalyticsClient class is used to send data to the analytics service."""

    load_dotenv()
    analytics_base = str(os.getenv("ANALYTICS_BASE_URL") or "")

    measurement_url = urllib.parse.urljoin(analytics_base, "/source-measurement")
    feed_raw_url = urllib.parse.urljoin(analytics_base, "/feed-raw-data")
    crawling_finished_url = urllib.parse.urljoin(analytics_base, "/crawling-finished")

    def send_post_request(self, token: str, api_endpoint, data):
        """Send a POST request to the given API endpoint with the given data."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response = httpx.post(api_endpoint, json=data, headers=headers, timeout=120)

        if response.status_code in [HTTP_200, HTTP_201]:
            return response.json()
        else:
            logger.error(
                f"API request failed with status code {response.status_code},"
                f"response: {response.text}"
            )
            raise AnalyticsError(
                f"API request failed with status code {response.status_code},"
                f"response: {response.text}"
            )

    def register_measurements(
        self, token: str, mapping, parent_id=None, source_module_id=None
    ):
        """Register the given mapping as a measurement."""
        result = []

        for field_mapping in mapping["Mappings"]:
            measurement_data = {
                "source_module_id": source_module_id,
                "type": field_mapping["DataType"],
                "measurement_name": field_mapping["MeasurementName"],
            }

            if parent_id is not None:
                measurement_data["parent_measurement_id"] = parent_id
            else:
                logger.debug(
                    f"No parent id provided for "
                    f"measurement {measurement_data['measurement_name']}"
                )

            response = self.send_post_request(
                token, self.measurement_url, measurement_data
            )
            measurement_data["source_measurement_id"] = response.get("id")

            # add the source measurement id to mapping
            field_mapping["source_measurement_id"] = measurement_data[
                "source_measurement_id"
            ]

            if "NestedMappings" in field_mapping:
                nested_measurements = self.register_measurements(
                    token,
                    {"Mappings": field_mapping["NestedMappings"]},
                    parent_id=measurement_data["source_measurement_id"],
                    source_module_id=source_module_id,
                )[0]
                result.extend(nested_measurements)
            result.append(measurement_data)
        return result, mapping

    def feed_raw_data(self, token: str, input_data: ResponseModel):
        """Feed the raw data to the analytics service."""
        organization_json = json.loads(input_data.raw_data.updated_model_dump())

        data = {
            "source_name": input_data.source_name,
            "company_id": input_data.company_id,
            "raw_data": organization_json,
        }

        return self.send_post_request(token, self.feed_raw_url, data)

    def crawling_finished(self, token, data):
        """Notify crawling is finished to the analytics."""
        return self.send_post_request(token, self.crawling_finished_url, data)
