while('true'):
	while(refresh()):
		time.sleep(0.3)
	if (float(bnc_dict['buy1_price'])/float(otc_dict['sell1_price']))>1.003:
		minium_quntity=100.0
		available_quntity=[float(bnc_dict['buy1_quntity']),float(bnc_dict['eth_balance']),float(otc_dict['sell1_quntity']),(float(otc_dict['usdt_balance'])/float(otc_dict['sell1_price']))]
		for i in available_quntity:
			if(i<minium_quntity):
				minium_quntity=i
		minium_quntity=minium_quntity-0.00001
		if(minium_quntity>0.03):
			client.order_limit_sell(symbol='ETHUSDT',quantity="%.5f" %minium_quntity,price=str(bnc_dict['buy1_price']))
			otc_order('ethusdt','buy',str("%.5f" %minium_quntity),str(otc_dict['sell1_price']))
			BUY=float(otc_dict['sell1_price'])
			SELL=float(bnc_dict['buy1_price'])
			QUANTITY="%.5f" %minium_quntity
			print('BUY_PRICE:'+`BUY`+'  SELL_PRICE:'+`SELL`+'  QUNTITY:'+`QUANTITY`+'  STATE1')
		#--------------------------------------------------------------------------檢測有沒有交易成功---------------------------------------------------------------------
			time.sleep(1)
			while(refresh()):
				time.sleep(0.3)
			if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':#交易成功
				with open("Trade_view.csv","a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'BUY:',BUY,'SELL:',SELL,'QUANTITY:',QUANTITY,'STATE1'])
			elif bnc_dict['order_now'][0]['buyorsell']=='SELL'and otc_dict['order_now'][0]['buyorsell']=='NULL':#幣安沒賣完
				time.sleep(4)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL':
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'BUY:',BUY,'SELL:',SELL,'QUANTITY:',QUANTITY,'STATE1'])
				else:
					client.cancel_order(symbol='ETHUSDT',orderId=bnc_dict['order_now'][0]['id'])
					client.order_market_sell(symbol='ETHUSDT',quantity="%.5f" %float(bnc_dict['order_now'][0]['quntity']))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				time.sleep(1)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':
					pass
				else:
					while('true'):#系統中斷
						time.sleep(10)
			elif bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='buy':#OTC買不夠
				time.sleep(4)
				while(refresh()):
					time.sleep(0.3)
				if otc_dict['order_now'][0]['buyorsell']=='NULL':
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'BUY:',BUY,'SELL:',SELL,'QUANTITY:',QUANTITY,'STATE1'])
				else:
					otc_cancel_order(str(otc_dict['order_now'][0]['id']))
					client.order_market_buy(symbol='ETHUSDT',quantity="%.5f" %float(otc_dict['order_now'][0]['quntity']))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				time.sleep(1)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':
					pass
				else:
					while('true'):#系統中斷
						time.sleep(10)
			elif bnc_dict['order_now'][0]['buyorsell']=='SELL'and otc_dict['order_now'][0]['buyorsell']=='buy':#兩邊都沒成功
				client.cancel_order(symbol='ETHUSDT',orderId=bnc_dict['order_now'][0]['id'])
				otc_cancel_order(str(otc_dict['order_now'][0]['id']))
				if(float(bnc_dict['order_now'][0][quntity])>float(otc_dict['order_now'][0][quntity])):
					client.order_market_sell(symbol='ETHUSDT',quantity="%.5f" %(float(bnc_dict['order_now'][0]['quntity'])-float(otc_dict['order_now'][0]['quntity'])))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				else:
					client.order_market_buy(symbol='ETHUSDT',quantity="%.5f" %(float(otc_dict['order_now'][0]['quntity'])-float(bnc_dict['order_now'][0]['quntity'])))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				time.sleep(1)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':
					pass
				else:
					while('true'):#系統中斷
						time.sleep(10)
		else:
			print('QUNTITY NOT ENOUGH   BUY_PRICE:'+`float(otc_dict['sell1_price'])`+'  SELL_PRICE:'+`float(bnc_dict['buy1_price'])`+'  QUNTITY:'+`float(minium_quntity)+0.00001`+'  STATE1')
	elif (float(otc_dict['buy1_price'])/float(bnc_dict['sell1_price']))>1.003:
		minium_quntity=100.0
		available_quntity=[float(bnc_dict['sell1_quntity']),(float(bnc_dict['usdt_balance'])/float(bnc_dict['sell1_price'])),float(otc_dict['buy1_quntity']),float(otc_dict['eth_balance'])]
		for i in available_quntity:
			if(i<minium_quntity):
				minium_quntity=i
		minium_quntity=minium_quntity-0.00001
		if(minium_quntity>0.03):
			client.order_limit_buy(symbol='ETHUSDT',quantity="%.5f" %minium_quntity,price=str(bnc_dict['sell1_price']))
			otc_order('ethusdt','sell',str("%.5f" %minium_quntity),str(otc_dict['buy1_price']))
			print('BUY_PRICE:'+`float(bnc_dict['sell1_price'])`+'  SELL_PRICE:'+`float(otc_dict['buy1_price'])`+'  QUNTITY:'+`"%.5f" %minium_quntity`+'  STATE2')
			BUY=float(bnc_dict['sell1_price'])
			SELL=float(otc_dict['buy1_price'])
			QUANTITY="%.5f" %minium_quntity
		#--------------------------------------------------------------------------檢測有沒有交易成功---------------------------------------------------------------------
			time.sleep(1)
			while(refresh()):
				time.sleep(0.3)
			if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':#交易成功
				with open("Trade_view.csv","a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'BUY:',BUY,'SELL:',SELL,'QUANTITY:',QUANTITY,'STATE2'])
			elif bnc_dict['order_now'][0]['buyorsell']=='BUY'and otc_dict['order_now'][0]['buyorsell']=='NULL':#幣安買不夠
				time.sleep(4)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL':
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'BUY:',BUY,'SELL:',SELL,'QUANTITY:',QUANTITY,'STATE2'])
				else:
					client.cancel_order(symbol='ETHUSDT',orderId=bnc_dict['order_now'][0]['id'])
					client.order_market_buy(symbol='ETHUSDT',quantity="%.5f" %float(bnc_dict['order_now'][0]['quntity']))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				time.sleep(1)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':
					pass
				else:
					while('true'):#系統中斷
						time.sleep(10)
			elif bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='sell':#OTC賣不完
				time.sleep(4)
				while(refresh()):
					time.sleep(0.3)
				if otc_dict['order_now'][0]['buyorsell']=='NULL':
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'BUY:',BUY,'SELL:',SELL,'QUANTITY:',QUANTITY,'STATE2'])
				else:
					otc_cancel_order(str(otc_dict['order_now'][0]['id']))
					client.order_market_sell(symbol='ETHUSDT',quantity="%.5f" %float(otc_dict['order_now'][0]['quntity']))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				time.sleep(1)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':
					pass
				else:
					while('true'):#系統中斷
						time.sleep(10)
			elif bnc_dict['order_now'][0]['buyorsell']=='BUY'and otc_dict['order_now'][0]['buyorsell']=='sell':#兩邊都沒成功
				client.cancel_order(symbol='ETHUSDT',orderId=bnc_dict['order_now'][0]['id'])
				otc_cancel_order(str(otc_dict['order_now'][0]['id']))
				if(float(bnc_dict['order_now'][0][quntity])>float(otc_dict['order_now'][0][quntity])):
					client.order_market_buy(symbol='ETHUSDT',quantity="%.5f" %(float(bnc_dict['order_now'][0]['quntity'])-float(otc_dict['order_now'][0]['quntity'])))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				else:
					client.order_market_sell(symbol='ETHUSDT',quantity="%.5f" %(float(otc_dict['order_now'][0]['quntity'])-float(bnc_dict['order_now'][0]['quntity'])))
					with open("Trade_view.csv","a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow([time.strftime(DATEFORMAT,time.localtime()),time.strftime(TIMEFORMAT,time.localtime()),'Fail'])
				time.sleep(1)
				while(refresh()):
					time.sleep(0.3)
				if bnc_dict['order_now'][0]['buyorsell']=='NULL' and otc_dict['order_now'][0]['buyorsell']=='NULL':
					pass
				else:
					while('true'):#系統中斷
						time.sleep(10)
		else:
			print('QUNTITY NOT ENOUGH   BUY_PRICE:'+`float(bnc_dict['sell1_price'])`+'  SELL_PRICE:'+`float(otc_dict['buy1_price'])`+'  QUNTITY:'+`float(minium_quntity)+0.00001`+'  STATE2')
	else:
		print('BNC_BUY:'+`float(bnc_dict['buy1_price'])`+'  OTC_SELL:'+`float(otc_dict['sell1_price'])`+'  OTC_BUY:'+`float(otc_dict['buy1_price'])`+'  BNC_SELL:'+`float(bnc_dict['sell1_price'])`)
	time.sleep(0.3)