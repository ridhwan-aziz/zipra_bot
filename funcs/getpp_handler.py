from pyrogram.types import Message, InputMediaPhoto
from pyrogram import Client

def main(msg: Message, bot: Client):
    # Cek anonim
    if msg.from_user == None:
        return None
    
    if msg.reply_to_message != None:
        if msg.reply_to_message.from_user != None:
            user = msg.reply_to_message.from_user.id
    else:
        user = msg.from_user.id
    # Dapatkan list photo profile
    pp_count = bot.get_profile_photos_count(user)
    photos = bot.get_profile_photos(user)
    list_pp = []
    last = 0
    jumlah = len(photos)

    if pp_count == 0:
        return msg.reply(f"Tidak dapat menemukan profile photo. Mungkin dia tidak set profile photo atau mungkin dia set privasi foto.", True)
    while jumlah > 10:
        for i in range(last, last+10):
            list_pp.append(InputMediaPhoto(photos[i].file_id))
        msg.reply_media_group(list_pp)
        list_pp = []
        last += 10
        jumlah -= 10
    for i in range(last, pp_count):
        list_pp.append(InputMediaPhoto(photos[i].file_id))
    msg.reply_media_group(list_pp)
    return msg.reply(f"Jumlah photo profile: {pp_count}")
    
    