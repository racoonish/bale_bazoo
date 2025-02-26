from balethon import Client 
from balethon.conditions import document, private ,text, video
from gradio_client import Client as C
from gradio_client import handle_file
from balethon.objects import InlineKeyboard

client_hf = C("rayesh/bale_clean")
bot = Client("1261816176:T4jSrvlJiCfdV5UzUkpywN2HFrzef1IZJs5URAkz")

user_states = {}

@bot.on_message(text)
async def answer_message(message):
    user_id = message.author.id
    print(user_states.get(user_id))
    # Check if user is in middle of a process
    if user_states.get(user_id) == None : 
        await message.reply(
            "به شهر فرنگ خوش آومدی شهر فرنگ رباتی برای ترجمه و تولید محتوای انگلیسی به فارسی است ",
            InlineKeyboard(
                [("تولید زیرنویس ", "sub")],
                [("توضیحات بیشتر ", "toturial")]
            )
        )
        user_states[user_id] = 'awaiting_choose'
        
    
@bot.on_callback_query()
async def handle_callbacks(callback_query):
    user_id = callback_query.author.id
    if user_states.get(user_id) == 'awaiting_choose':
        
        if callback_query.data == "toturial":
            await callback_query.answer("📌 راهنمای استفاده:")
            
        elif callback_query.data == "sub":
            await callback_query.answer("ویدیو خودتان را آپلود کنید")
            user_states[user_id] = 'awaiting_document'
            print(user_states.get(user_id))

@bot.on_message(video)
async def handle_document(client, message):
    user_id = message.author.id
    
    if user_states.get(user_id) == 'awaiting_document':
        print(user_states.get(user_id))            
        downloading = await message.reply("در صف پردازش...")
        
        try:
            # Download file
            #file_content = await client.download(message.document.id)
            #mime_type = message.document.mime_type.split("/")[-1]
            #file_format = mime_type.split(";")[0]
            #filename = f"downloaded_file.{file_format}"
            file = await bot.get_file(message.video.id)
            file_path = file.path
            print(f"https://tapi.bale.ai/file/bot1261816176:T4jSrvlJiCfdV5UzUkpywN2HFrzef1IZJs5URAkz/{file_path}")
            #with open(filename, "wb") as f:
            #    f.write(file_content)
            print("download completed")
            # Process video
            await downloading.edit_text("... در حال پردازش")
            result = client_hf.predict(
                url=f"https://tapi.bale.ai/file/bot1261816176:T4jSrvlJiCfdV5UzUkpywN2HFrzef1IZJs5URAkz/{file_path}",
                clip_type="auto edit",
                api_name="/main"
            )

            print("process completed")
            if result.get("video"):
                await client.send_video(
                    chat_id=message.chat.id,
                    video=result["video"],
                    caption="از شهر فرنگ برات ویدیو آوردم !!"
                )
                
            await downloading.edit_text("✅ پردازش با موفقیت انجام شد!")
            user_states[user_id] = None
            
        except Exception as e:
            await downloading.edit_text(f"❌ خطا در پردازش: {str(e)}")
            user_states[user_id] = None  # Reset state on error

bot.run()