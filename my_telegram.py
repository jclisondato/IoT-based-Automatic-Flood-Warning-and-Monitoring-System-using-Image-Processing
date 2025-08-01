import requests
import main

api_token = '6127325854:AAGsCeqD6SZApUMGU5yWHmMpwX0Y7TNLRpY'
chat_id = '-1001926809085'

image_path = 'picture.jpg'
caption = 'This is the caption for the picture.'
print()


url = f'https://api.telegram.org/bot{api_token}/sendPhoto'
files = {'photo': open(image_path, 'rb')}
data = {'chat_id': chat_id, 'caption': caption}
response = requests.post(url, files=files, data=data)

# Check the response statu  s
if response.status_code == 200:
    print('Picture sent successfully.')
else:
    print('Failed to send the picture. Response:', response.text)