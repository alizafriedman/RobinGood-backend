from .routes import rd
import requests
import json

def get_charity_by_id(charity_id):
    charity = rd.get(charity_id)
    if charity:
        return charity
    else:
        req = requests.get(f'http://data.orghunter.com/v1/charityfinancial?user_key=3527271551210ee6dbcb09d5e20c8a41&ein={charity_id}')
        requ = requests.get( f'http://data.orghunter.com/v1/charitysearch?user_key=3527271551210ee6dbcb09d5e20c8a41&sein={charity_id}')
        if req.status_code == requests.codes.ok and requ.status_code == requests.codes.ok:
            charityInfo = req.json()
            charityInfos = requ.json()
            print(charityInfos)
            info = charityInfo['data']
            info_w = charityInfos['data'][0]
            print(info_w)
            charity_id = info['ein']
            name = info['name']
            city = info['city']
            state = info['state']
            zipCode = info['zipCode']
            category = info['nteeClass']
            revenue = info['totrevenue'] or 0
            functionalExpenses = info['totfuncexpns'] or 0
            fundraising = info['grsincfndrsng'] or 0
            contributions = info['totcntrbgfts'] or 0
            url = info_w['website'] or info_w['url']
            # website = info_w['website']
            donate = info_w['donationUrl']

            charity_data = {
            'ein': charity_id,
            'name': name,
            'city': city,
            'state': state,
            'zip_code': zipCode,
            'category': category,
            'chart_data':[
                {'x':'Total Revenue', 'y':int(revenue)},
                {'x': 'Total Functional Expenses',
                    'y': int(functionalExpenses)},
                {'x': 'Gross Fundraising', 'y': int(fundraising)},
                {'x': 'Total Contributions', 'y':int(contributions)}
            ],
            'total_revenue': int(revenue),
            'total_functional_expenses': int(functionalExpenses),
            'gross_fundraising': int(fundraising),
            'total_contributions': int(contributions),
            'website': url,
            'donate_link': donate
            },

            charity_string = json.dumps(charity_data)
            rd.set(charity_id, charity_string)
            test = rd.get(charity_id)
            print(test)

            return test
