from core import baemin
import datetime
import time

if __name__ == "__main__":

    bm = baemin.Crawler()

    a = bm.update_orders()

    print(a)

    # while True:
    #     bm.update_orders()
    #     for order_code in bm.df_dict['orders'].index:
    #         bm.get_order_details(order_code)
    #     print(datetime.datetime.now())
    #     time.sleep(600)
