import aiohttp
import asyncio
async def get_webhook_urls_by_event(evento):
    endpoint_url = "http://localhost:4000/"
    query = f"""
    query GetWebhookUrlsByEvent {{
        getWebhookUrlsByEvent(evento: "{evento}")
    }}
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint_url, json={"query": query}, timeout=20) as response:
                if response.status == 200:
                    data = await response.json()
                    urls = data.get("data", {}).get("getWebhookUrlsByEvent", [])
                    return urls

                print(f"Error al realizar la consulta: {await response.text()}")

    except aiohttp.ClientTimeout as e:
        print(f"Error: La solicitud ha superado el tiempo de espera. Detalles: {e}")

    except aiohttp.ClientError as e:
        print(f"Error durante la solicitud: {e}")

    return []

async def post_data_to_webhooks(webhook_urls, post_data):
    async with aiohttp.ClientSession() as session:
        tasks = [post_to_webhook(session, url, post_data) for url in webhook_urls]
        await asyncio.gather(*tasks)

async def post_to_webhook(session, url, post_data):
    try:
        async with session.post(url, json=post_data, timeout=20) as response:
            if response.status == 200:
                print(f"POST a {url} exitoso")
            else:
                print(f"Fallo en el POST a {url}. Código de estado: {response.status}")

    except aiohttp.ClientTimeout as e:
        print(f"Error: La solicitud a {url} ha superado el tiempo de espera. Detalles: {e}")

    except aiohttp.ClientError as e:
        print(f"Error durante el POST a {url}: {e}")

async def response_to_url(evento, data):
    urls = await get_webhook_urls_by_event(evento)

    if urls:
        print("URL en el webhook:")
        print(urls)
        await post_data_to_webhooks(urls, data)
    else:
        print("No se obtuvieron URLs en el webhook.")

