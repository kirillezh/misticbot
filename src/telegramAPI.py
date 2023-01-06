from src.locales import localisation
class telegramAPI:
    def __init__(self, bot):
        self.bot=bot
        
    async def sendPhoto(self, toСhat: int, photoId: str, caption: str = "", messageId: str = None, end: str = " \n"+localisation['end']):
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

    async def uploadPhoto(self, toСhat: int, photoId: str, caption: str = "", messageId: str = None, end: str = " \n"+localisation['end']):
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
    
    async def sendVideoURL(self, toСhat: int, videoURL: str, messageId: int,caption: str = "", end: str = " \n"+localisation['end'], disableNotification: bool = True):
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
    
    
    async def reply(self, message, text: str, end: str = " \n"+localisation['end'], disableURL: bool = True):
        await self.sendReaction(message.chat.id, 'typing')
        return await self.bot.send_message( 
            message.chat.id, 
            f"{text}{end}",
            parse_mode="HTML", 
            disable_web_page_preview=disableURL,
            reply_to_message_id=message.message_id)

    async def editText(self, message, text: str, end: str = " \n"+localisation['end'], disableURL: bool = True):
        return await message.edit_text(
            f"{text}{end}",
            parse_mode="HTML", 
            disable_web_page_preview=disableURL)
    async def editPhoto(self, message, photoId: str, text: str, end: str = " \n"+localisation['end']):
        from aiogram import types
        return await message.edit_media(
            media = types.InputMediaPhoto(open(photoId, 'rb'),
            caption = f"{text}{end}",
            parse_mode="HTML"))

    async def sendReaction(self, toChat: str, react: str = 'typing'):
        return await self.bot.send_chat_action(toChat, react)

    async def getFile(self, fileId: str):
        return await self.bot.get_file(fileId)
    
    async def downloadFile(self, path: str, name: str):
        return await self.bot.download_file(path, name)
    