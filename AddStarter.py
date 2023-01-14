import win32com.client
import os
from tkinter.messagebox import Message

TASK_TRIGGER_LOGON = 8
TASK_CREATE_OR_UPDATE = 6
TASK_ACTION_EXEC = 0

scheduler = win32com.client.Dispatch("Schedule.Service")
scheduler.Connect()
rootFolder = scheduler.GetFolder("\\")

taskDef = scheduler.NewTask(0)
TASK_RUNLEVEL_HIGHEST = 1
TASK_LOGON_SERVICE_ACCOUNT = 5
taskDef.Principal.DisplayName = "SYSTEM"
taskDef.Principal.GroupID = "Administrators"
taskDef.Principal.LogonType = TASK_LOGON_SERVICE_ACCOUNT
taskDef.Principal.RunLevel = TASK_RUNLEVEL_HIGHEST
colTriggers = taskDef.Triggers

trigger = colTriggers.Create(TASK_TRIGGER_LOGON)
trigger.Id = "LogonTriggerId"

colActions = taskDef.Actions
action = colActions.Create(TASK_ACTION_EXEC)
action.ID = "Mojiboard"
action.Path = r"cmd.exe"
action.Arguments =f'/c start "" "{os.getcwd()}\\Mojiboard.exe"'


info = taskDef.RegistrationInfo
info.Author = "Mojiboard"
info.Description = "Run Mojiboard.exe when the current user logs on"

settings = taskDef.Settings
settings.Hidden = False

try:
    result = rootFolder.RegisterTaskDefinition("Mojiboard", taskDef, TASK_CREATE_OR_UPDATE, taskDef.Principal.UserID, "", TASK_LOGON_SERVICE_ACCOUNT)
    Message(parent=None, title="성공!", message="시작 스케줄러에 Mojiboard를 추가했습니다!").show()
except Exception as e:
    Message(parent=None, title="오류!", message=e).show()
