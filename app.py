Seyed Mamareza, [28.02.25 19:32]
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

Seyed Mamareza, [28.02.25 19:32]
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
