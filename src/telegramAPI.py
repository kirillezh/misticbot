from src.locales import localisation
class telegramAPI:
    def __init__(self, bot):
        self.bot=bot

    async def sendPhotobyID(self, toСhat: int, photoId: str, caption: str = "", messageId: str = None, lang: str = 'ua', end: str ="def"):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        if messageId is None:
            return await self.bot.send_photo(
                chat_id=toСhat, 
                photo=photoId, 
                caption=f"{caption} {end}", 
                parse_mode="HTML")
        else:
            return await self.bot.send_photo(
                chat_id=toСhat, 
                photo=photoId, 
                caption=f"{caption} {end}", 
                parse_mode="HTML",
                reply_to_message_id=messageId)

    async def sendPhoto(self, toСhat: int, photoId: str, caption: str = "", messageId: str = None, lang: str = 'ua', end: str ="def"):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        if messageId is None:
            return await self.bot.send_photo(
                chat_id=toСhat, 
                photo=open(photoId, 'rb'), 
                caption=f"{caption} {end}", 
                parse_mode="HTML")
        else:
            return await self.bot.send_photo(
                chat_id=toСhat, 
                photo=open(photoId, 'rb'), 
                caption=f"{caption} {end}", 
                parse_mode="HTML",
                reply_to_message_id=messageId)

    async def uploadPhoto(self, toСhat: int, photoId: str, caption: str = "", messageId: str = None, lang: str = 'ua', end: str ="def"):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        if messageId is None:
            return await self.bot.send_photo(
                chat_id=toСhat, 
                photo=photoId, 
                caption=f"{caption} {end}", 
                parse_mode="HTML")
        else:
            return await self.bot.send_photo(
                chat_id=toСhat, 
                photo=photoId, 
                caption=f"{caption} {end}", 
                parse_mode="HTML",
                reply_to_message_id=messageId)
    
    async def sendVideoURL(self, toСhat: int, videoURL: str, messageId: int,caption: str = "", lang: str = 'ua', end: str ="def", disableNotification: bool = True):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        if messageId is None:
            await self.bot.send_video(
                    chat_id=toСhat, 
                    video=videoURL, 
                    caption=caption+end,
                    parse_mode="HTML",
                    disable_notification = disableNotification)
        else:
            await self.bot.send_video(
                    chat_id=toСhat, 
                    video=videoURL, 
                    reply_to_message_id=messageId, 
                    caption=caption+end,
                    parse_mode="HTML",
                    disable_notification = disableNotification)

    
    async def replyWithButtons(self, message, text: str, keyboard, lang: str = 'ua', end: str ="def", disableURL: bool = True, reply: bool = True):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        await self.sendReaction(message.chat.id, 'typing')
        return await self.bot.send_message( 
            message.chat.id, 
            f"{text}{end}",
            parse_mode="HTML", 
            disable_web_page_preview=disableURL,
            reply_to_message_id=(None,message.message_id)[reply], 
            reply_markup=keyboard)
    async def editTextWithButtons(self, message, text: str, keyboard, end: str = "def", lang: str = 'ua', disableURL: bool = True):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        return await message.edit_text(
            text,
            parse_mode="HTML", 
            disable_web_page_preview=disableURL,
            reply_markup=keyboard)
    async def reply(self, message, text: str, lang: str = 'ua', end: str ="def", disableURL: bool = True):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        await self.sendReaction(message.chat.id, 'typing')
        return await self.bot.send_message( 
            message.chat.id, 
            f"{text}{end}",
            parse_mode="HTML", 
            disable_web_page_preview=disableURL,
            reply_to_message_id=message.message_id)

    async def sendMessage(self, chatId, text: str, lang: str = 'ua', end: str ="def", disableURL: bool = True):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        return await self.bot.send_message( 
            chatId, 
            f"{text}{end}",
            parse_mode="HTML", 
            disable_web_page_preview=disableURL)

    async def editText(self, message, text: str, end: str = "def", lang: str = 'ua', disableURL: bool = True):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        return await message.edit_text(
            f"{text}{end}",
            parse_mode="HTML", 
            disable_web_page_preview=disableURL)
    async def editVideo(self, message, videoId: str, text: str, end: str = "def", lang: str = 'ua'):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        from aiogram import types
        print(videoId)
        return await self.bot.edit_message_media(
        media = types.InputMediaVideo(
            media=videoId,
            caption = f"{text}{end}",
            parse_mode="HTML"),
        chat_id = message.chat.id,
        message_id = message.message_id
        )
    async def editVideoFile(self, message, destVideo: str,w:str, h:str, text: str, end: str = "def", lang: str = 'ua'):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        from aiogram import types
        return await self.bot.edit_message_media(
        media = types.InputMediaVideo(open(destVideo, 'rb'),
            caption = f"{text}{end}",
            parse_mode="HTML",
            width=w,
            height=h),
        chat_id = message.chat.id,
        message_id = message.message_id
        )
    async def editPhotobyID(self, message, photoId: str, text: str, end: str = "def", lang: str = 'ua'):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        from aiogram import types
        return await self.bot.edit_message_media(
        media = types.InputMediaPhoto(photoId,
            caption = f"{text}{end}",
            parse_mode="HTML"),
        chat_id = message.chat.id,
        message_id = message.message_id
        )   
    async def editPhotobyMessageID(self, messageid, chatid, photoId: str, text: str, end: str = "def", lang: str = 'ua'):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        from aiogram import types
        return await self.bot.edit_message_media(
        media = types.InputMediaPhoto(open(photoId, 'rb'),
            caption = f"{text}{end}",
            parse_mode="HTML"),
        chat_id = chatid,
        message_id = messageid
        )  
    async def editPhoto(self, message, photoId: str, text: str, end: str = "def", lang: str = 'ua'):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        from aiogram import types
        return await self.bot.edit_message_media(
        media = types.InputMediaPhoto(open(photoId, 'rb'),
            caption = f"{text}{end}",
            parse_mode="HTML"),
        chat_id = message.chat.id,
        message_id = message.message_id
        )   
    async def editPhotoByIds(self, groupID: int, messageID: int, photoId: str, text: str, end: str = "def", lang: str = 'ua'):
        if(end == "def"):
             end = " \n"+localisation[lang]['end']
        from aiogram import types
        return await self.bot.edit_message_media(
        media = types.InputMediaPhoto(open(photoId, 'rb'),
            caption = f"{text}{end}",
            parse_mode="HTML"),
        chat_id = groupID,
        message_id = messageID
        )   
    async def sendReaction(self, toChat: str, react: str = 'typing'):
        return await self.bot.send_chat_action(toChat, react)

    async def getFile(self, fileId: str):
        return await self.bot.get_file(fileId)
    
    async def downloadFile(self, path: str, name: str):
        return await self.bot.download_file(path, name)
    
    async def pinMessage(self, chatid, messageid):
        return await self.bot.pin_chat_message(chat_id=chatid, message_id=messageid, disable_notification=True)
    
    async def unpinMessage(self, chatid, messageid):
        return await self.bot.unpin_chat_message(chat_id=chatid, message_id=messageid)
    
    async def me(self):
        return await self.bot.get_me()

    async def getChatMember(self, userID: int, groupID: int):
        status = await self.bot.get_chat_member(chat_id=groupID, user_id=userID)
        return status['status']
