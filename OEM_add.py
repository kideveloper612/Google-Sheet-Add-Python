import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from gspread.models import Cell


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('OEM Project-f6b584127210.json', scope)
client = gspread.authorize(creds)

sheet = client.open('dealer_list_all').sheet1
pp = pprint.PrettyPrinter()


def get_compare_list():
    result = []
    for i in Origin_Makes:
        result.append(i.lower().split(' ')[0])
    return result


def main():
    compare_list = get_compare_list()
    sheet_list = sheet.get_all_records()
    oems = []
    for i in range(len(sheet_list)):
        seller_names = sheet_list[i]['SELLER_NAME'].lower().split(' ')
        inventory = sheet_list[i]['INVENTORY_URL'].lower()
        tmp_flag = True
        empty_flag = True
        for cmp_name in compare_list:
            if cmp_name in inventory:
                oems.append(Origin_Makes[compare_list.index(cmp_name)])
                tmp_flag = False
                empty_flag = False
                break
            elif 'benz' in inventory:
                oems.append('Mercedes Benze')
                tmp_flag = False
                empty_flag = False
                break
            elif inventory[:2] == 'mb':
                oems.append('Mercedes Benze')
                tmp_flag = False
                empty_flag = False

                break
            elif 'cdjr' in inventory:
                oems.append('Chrysler Dodge Jeep Ram')
                tmp_flag = False
                empty_flag = False
                break
            elif 'cdj' in inventory:
                oems.append('Chrysler Dodge Jeep')
                tmp_flag = False
                empty_flag = False
                break
            elif 'vw' in inventory:
                oems.append('Volkswagen')
                tmp_flag = False
                empty_flag = False
                break
        if tmp_flag:
            for seller_name in seller_names:
                if seller_name in compare_list:
                    oems.append(Origin_Makes[compare_list.index(seller_name)])
                    empty_flag = False
                    break
        if empty_flag:
            oems.append('')

    cells = []
    for i, val in enumerate(oems):
        print(val)
        cells.append(Cell(row=i+2, col=15, value=val))
    sheet.update_cells(cells)


if __name__ == '__main__':
    Origin_Makes = [
        'Acura',
        'Audi',
        'BMW',
        'Buick',
        'Cadillac',
        'Chevrolet',
        'Chevy',
        'Chrysler',
        'Dodge',
        'CDJR',
        'CDJ',
        'Fiat',
        'Ford',
        'GMC',
        'Honda',
        'Hyundai',
        'Infiniti',
        'Jeep',
        'Kia',
        'Lexus',
        'Lincoln',
        'Mazda',
        'Mercedes Benz',
        'MB',
        'Benz',
        'Nissan',
        'RAM',
        'Subaru',
        'Toyota',
        'Volkswagen',
        'VW',
        'Volvo'
    ]
    main()
