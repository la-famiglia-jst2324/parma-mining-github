"""Normalization map for github data."""


class GithubNormalizationMap:
    """Normalization map for github data."""

    map_json = {
        "Source": "github",
        "Mappings": [
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "company name",
            },
            {
                "SourceField": "description",
                "DataType": "text",
                "MeasurementName": "company description",
            },
            {"SourceField": "url", "DataType": "link", "MeasurementName": "github url"},
            {
                "SourceField": "repos",
                "DataType": "nested",
                "MeasurementName": "repositories",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "repository name",
                    },
                    {
                        "SourceField": "description",
                        "DataType": "paragraph",
                        "MeasurementName": "repository description",
                    },
                    {
                        "SourceField": "language",
                        "DataType": "text",
                        "MeasurementName": "repository primary language",
                    },
                    {
                        "SourceField": "created_at",
                        "DataType": "date",
                        "MeasurementName": "repository creation date",
                    },
                    {
                        "SourceField": "updated_at",
                        "DataType": "date",
                        "MeasurementName": "repository last updated date",
                    },
                    {
                        "SourceField": "pushed_at",
                        "DataType": "date",
                        "MeasurementName": "repository last pushed date",
                    },
                    {
                        "SourceField": "html_url",
                        "DataType": "link",
                        "MeasurementName": "repository html url",
                    },
                    {
                        "SourceField": "clone_url",
                        "DataType": "link",
                        "MeasurementName": "repository clone url",
                    },
                    {
                        "SourceField": "svn_url",
                        "DataType": "link",
                        "MeasurementName": "repository svn url",
                    },
                    {
                        "SourceField": "homepage",
                        "DataType": "link",
                        "MeasurementName": "repository homepage url",
                    },
                    {
                        "SourceField": "size",
                        "DataType": "int",
                        "MeasurementName": "repository size",
                    },
                    {
                        "SourceField": "watchers_count",
                        "DataType": "int",
                        "MeasurementName": "repository watchers count",
                    },
                    {
                        "SourceField": "open_issues_count",
                        "DataType": "int",
                        "MeasurementName": "repository open issues count",
                    },
                    {
                        "SourceField": "stars",
                        "DataType": "int",
                        "MeasurementName": "repository stars",
                    },
                    {
                        "SourceField": "forks",
                        "DataType": "int",
                        "MeasurementName": "repository forks",
                    },
                ],
            },
            {
                "SourceField": "aggregated_sum_size",
                "DataType": "int",
                "MeasurementName": "total repository size",
            },
            {
                "SourceField": "aggregated_sum_watchers_count",
                "DataType": "int",
                "MeasurementName": "total watchers count",
            },
            {
                "SourceField": "aggregated_sum_open_issues_count",
                "DataType": "int",
                "MeasurementName": "total open issues count",
            },
            {
                "SourceField": "aggregated_sum_stars",
                "DataType": "int",
                "MeasurementName": "total repository stars",
            },
            {
                "SourceField": "aggregated_sum_forks",
                "DataType": "int",
                "MeasurementName": "total repository forks",
            },
        ],
    }

    def get_normalization_map(self) -> dict:
        """Return the normalization map."""
        return self.map_json
