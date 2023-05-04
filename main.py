import yfinance as yf
import pandas as pd
import math
import csv


def fetch_data(share,start_date,end_date):

    try:
        data = pd.DataFrame()
        stock_data = yf.download(share+".NS",start=start_date,end=end_date)
        stock_data["Ticker"] = share
        data = pd.concat([data,stock_data])
        return data

    except Exception as err:
        print(f"Can't fetch data for {share}")
        print(err)


def cal_share(share_wt,closing_price,investment_amt):

    weighted_amt = investment_amt*share_wt
    share_count = weighted_amt / closing_price
    return math.floor(share_count)



if __name__=="__main__":

    #input from user
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date: (YYYY-MM-DD) ")
    investement_amt = int(input("Enter amount to invest: "))

    #read given stock list from file
    shares = pd.read_csv('Stocks.csv')

    stock_lis =  shares['Ticker']
    stock_wt = shares['Weightage']

    stock_map ={}
    for i in range(len(stock_lis)):
        stock_map[stock_lis[i]] = stock_wt[i]


    
    temp_dict = {}
    uniq_date = set()

    #fetch data for each share 
    for share in shares['Ticker']:

        #fetch data from API
        stock_data = fetch_data(share,start_date,end_date)

        tempdata = [share,stock_map[share]]

        #calculate number of share 
        for date,row in stock_data.iterrows():

            close_price = row["Close"]
            share_count = cal_share(stock_map[share],close_price,investement_amt)

            tempdata.append(share_count)
            uniq_date.add(str(date.date()))
            
        temp_dict[share] = tempdata
    

    header = ["Ticker","Weightage"]
    data = temp_dict.values()
  
    for date in uniq_date:
        header.append(date)
    
    #write data to csv
    with open('output.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)



  


    



