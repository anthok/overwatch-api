import aiohttp.connector

class NoSSLTCPConnector(aiohttp.connector.TCPConnector):
    """Aiohttp doesn't have any tools to validate SSL certificates, and we will therefore get "Network unreachable" errors if we try to use """