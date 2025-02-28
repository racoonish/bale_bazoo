
from balethon import Client
from balethon.conditions import document, private, text, video
from balethon.objects import InlineKeyboard, ReplyKeyboard
from gradio_client import Client as C
from gradio_client import handle_file

client_hf = C("rayesh/bale_clean")
bot = Client("1261816176:T4jSrvlJiCfdV5UzUkpywN2HFrzef1IZJs5URAkz")

user_states = {}
user_parametrs_sub={}
user_parametrs_dub={}


# Define reply keyboards
home_keyboard = ReplyKeyboard(["خانه"])
#back_home_keyboard = ReplyKeyboard(["بازگشت", "خانه"])

# Handle all text messages (including navigation buttons)
@bot.on_message(text)
async def answer_message(message):
    user_id = message.author.id
    state = user_states.get(user_id)
    print("mess")

    # Handle "Home" button
    if message.text == "خانه" or  message.text =="start":
        user_states[user_id] = ['awaiting_choose']
        await message.reply(
            "به شهر فرنگ خوش آومدی شهر فرنگ رباتی برای ترجمه و تولید محتوای انگلیسی به فارسی است ",
            reply_markup=InlineKeyboard(
                [("تولید زیرنویس ", "sub")],
                [("دوبله فارسی", "dub")],
                [("توضیحات بیشتر ", "toturial")]
            )
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="برای ناوبری از کیبورد زیر استفاده کنید.",
            reply_markup=home_keyboard
        )
    
# Handle inline keyboard selections
@bot.on_callback_query()
async def handle_callbacks(callback_query):
    user_id = callback_query.author.id
    print('callback_query')
    print(user_states[user_id][0]+"1\n")
    if user_states[user_id][0] == 'awaiting_choose':
        print("again")
        if callback_query.data == "toturial":
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="📌 راهنمای استفاده: اینجا توضیحات کامل استفاده از ربات قرار می‌گیرد.",
                reply_markup=home_keyboard
            )
        elif callback_query.data == "sub":
            
            user_states[user_id][0] = "awaiting_parametrs"
            user_states[user_id].append(1)
            print(user_states[user_id][0]+"2\n")
            
            await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="لطفا یک گزینه را از کیبورد انتخاب کنید.",
            reply_markup=InlineKeyboard(
                    [(" تولید زیرنویس ", "sub_def")],
                    [("تولید زیرنویس پیشرفته", "sub_custome")]
                    ),
          #  reply_markup=home_keyboard
            )
        elif callback_query.data == "dub":
         user_states[user_id][0] = "awaiting_parametrs"
         user_states[user_id].append(2)
         await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="لطفا یک گزینه را از کیبورد انتخاب کنید.",
              reply_markup=InlineKeyboard(
                    [("دوبله سریع", "dub_def")],
                    [(" دوبله پیشرفته", "dub_custome")]
                ),
            #reply_markup=home_keyboard
            )
         #await bot.send_message(
       #         chat_id=callback_query.message.chat.id,
       #         text="لطفا ویدیو خود را برای دوبله آپلود کنید ",
       #         reply_markup=home_keyboard
        #    )
    
    #choose custome or default 
    elif user_states[user_id][0] == 'awaiting_parametrs':
        print(user_states[user_id][0]+"3\n")
        if callback_query.data == "dub_custome":
            user_states[user_id][0] = 'awaiting_send_parametrs'
            await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="لطفا یک گوینده را از کیبورد انتخاب کنید.",
            reply_markup=InlineKeyboard(
                    [("آقا", "he")],
                    [("خانم", "she")]
             )
            )
            
            
        elif callback_query.data == "sub_custome":
            if user_states[user_id][0] == 'awaiting_parametrs':
                user_states[user_id][0] = 'awaiting_send_parametrs'
                await bot.send_message(


chat_id=callback_query.message.chat.id,
                text="لطفا رنگ مورد نظر را از کیبورد انتخاب کنید.",
                reply_markup=InlineKeyboard(
                        [("سفید", "white")],
                        [("سیاه", "black")],
                        [("زرد", "yellow")]
                        )
                )
                

        elif callback_query.data == "sub_def":
             user_states[user_id][0] = 'awaiting_document'
        elif callback_query.data == "dub_def":
             user_states[user_id][0] = 'awaiting_document'
    elif user_states[user_id][0] == 'awaiting_font':
                user_states[user_id][0]= 'append_font'
                await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="لطفا فونت مورد نظر را از کیبورد انتخاب کنید.",
                reply_markup=InlineKeyboard(
                        [("ب نازنین", "nazanin")],
                        [("ب یکان", "yekan")],
                        [("آریا", "aria")]
                        )
                )
    #choose color
    elif user_states[user_id][0] == 'awaiting_send_parametrs' :
        if callback_query.data == "he":
            user_parametrs_dub[user_id]=['he']
            user_states[user_id][0]= 'awaiting_document'
        elif callback_query.data == "she":
            user_states[user_id][0]= 'awaiting_document'
            user_parametrs_dub[user_id]=['she']
        elif callback_query.data=="black":
            user_parametrs_sub[user_id]=['black']
            user_states[user_id][0] = 'awating_font'
        elif callback_query.data=="white":
            user_parametrs_sub[user_id]=['white']
            user_states[user_id][0]= 'awaiting_font'
        elif callback_query.data=="yellow":
            user_parametrs_sub[user_id]=['yellow']
            user_states[user_id][0] = 'awaiting_font'
    #choose font 
    elif user_states[user_id][0] == 'append_font': 
        if callback_query.data == "yekan":
            user_parametrs_sub[user_id].append('yekan')
        elif callback_query.data == "nazanin":
            user_parametrs_sub[user_id].append('nazanin')
        elif callback_query.data == "aria":
            user_parametrs_sub[user_id].append('aria')
        user_states[user_id][0]= 'awaiting_document'
        await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="ایا از انتخاب خود مطمین هستید ؟",
                reply_markup=InlineKeyboard(
                        [("بلی ", "confirm")],
                        )
        )
        
    elif user_states[user_id][0] == 'awaiting_document':         
        await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="لطفا ویدیو مورد نظر را آپلود کنید"
        )
# Handle video uploads
@bot.on_message(video)
async def handle_document(message):
    user_id = message.author.id
    if user_states[user_id][0] == 'awaiting_document': 
        downloading = await message.reply("در صف پردازش...")
        try:
            #mood
            file = await bot.get_file(message.video.id)
            file_path = file.path
            result = client_hf.predict(
                url=f"https://tapi.bale.ai/file/bot1261816176:T4jSrvlJiCfdV5UzUkpywN2HFrzef1IZJs5URAkz/{file_path}",
                clip_type="auto edit",
                api_name="/main"
            )
            
            await bot.send_video(
                chat_id=message.chat.id,
                video=result["video"],
                caption="از شهر فرنگ برات ویدیو آوردم !!"
            )
            await downloading.edit_text("✅ پردازش با موفقیت انجام شد!")
            user_states[user_id][0] = 'awaiting_choose'
            await bot.send_message(
                chat_id=message.chat.id,
                text="برای ادامه، یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboard(
                    [("تولید زیرنویس ", "sub")],
                    [("توضیحات بیشتر ", "toturial")]
                )
            )


await bot.send_message(
                chat_id=message.chat.id,
                text="برای ناوبری از کیبورد زیر استفاده کنید.",
                reply_markup=home_keyboard
            )
        except Exception as e:
            await downloading.edit_text(f"❌ خطا در پردازش: {str(e)}")
            user_states[user_id][0] = 'awaiting_choose'
            await bot.send_message(
                chat_id=message.chat.id,
                text="برای ادامه، یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboard(
                    [("تولید زیرنویس ", "sub")],
                    [("توضیحات بیشتر ", "toturial")]
                )
            )
            await bot.send_message(
                chat_id=message.chat.id,
                text="برای ناوبری از کیبورد زیر استفاده کنید.",
                reply_markup=home_keyboard
            )

bot.run()
