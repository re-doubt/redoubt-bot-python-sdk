import os
import requests
from .alert import Alert
from .utils import get_redoubt_config


def get_alerts(dict):
    alerts_api_url = get_alerts_api_url()
    headers = get_alerts_api_headers()
    query_options = AlertQueryOptions(dict)
    payload = query_options.get_query()

    response = requests.request(
        "POST", alerts_api_url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json().get('data')
        if data:
            return AlertsResponse(data.get('alerts'))
    else:
        message = response.text
        raise Exception(message)


def get_alerts_api_url():
    if 'REDOUBT_PUBLIC_API_PROXY_HOST' in os.environ:
        return f'http://{os.environ["REDOUBT_PUBLIC_API_PROXY_HOST"]}' f'{":"+os.environ["REDOUBT_PUBLIC_API_PROXY_PORT"] if "REDOUBT_PUBLIC_API_PROXY_PORT" in os.environ else ""}/graphql'

    config = get_redoubt_config()
    if "alertsApiUrl" not in config:
        return "https://graphql.redoubt.online/v1/graphql"
    return config.get("alertsApiUrl")


def get_alerts_api_headers():
    headers = {"content-type": "application/json"}

    config = get_redoubt_config()
    if "redoubtApiKey" in config:
        headers["Authorization"] = f'Bearer {config.get("redoubtApiKey")}'

    return headers


class AlertCursor:
    def __init__(self, dict):
        self.alert_id = dict.get('alertId')
        self.block_number = dict.get('blockNumber')


class AlertQueryOptions:
    def __init__(self, dict):
        self.bots = dict.get('bot_ids')
        self.addresses = dict.get('addresses')
        self.alertHash = dict.get('alert_hash')
        self.alertId = dict.get('alert_id')
        self.alertIds = dict.get('alert_ids')
        self.chainId = dict.get('chain_id')
        self.createdSince = dict.get('created_since')
        self.createdBefore = dict.get('created_before')
        self.first = dict.get('first')
        self.after = dict.get('starting_cursor')
        self.projectId = dict.get('project_id')
        self.scanNodeConfirmations = dict.get('scan_node_confirmations')
        self.severities = dict.get('severities')
        self.transactionHash = dict.get('transaction_hash')
        self.blockSortDirection = dict.get('block_sort_direction')
        self.blockDateRange = dict.get('block_date_range')
        self.blockNumberRange = dict.get('block_number_range')

    def get_query(self):
        query = """
          query($input: AlertsInput) {
            alerts(input: $input) {
                alerts {
                    alertId
                    addresses
                    contracts {
                        address
                        name
                        projectId
                    }
                    createdAt
                    description
                    hash
                    metadata
                    name
                    projects {
                        id
                    }
                    protocol
                    scanNodeCount
                    severity
                    source {
                        transactionHash
                        bot {
                            chainIds
                            createdAt
                            description
                            developer
                            docReference
                            enabled
                            id
                            image
                            name
                            reference
                            repository
                            projects
                            scanNodes
                            version
                        }
                        block {
                            number
                            hash
                            timestamp
                            chainId
                        }
                        sourceAlert {
                            hash
                            botId
                            timestamp
                            chainId
                        }
                    }
                    alertDocumentType
                    findingType
                    relatedAlerts
                    chainId
                    labels {
                        label
                        confidence
                        entity
                        entityType
                        remove
                        metadata
                    }
                    addressBloomFilter {
                        bitset
                        k
                        m
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor {
                        blockNumber
                        alertId
                    }
                }
            }
          }
          """
        query_variables = vars(self)
        filtered_query_variables = {
            k: v for k, v in query_variables.items() if v is not None}
        return dict(query=query, variables={"input": filtered_query_variables})


class AlertsResponse:
    def __init__(self, dict):
        self.alerts = list(map(lambda t: Alert(t), dict.get(
            'alerts', []))) if dict.get('alerts') is not None else []
        self.page_info = PageInfo(dict.get('pageInfo')) if dict.get(
            'pageInfo') is not None else None


class PageInfo:
    def __init__(self, dict):
        self.has_next_page = dict.get('hasNextPage')
        self.end_cursor = AlertCursor(dict.get('endCursor')) if dict.get(
            'endCursor') is not None else None
