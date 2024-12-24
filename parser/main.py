import pandas as pd
import logging
import argparse
from parser import init_browser, parse_page, close_browser,ParserException
from data_handler import read_data, write_data
import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Google Transparency Report parser.\n This program requires running another program geckodriver.")
    parser.add_argument('--loop', action='store_true', help='Start special loop mode')
    parser.add_argument('--start', type=int, help='Start time in Unix timestamp * 1000 (miliseconds)')
    parser.add_argument('--end', type=int, help='End time in Unix timestamp * 1000 (miliseconds)')
    parser.add_argument('--product', type=str, default='21', help='Product identifier. Default 21 is YouTube.')
    parser.add_argument('--region', type=str, default='RU', help='Region identifier')
    parser.add_argument('--step', type=int, default=60*60*24*30*1000, help='Step interval in miliseconds. Default is 30 days')
    parser.add_argument('--pause', type=int, default='30', help='Pause. Wait some seconds between fetching in loop mode')
    parser.add_argument('--filename', type=str, default='data.xlsx', help='Output filename')
    args = parser.parse_args()

    if args.loop and (args.start is None or args.end is None):
        parser.error('--loop requires --start and --end')

    return args

def fetch_data(s, product, region, start, end):
    element_html_io = parse_page(s, product, region, start, end)
    dfs = pd.read_html(element_html_io)
    df = dfs[0]  # Give first table from list of tables
    df.columns.values[0] = 'time'
    df.columns.values[1] = 'traffic'
    df.time = pd.to_datetime(df.time, format='%b %d, %Y, %I:%M:%S %p')
    return df

def main():
    args = parse_arguments()

    product = args.product
    region = args.region
    step = args.step
    file_name = './data/' + args.filename

    if args.loop:
        start = args.start
        end = args.end
    else:
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        start_date = yesterday - datetime.timedelta(days=30)
        start = int(time.mktime(start_date.timetuple())) * 1000
        end = int(time.mktime(yesterday.timetuple())) * 1000


    old_df = read_data(file_name)

    # Initialize browser
    s = init_browser()

    try:
        while start < end:
            next_start = start + step
            df = fetch_data(s, product, region, start, next_start)
            combined_df = pd.concat([old_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset='time', keep='last')
            combined_df = combined_df.sort_values(by='time')
            new_records_count = len(combined_df) - len(old_df)
            # Update file if new or itermediate results found
            if args.loop or new_records_count > 0:
                write_data(file_name, combined_df)
                old_df = combined_df
                logging.info('File updated. New records: %d', new_records_count)
            else:
                logging.info('No new records')

            if args.loop:
                logging.info('Sleeping %d seconds', args.pause)
                time.sleep(args.pause)


            start = next_start
    except ParserException as e:
        logging.error('Parsing error!')

    # Normal task exit
    close_browser(s)


if __name__ == '__main__':
    main()
