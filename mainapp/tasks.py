from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
from channels.layers import get_channel_layer 
import asyncio
import queue
import simplejson as json
@shared_task(bind = True)
def update_stock(self, stockpicker):
    data = {}
    available_stocks = tickers_nifty50()
   
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()

    print("STOCKPICKER FROM TASKS", stockpicker)
    # for i in stockpicker:
    #    details = get_quote_table(i)
    #    data.update({i:details})
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: json.loads(json.dumps(get_quote_table(arg1), ignore_nan=True))}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    for thread in thread_list:
        thread.join()
    while not que.empty():
        result = que.get()
        data.update(result)
    # send data to group
    print("tasks*******",data)
    channel_layer = get_channel_layer()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send("stock_track",{ 
        'type':'send_stock_update',
        'message': data,


    }))
  
    return 'Done'
     