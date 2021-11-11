from utils.service_database import insert_data, get_data

def main(msg, option):
    group = msg.chat.id
    if msg.chat.type == "private":
        return
    if option == "no" or option == "false":
        opt = False
    elif option == "yes" or option == "true":
        opt = True
    elif option == None or option == "":
        p = get_data(group)
        return msg.reply(f"Current settings for cleanservice is: {p}")
    else:
        return msg.reply("Invalid arguments!\n\nArgumen tersedia: yes/no/true/false")

    result = insert_data(group, opt)
    if result == True:
        return msg.reply("Baiklah, setiap ada service message, akan saya hapus!", True)
    elif result == False:
        return msg.reply("Baiklah, setiap ada service message, tidak akan saya hapus!", True)
    else:
        return msg.reply("<code>Something went wrong while input to database!</code>", True)