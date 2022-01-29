CREATE TABLE Users ( User_ID   STRING PRIMARY KEY, User_Name STRING);

CREATE TABLE Tasks ( Task_ID       INTEGER  PRIMARY KEY, Task_Name     STRING   NOT NULL, Task_Due_Date DATETIME, Task_Est_Min  INTEGER
);

CREATE TABLE User_Tasks ( User_ID           STRING  REFERENCES Users (User_ID), Task_ID           INT     REFERENCES Tasks (Task_ID), Task_Is_Completed BOOLEAN DEFAULT (FALSE) );
