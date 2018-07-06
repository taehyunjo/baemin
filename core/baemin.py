import requests
import json
import datetime
import time
import pandas as pd
import config
from core import db

class Crawler():

    datetime_now = datetime.datetime.now()
    today_date = str(datetime_now.year) + "-" \
                 + str('%02d' % datetime_now.month) + "-" \
                 + str('%02d' % datetime_now.day)

    # folder_path = config.LOCAL_CONFIG['path'] + today_date

    df_dict = {}


    def __init__(self):
        self.session = self.get_Session() #session
        self.login(config.IDPW['ID'],config.IDPW['PW']) #login
        self.load_data()
        self.db_engine = db.db_machine()

    def get_Session(self):
        session = requests.Session()
        return session

    def login(self, id, pw):
        login_url = "https://sso-ceo.baemin.com/web/login?returnUrl=https%3A%2F%2Fceo.baemin.com%2F"
        login_params = {'id': id, "password": pw, "redirectUrl": "https://ceo.baemin.com/"}
        self.session.post(login_url, login_params) #login
        return None

    def get_orders_by_page(self, pageNo):
        orders_url = "https://ceo.baemin.com/v1/orders"

        # datetime_now = datetime.datetime.now()
        #
        # # today_date = '2018-06-24' # for testing
        #
        # today_date = str(datetime_now.year) + "-" \
        #              + str('%02d' % datetime_now.month) + "-" \
        #              + str('%02d' % datetime_now.day)

        orders_params = {"shopNo" : "all", # We can set shopNo in details, but it would be better to set it "all"
                           "pageNo" : str(pageNo+1) , # Loop until there is no more order.
                           "from" : "2018-06-24",#self.today_date ,
                           "to" : "2018-06-24",#self.today_date ,
                           "ordProgCd" : 2, # 1: In progress, 2: Done
                           "purchPstnCd" : "", # "" means all kinds of purchase types.
                           "ts" : str(int(time.time() * 1000))} #timestamp, I don't know why it is needed. I need to check the reason why it is needed.

        r_orders = self.session.get(orders_url, params=orders_params)  # get orders management page
        tmp_orders_text = r_orders.text
        # tmp_orders_dict = json.loads(tmp_orders_text)
        try:
            tmp_orders_dict = json.loads(tmp_orders_text)
        except JSONDecodeError:
            print("JSONDecodeError! => CONTEXT : " + tmp_orders_text)
            return pd.DataFrame()

        temp_df = pd.DataFrame(tmp_orders_dict['data']['orders'])
        if len(temp_df) != 0:
            temp_df.set_index('orderNo', inplace=True)
            return temp_df
        else:
            return pd.DataFrame()

            # if len(tmp_orders_dict['data']['orders']) != 0:
            #     temp_df = pd.DataFrame(tmp_orders_dict['data']['orders'])
            #     try:
            #         temp_orders_df
            #     except UnboundLocalError:
            #         temp_orders_df = temp_df
            #     else:
            #         temp_orders_df = pd.concat([temp_orders_df, temp_df])
            #     pageNo = pageNo + 1
            #     time.sleep(1)
            # else:
            #     break

    def update_orders(self):
        pageNo = 0
        check_idx = 0
        check_boolean = False

        while True:
            df_temp_orders = self.get_orders_by_page(pageNo)

            if len(df_temp_orders) == 0:
                check_boolean = True

            for i, idx in enumerate(df_temp_orders.index):
                if idx not in self.df_dict['orders'].index:
                    check_idx = check_idx + 1
                else:
                    check_boolean = True

            try:
                df_all_temp_orders
            except UnboundLocalError:
                df_all_temp_orders = df_temp_orders
            else:
                df_all_temp_orders = pd.concat([df_all_temp_orders, df_temp_orders])

            if check_boolean:
                self.df_dict['orders'] = pd.concat([df_all_temp_orders.iloc[:check_idx], self.df_dict['orders']])
                self.df_dict['orders'] = self.df_dict['orders'].sort_values(by='orderDate')
                #self.df_dict['orders'].to_csv(self.folder_path + '/orders.csv', encoding='cp949')
                return self.df_dict['orders'] #break
            else:
                pageNo = pageNo + 1
                time.sleep(3.5) # hope to be seemed like human, but machine.

    def get_order_details(self, order_code):
        order_details_url = 'https://ceo.baemin.com/v1/orders/' + order_code
        order_details_params = {'orderDt' : self.today_date,
                                'ts' : str(int(time.time() * 1000))}

        r_order_details = self.session.get(order_details_url, params = order_details_params)
        tmp_order_details_text = r_order_details.text
        # tmp_order_details_dict = json.loads(tmp_order_details_text)


        try:
            tmp_order_details_dict = json.loads(tmp_order_details_text)
        except JSONDecodeError:
            print("JSONDecodeError! => CONTEXT : " + tmp_order_details_text)
            return

        tmp_list = []
        for key in tmp_order_details_dict['data'].keys():
            tmp_list.append(pd.DataFrame(tmp_order_details_dict['data'][key]))

        df_name_list = ['order_details', 'purch_details', 'food_details']
        for i in range(len(tmp_list)):
            tmp_list[i].index = [order_code for i in range(len(tmp_list[i].index))]
            if order_code not in self.df_dict[df_name_list[i]].index:
                self.df_dict[df_name_list[i]] = pd.concat([tmp_list[i], self.df_dict[df_name_list[i]]])
                self.df_dict[df_name_list[i]].to_csv(self.folder_path + '/' + df_name_list[i] + '.csv', encoding = 'cp949')

    def set_order_details_2_db(self):
        """when familiar with db system, I'll write these codes"""
        pass

    def set_orders_2_db(self):
        """when familiar with db system, I'll write these codes"""
        pass

