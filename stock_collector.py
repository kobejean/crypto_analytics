from alpha_vantage.timeseries import TimeSeries
from googleapiclient.http import MediaFileUpload, HttpRequest
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import argparse
import os
import csv


def data_to_csv(filename, reader):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',', )
        for row in reader:
            writer.writerow(row)


def google_drive_auth():
    # Google Drive API authentication
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server()
            # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)


def googe_doc_upload(filename, filetype, url):
    media = MediaFileUpload('files/' + filename, mimetype=filetype)
    file_stats = os.stat(filename)
    if file_stats.size <= 5e6:
        HttpRequest(url, method='POST', body=media).execute()
    else:
        # Resumable upload
        request = HttpRequest(url, method='POST', body=media, resumable=True)
        response = None
        while response is None:
            status, response = request.next_chunk()


valid_intervals = ['1min', '5min', '15min', '60min', '1day', '1week', '1month']

# Parse command line arguments
parser = argparse.ArgumentParser(description='A tool for generating stock datasets for use in python programs')
parser.add_argument('symbol', type=str, help='Symbol for the stock who\'s data we want')
parser.add_argument('interval', type=str, help='Interval of time between open and close for the data set')
args = parser.parse_args()

if args.interval not in valid_intervals:
    raise ValueError('Invalid time interval entered')

# Create time series object for alpha vantage data
key = open('avkey.txt', 'r').read()
ts = TimeSeries(key=key, output_format='csv')

# Get data from alpha vantage
print('Getting data from Alpha Vantage...')
if args.interval in valid_intervals[:3]:
    dataset, dataset_meta = ts.get_intraday(symbol=args.symbol, interval=args.interval, outputsize='full')
elif args.interval == '1day':
    dataset, dataset_meta = ts.get_daily(symbol=args.symbol, outputsize='full')
elif args.interval == '1week':
    dataset, dataset_meta = ts.get_weekly(symbol=args.symbol)
else:
    dataset, dataset_meta = ts.get_monthly(symbol=args.symbol)

# Write data to files and upload to google drive
set_file = '{}-{}.csv'.format(args.symbol, args.interval)
print('Writing data to {}'.format(set_file))
data_to_csv(set_file, dataset)

#google_doc_upload(set1_file, 'csv', )
#google_doc_upload(set2_file, 'csv', )
#google_doc_upload(set3_file, 'csv', )

