from datetime import datetime, timedelta
import logging
import argparse
import aiohttp
import asyncio
import platform


if platform.system() == 'Windows': # Setting a loop policy to avoid RuntimeError: Event loop is closed
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Parser settings
parser = argparse.ArgumentParser(description='Console application for viewing exchange rates') 
parser.add_argument('days', type=int, help='Number of days for which statistics are collected')
parser.add_argument('currencies', nargs='+', help='Currencies list for processing')
args = parser.parse_args()


# Request on PB Api
async def request(session, url: str):
    try:
        async with session.get(url, ssl=False) as resp:
            if resp.status == 200:
                result = await resp.json()
                return result
            logging.error(f"Error status: {resp.status} for {url}")
            return None
    except aiohttp.ClientConnectorError as err:
        logging.error(f"Connection error: {str(err)}")
        return None


# Create a pool of requests to obtain data for certain days
async def create_request_pool(days):
    url_pool = []
    base_url = 'https://api.privatbank.ua/p24api/exchange_rates?date='
    for iterator in range(days):
        date = (datetime.now() - timedelta(days=iterator)).strftime("%d.%m.%Y")
        url_for_pool = f'{base_url}{date}'
        url_pool.append(url_for_pool)
    return url_pool


# Proccess all requests from pool and generate results from API
async def process_requests(session, urls, currencies):
    results = [] 
    for url in urls:
        date_str = url.split('=')[-1]  
        response = await request(session, url)
        if response:
            daily_data = {date_str: {}}
            for currency in currencies:
                exc = next((item for item in response['exchangeRate'] if item["currency"] == currency), None)
                if exc:
                    daily_data[date_str][currency] = {
                        'sale': exc.get('saleRate', exc.get('saleRateNB', 'N/A')),
                        'purchase': exc.get('purchaseRate', exc.get('purchaseRateNB', 'N/A'))
                    }
            results.append(daily_data) 
        else:
            print(f"Failed to retrieve data for {date_str}")
    return results


# Enter point
async def get_exchange_for_days(days: int, currencies: list):
    async with aiohttp.ClientSession() as session:
        urls = await create_request_pool(days)
        results = await process_requests(session, urls, currencies)
        print(results)

async def main():
    days = args.days
    currencies = args.currencies
    if days > 10:
        print("Error. The maximum number of days for which statistics can be collected is 10")
        return
    print(f"Statistics for the last {args.days} days")
    print(f"Currencies: {', '.join(currency for currency in args.currencies)}")
    await get_exchange_for_days(days, currencies)

if __name__ == '__main__':
    asyncio.run(main())
