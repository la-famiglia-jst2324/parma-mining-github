class GithubNormalizationMap:
    map_json = {
        "Source": "GitHub",
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
                        "SourceField": "stargazers_count",
                        "DataType": "int",
                        "MeasurementName": "repository stargazers count",
                    },
                    {
                        "SourceField": "watchers_count",
                        "DataType": "int",
                        "MeasurementName": "repository watchers count",
                    },
                    {
                        "SourceField": "forks_count",
                        "DataType": "int",
                        "MeasurementName": "repository forks count",
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
        ],
    }

    def get_normalization_map(self):
        return self.map_json
