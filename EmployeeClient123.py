import requests
import const

def serviceTester():
    api_base_url = 'http://' + get_service_ip() + '/empdb/employee'

    print ('USING SERVICE 123...')
    print ('Will connect to: ' + api_base_url)
    
    # Test get_all_employees endpoint
    api_url = api_base_url
    print ('Calling GET on endpoint: ' + api_url)
    response = requests.get(api_url)
    print (response.json())

def get_service_ip():
    params = {'serviceName': '123'}
    response = requests.get(url=const.DNS_IP + '/lookup', params=params)
    return response.json()['url']

if __name__ == '__main__':
    serviceTester()
