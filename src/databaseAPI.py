import sqlite3
from datetime import datetime
from types import NoneType
import logging, json

class databaseAPI:
    def __init__(self, src="src/database.db"):
        self.src = src
        self.database = sqlite3.connect(self.src)
        row = self.createTable()
        if(row != 'ok'):
            logging.critical(row)

    #CreateTable
    def createTable(self):
        try:
            #CreateTable User
            stmt = "CREATE TABLE IF NOT EXISTS users (user_id integer,user_username text DEFAULT NULL,user_name text,user_bio text,user_date_added datetime DEFAULT NULL,user_premium num DEFAULT '0', PRIMARY KEY (user_id))"
            self.database.execute(stmt)
            self.database.commit()
            #CreateTable Group
            stmt = "CREATE TABLE IF NOT EXISTS supergroup (group_id integer, group_name text, group_bio text, group_date_added datetime, group_admins text DEFAULT 'owner', group_lang text DEFAULT 'ua', group_siren num DEFAULT NULL, group_city text DEFAULT 'Kyiv', group_siren_id text DEFAULT NULL, group_voicy num DEFAULT NULL, group_tiktok num DEFAULT NULL, group_youtube num DEFAULT NULL, group_reels num DEFAULT NULL, group_twitter num, PRIMARY KEY (group_id))"
            self.database.execute(stmt)
            self.database.commit()
            #CreateTable Messages
            stmt = "CREATE TABLE IF NOT EXISTS messages (message_id integer,message_id_user integer,message_id_group integer,message_text text DEFAULT NULL,message_file text DEFAULT NULL,message_full text, message_time datetime, PRIMARY KEY (message_id))"
            self.database.execute(stmt)
            self.database.commit()
            #CreateTable usersToGroup
            stmt = "CREATE TABLE IF NOT EXISTS userstogroup (user_id integer,group_id integer,status text DEFAULT 'member', date_added datetime, PRIMARY KEY (user_id, group_id))"
            self.database.execute(stmt)
            self.database.commit()
            #CreateTable photoBase
            stmt = "CREATE TABLE IF NOT EXISTS photo_base (photo_id text,photo_name text, PRIMARY KEY (photo_id))"
            self.database.execute(stmt)
            self.database.commit()
            #CreateTable infoBot
            stmt = "CREATE TABLE IF NOT EXISTS info_bot (bot_name text,bot_link text,version text)"
            self.database.execute(stmt)
            self.database.commit()
            #importInfoBot
            if(self.selectInfo() is None):
                f = json.load(open('info.json'))
                self.newInfo(f['name'], f['link'], f['version'])
            #CreateTable citySiren
            stmt = "CREATE TABLE IF NOT EXISTS city_siren (city_id integer,city_name text,city_siren num, PRIMARY KEY (city_id))"
            self.database.execute(stmt)
            self.database.commit()
            #importCities
            row = self.selectAllCity()
            if(row == []):
                from src.locales import cities
                for city in cities:
                    self.newCity(cities[city])

        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return 'ok'
    #User
    def selectUser(self, userID: int):
        stmt = "SELECT * FROM users WHERE user_id=(?)"
        args = (userID, )
        return self.database.execute(stmt, args).fetchone()
    
    def selectAllUser(self):
        stmt = "SELECT * FROM users ORDER BY user_date_added"
        return self.database.execute(stmt).fetchall()

    def newUser(self, userID: int, userName: str, userUsername: str = '', userBio: str = '', userDataAdded = '', userPremium: bool = False):
        if(type(userPremium) is NoneType):
            userPremium = False
        stmt = "INSERT INTO users (user_id, user_username, user_name, user_bio, user_date_added, user_premium) VALUES (?, ?, ?, ?, ?, ?)"
        args = (userID, userUsername, userName,userBio, (datetime.now(), userDataAdded)[userDataAdded!=''], (0, 1)[userPremium])
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    def updateUser(self, userID: int, userName: str, userUsername: str = '', userBio: str = '', userPremium: bool = False):
        stmt = "UPDATE users SET user_name=(?), user_username=(?), user_bio=(?), user_premium=(?) WHERE user_id=(?)"
        args = (userName, userUsername, userBio, userPremium, userID)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    #Group
    def selectGroup(self, groupID: int):
        stmt = "SELECT * FROM supergroup WHERE group_id=(?)"
        args = (groupID, )
        return self.database.execute(stmt, args).fetchone()
    
    def selectAllGroup(self):
        stmt = "SELECT * FROM supergroup ORDER BY group_date_added"
        return self.database.execute(stmt).fetchall()

    def newGroup(self, groupID: int, groupName: str, groupBio: str = '', groupDataAdded = '', groupAdmins: str = "administrator", groupLang: str = "ua", groupSiren: bool = False, groupCity: str = "Kyiv city", groupVoicy: bool = True, groupTiktok: bool = True, groupYoutube: bool = False, groupReels: bool = False, groupTwitter: bool = False):
        stmt = "INSERT INTO supergroup (group_id, group_name, group_bio, group_date_added, group_admins, group_lang, group_siren, group_city, group_voicy, group_tiktok, group_youtube, group_reels, group_twitter) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        args = (groupID, groupName, groupBio, (datetime.now(), groupDataAdded)[groupDataAdded!=''], groupAdmins, groupLang, (groupSiren if 1 else 0), groupCity, (groupVoicy if 1 else 0), (groupTiktok if 1 else 0), (groupYoutube if 1 else 0), (groupReels if 1 else 0), (groupTwitter if 1 else 0))
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    def updateGroup(self, groupID: int, groupName: str, groupBio: str = ''):
        stmt = "UPDATE supergroup SET group_name=(?), group_bio=(?) WHERE group_id=(?)"
        args = (groupName, groupBio, groupID)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    def updateRightGroup(self, groupID: int, change: str, arg):
        stmt = "UPDATE supergroup SET "+change+"=(?) WHERE group_id=(?)"
        args = (arg, groupID)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"
    
    #Messages
    def selectMessageByID(self, messageID: int):
        stmt = "SELECT * FROM messages WHERE message_id=(?)"
        args = (messageID, )
        return self.database.execute(stmt, args).fetchone()

    def selectMessagesByUser(self, userID: int):
        stmt = "SELECT * FROM messages WHERE message_id_user=(?) ORDER BY message_time"
        args = (userID, )
        return self.database.execute(stmt, args).fetchall()

    def selectMessagesByGroup(self, groupID: int):
        stmt = "SELECT * FROM messages WHERE message_id_group=(?) ORDER BY message_time"
        args = (groupID, )
        return self.database.execute(stmt, args).fetchall()

    def selectAllMessages(self):
        stmt = "SELECT * FROM messages ORDER BY message_time"
        return self.database.execute(stmt).fetchall()

    def newMessage(self, messageID: int, userID: int, groupID: int, messageFull: str, messageText: str = "", messageFile: str = "", messageTime = None):
        stmt = "INSERT INTO messages (message_id, message_id_user, message_id_group, message_text, message_file, message_full, message_time) VALUES (?, ?, ?, ?, ?, ?, ?)"
        args = (messageID, userID, groupID, messageText, messageFile, messageFull, (messageTime, datetime.now())[messageTime is None])
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    #UserToGroup
    def selectUserFromGroup(self, userID: int, groupID: int):
        stmt = "SELECT * FROM userstogroup WHERE user_id=(?), group_id=(?)"
        args = (userID, groupID)
        return self.database.execute(stmt, args).fetchone()

    def selectAllUsersFromGroup(self, groupID: int):
        stmt = "SELECT * FROM userstogroup WHERE group_id=(?) ORDER BY date_added"
        args = (groupID,)
        return self.database.execute(stmt, args).fetchall()
    
    def selectAlGroupsFromUser(self, userID: int):
        stmt = "SELECT * FROM userstogroup WHERE user_id=(?) ORDER BY date_added"
        args = (userID,)
        return self.database.execute(stmt, args).fetchall()

    def newUserFromGroup(self, userID: int, groupID: int, status: str = "member", dateAdded = ''):
        stmt = "INSERT INTO userstogroup (user_id, group_id, status, date_added) VALUES (?, ?, ?, ?)"
        args = (userID, groupID, status, (datetime.now(), date_added)[dateAdded!=''])
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    def updateUserStatus(self, userID: int, groupID: int, status: str):
        stmt = "UPDATE userstogroup SET status=(?) WHERE user_id=(?), group_id=(?)"
        args = (status, userID, groupID)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    #InfoBot
    def selectInfo(self):
        stmt = "SELECT * FROM info_bot"
        return self.database.execute(stmt).fetchone()

    def newInfo(self, botName: str, botLink: str, botVersion: str):
        stmt = "INSERT INTO info_bot (bot_name, bot_link, version) VALUES (?, ?, ?)"
        args = (botName, botLink, botVersion)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    def updateInfo(self,botName: str, botLink: str, botVersion: str):
        stmt = "UPDATE info_bot SET bot_name=(?), bot_link=(?), version=(?)"
        args = (botName, botLink, botVersion)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    #CitySiren
    def selectCity(self, cityName: str = "Kyiv city"):
        stmt = "SELECT * FROM city_siren WHERE city_name=(?)"
        args = (cityName,)
        return self.database.execute(stmt, args).fetchone()
    
    def selectAllCity(self):
        stmt = "SELECT * FROM city_siren ORDER BY city_name"
        return self.database.execute(stmt).fetchall()

    def newCity(self, cityName: str, citySiren: bool = False):
        stmt = "INSERT INTO city_siren (city_name, city_siren) VALUES (?, ?)"
        args = (cityName, citySiren)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    def updateCity(self,cityName: str, citySiren: bool):
        stmt = "UPDATE city_siren SET city_siren=(?) WHERE city_name=(?)"
        args = (citySiren, cityName)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    #PhotoBase
    def selectPhoto(self, photoName: str):
        stmt = "SELECT * FROM photo_base WHERE photo_name=(?)"
        args = (photoName,)
        return self.database.execute(stmt, args).fetchone()
    
    def selectAllPhoto(self):
        stmt = "SELECT * FROM photo_base WHERE ORDER BY photo_name"
        return self.database.execute(stmt).fetchall()

    def newPhoto(self, photoID: str, photoName: str = ""):
        stmt = "INSERT INTO photo_base (photo_id, photo_name) VALUES (?, ?)"
        args = (photoID, photoName)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"

    def updatePhoto(self,photoID: str, photoName: str):
        stmt = "UPDATE photo_base SET photo_id=(?) WHERE photo_name=(?)"
        args = (photoID, photoName)
        try:
            self.database.execute(stmt, args)
            self.database.commit()
        except sqlite3.Error as error:
            return {
                "result": "error",
                "except": error
            }
        return "ok"