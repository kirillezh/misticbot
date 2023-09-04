from src.databaseAPI import databaseAPI

class dbHelper:
    def __init__(self, ):
        self.db  = databaseAPI()
    #main
    def full_check(self, message):
        row = self.user(message.from_user)
        if(row != 'ok'):
            return row
        row = self.group(message.chat)
        if(row != 'ok'):
            return row
        row = self.message(message)
        if(row != 'ok'):
            return row
        return row
        
    #Users
    def user(self, userInfo):
        row = self.db.selectUser(userInfo.id)
        if(row is None):
            row = self.db.newUser(userID= userInfo.id, userName= userInfo.full_name, userUsername= userInfo.username, userPremium=userInfo.is_premium)
        else:
            row = self.db.updateUser(userID= userInfo.id, userName= userInfo.full_name, userUsername= userInfo.username, userPremium=userInfo.is_premium)
        return row 

    def infoUser(self, userID):
        return self.db.selectUser(userID)

    def allUsers(self):
        return self.db.selectAllUser()

    #Group
    def group(self, groupInfo):
        row = self.db.selectGroup(groupInfo.id)
        if(row is None):
            if(groupInfo.id>0):
                row = self.db.newGroup(groupID= groupInfo.id, groupName=groupInfo.full_name, groupAdmins='member')
            else:
                row = self.db.newGroup(groupID=groupInfo.id, groupName=groupInfo.title, groupBio=groupInfo.bio)
        else:
            if(groupInfo.id>0):
                row = self.db.updateGroup(groupID= groupInfo.id, groupName=groupInfo.full_name)
            else:
                row = self.db.updateGroup(groupID=groupInfo.id, groupName=groupInfo.title, groupBio=groupInfo.bio)
        return row 

    def infoGroup(self, groupID):
        return self.db.selectGroup(groupID)

    def groupWithCity(self, city: str):
        groups = []
        row = self.db.selectAllGroup()
        for group in row:
            if(group[7] == city and group[6] == 1):
                groups.append(group)
        return groups

    def allGroup(self):
        return self.db.selectAllGroup()

    def updateGroup(self, groupID: int, change: str, args: bool = False):
        return self.db.updateRightGroup(groupID, change, (args if 1 else 0))
    
    #Messages
    def message(self, message):
        return self.db.newMessage(
            messageID=message.message_id, 
            userID=message.from_user.id, 
            groupID=message.chat.id, 
            messageFull=str(message), 
            messageText=(('', str(message.caption))[message.caption != None], str(message.text))[message.text != None], 
            messageFile=
            ((( ''
                ,str(message.document) )[message.document != None]
                ,str(message.video) )[message.video != None]
                ,str(message.photo) )[message.photo != []])
    #PhotoBase
    def newPhoto(self, photoID: str, photoName: str):
        return self.db.newPhoto(photoID=photoID, photoName=photoName)
    
    def photo(self, photoName: str):
        return self.db.selectPhoto(photoName=photoName)
    
    def allPhoto(self):
        return self.db.selectAllPhoto()
    #CitySiren
    def city(self, city: str):
        return self.db.selectCity(city)
    
    def allCity(self):
        return self.db.selectAllCity()
    
    def updateCity(self, city: str, status: bool):
        return self.db.updateCity(city, status)

    #InfoBot
    def infoBot(self):
        return self.db.selectInfo()

    def updateInfoBot(self, version: str):
        old = self.infoBot()
        return self.db.updateInfo(old[0], old[1], version)