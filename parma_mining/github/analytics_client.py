# The duty of this file is to make necessary calls to Analytics API
import httpx
from dotenv import load_dotenv
from parma_mining.github.model import ResponseModel
import os
import json
import urllib.parse


class AnalyticsClient:
    load_dotenv()
    analytics_base = str(os.getenv("ANALYTICS_BASE_URL") or "")

    measurement_url = urllib.parse.urljoin(analytics_base, "/source-measurement")
    feed_raw_url = urllib.parse.urljoin(analytics_base, "/feed-raw-data")

    def send_post_request(self, data):
        api_endpoint = self.measurement_url
        headers = {
            "Content-Type": "application/json",
        }
        print(data)
        response = httpx.post(api_endpoint, json=data, headers=headers)

        if response.status_code == 201:
            return response.json().get("id")
        else:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )

    def register_measurements(self, mapping, parent_id=None, source_module_id=None):
        result = []

        for field_mapping in mapping["Mappings"]:
            measurement_data = {
                "source_module_id": source_module_id,
                "type": field_mapping["DataType"],
                "measurement_name": field_mapping["MeasurementName"],
            }

            if parent_id is not None:
                measurement_data["parent_measurement_id"] = parent_id

            measurement_data["source_measurement_id"] = self.send_post_request(
                measurement_data
            )

            # add the source measurement id to mapping
            field_mapping["source_measurement_id"] = measurement_data[
                "source_measurement_id"
            ]

            if "NestedMappings" in field_mapping:
                nested_measurements = self.register_measurements(
                    {"Mappings": field_mapping["NestedMappings"]},
                    parent_id=measurement_data["source_measurement_id"],
                    source_module_id=source_module_id,
                )[0]
                result.extend(nested_measurements)
            result.append(measurement_data)
        return result, mapping

    def feed_raw_data(self, input_data: ResponseModel):
        api_endpoint = self.feed_raw_url
        headers = {
            "Content-Type": "application/json",
        }

        organization_json = json.loads(input_data.raw_data.updated_model_dump())

        data = {
            "source_name": input_data.source_name,
            "company_id": input_data.company_id,
            "raw_data": organization_json,
        }

        response = httpx.post(api_endpoint, json=data, headers=headers)

        if response.status_code == 201:
            return response.json()
        elif response.status_code == 404:
            pass
        else:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )
