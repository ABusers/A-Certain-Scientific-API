import requests as r

base_url = 'https://api-funimation.dadcdigital.com/xml/'
'''
All sub urls will not have a preceding slash
'''
menus = 'mobile/menu/?territory=US'


headers = {'userName': 'none',
           'userType': 'FunimationSubscriptionUser',
           'userRole': 'All-AccessPass',
           'userAge': '18', 'userId': '0',
           'Authorization': '12345'}