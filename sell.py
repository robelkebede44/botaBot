
from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler
import telegram
import requests
import re
import datetime
import pymongo
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_client = pymongo.MongoClient("mongodb://localhost:27017/")  

mydb = db_client["Bota"]
seller_info = mydb["seller_info"]
product_info = mydb["product_info"]

file_path = None
description = None



class Sell:
    def __init__(self):
        pass

    def get_location(self,bot,update):
        lat = None
        lng = None
        try:
            #lets not use phone for seller
            #phone = update.message.contact.phone_number
            lng = update.message.location.longitude
            lat = update.message.location.latitude
        except Exception as e:
            pass

        return lat,lng

    def chat_id_exists(self,chat_id):

        try:

            db_chat_id = seller_info.find_one({"chat_id":23})["chat_id"]

            return True
        except Exception as e:
            return False

        
    def insert_user_to_database(self,bot,update):

        lat,lng = self.get_location(bot,update)
        chat_id = update.message.chat_id

        update.message.reply_text("welcome first time seller")

        update.message.reply_text("send you location ")

        location_keyboard = telegram.KeyboardButton(
                text="send_location", 
                request_location=True)

        custom_keyboard =[[ location_keyboard ]]

        reply_markup = telegram.ReplyKeyboardMarkup(
                custom_keyboard)

        bot.send_message(chat_id=chat_id,
                text="Information",
                reply_markup=reply_markup
                )



        if lat and lng is None:
            print("the bot cant get the location ")

            update.message.reply_text("cant get the location ")
            
        else:
            db_chat_id = seller_info.find_one({"chat_id":chat_id})["chat_id"]
            print("dbdbdb ",db_chat_id)
            
            if db_chat_id:
                #update
                print("UPDATE")
                old_data = {"chat_id":chat_id}
                new_data = {"$set":{"chat_id":chat_id,"lat":lat,"lng":lng}}

                print("XSXSXSXSXSX ",[lat,lng,chat_id])
                
                mycol.update_one(old_data,new_data)

            else:
                #insert
                #mycol.insert({"chat_id":chat_id,"lat":lat,"lng":lng}) 
                print("XSXSXSXSXSX ",[lat,lng,chat_id])

                update.message.reply_text("you are now registerd go to /start")
                print("INSERT")



    def start(self,bot,update):
        
        chat_id = update.message.chat_id
        import server

        #phone = None

        if self.chat_id_exists(chat_id):
            #upload a picture 

            self.upload_product2(bot,update)

            server.FLAG  = 1

            #and description
            
            #if this both thing exists insert into database
            #(chat_id,pic_url,description,timestamp)
             

        else:
            #welcome first time seller
            self.insert_user_to_database(bot,update)

            server.FLAG  = 2


            #location
            #phone
            #if this both thing exists insert into database
            #(chat_id,location,phone)
            #i have a two text filters and in two diffrint classes callback method x.get_text y.get_text 

            #start /sell command
            pass

        #insert_user_to_database(bot,update)



    def test(self,bot,update):
        update.message.reply_text(" is at est")

    def upload_product2(self,bot,update):
        
        update.message.reply_text("upload a picture of the product2")
    
        chat_id = update.message.chat_id
        time = datetime.datetime.now()
        pic = update.message.photo[0].file_id
        file_path = bot.getFile(pic)["file_path"]

        if file_path is not None:
            print("XAXAXAXAXAXAX ",file_path)
            update.message.reply_text("picture recieved")
            
            product_info.insert({"chat_id":chat_id,"pic_url":file_path,"timestamp":time})
            #uploaded with out description


    
    """
    def upload_product(self,bot,update):
        
        update.message.reply_text("upload a picture of the product")
    
        chat_id = update.message.chat_id
        time = datetime.datetime.now()
        pic = update.message.photo[0].file_id
        file_path = bot.getFile(pic)["file_path"]

        if file_path is not None:
            print("XAXAXAXAXAXAX ",file_path)
            update.message.reply_text("picture recieved")

        update.message.reply_text("write a description")
        description = update.effective_message.text 

        if description is not None:
            update.message.reply_text("description updated")
            print("XSXSXSXSXSXSXS ",[description,file_path])
         
        if description and file_path is not None:
            print("XSXSXSXSXSXSX both exists",[description,file_path])
            #product_info.insert({"chat_id":chat_id,"pic_url":file_path,"timestamp":time})
        else:
            print("CSCSSXSXSXSX ",[description,file_path])
        #sucessfully uploaded the product
        """


def main():

    updater2 = Updater('971130326:AAFwIJEdclodQcpWNZtfEOjFXS_6qg5qusc')
    dp2 = updater2.dispatcher
    sell = Sell()

    dp2.add_handler(MessageHandler(Filters.contact, sell.test_bot))  
    dp2.add_handler(MessageHandler(Filters.location, sell.test_bot))
    dp2.add_handler(MessageHandler(Filters.photo, sell.upload_picture)) 
    dp2.add_handler(CommandHandler('start',sell.start))
    dp2.add_handler(CommandHandler('test',sell.test))
    updater2.start_polling()
    updater2.idle()



