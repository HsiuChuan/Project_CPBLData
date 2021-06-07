grant all privileges on *.* to root@localhost identified by '' with grant option;
SET SQL_SAFE_UPDATES=0

/*
Load Needed RowData
 1. All30_Battings
 2. matchPointt
*/

USE cpbl_data;
CREATE TABLE All30_Battings(
	year integer NOT NULL DEFAULT 0 , ID integer NOT NULL DEFAULT 0,
    HA text, Team text, Batting integer NOT NULL DEFAULT 0, Name text,
    AB integer NOT NULL DEFAULT 0, R integer NOT NULL DEFAULT 0, H integer NOT NULL DEFAULT 0, RBI integer NOT NULL DEFAULT 0, 2B integer NOT NULL DEFAULT 0, 3B integer NOT NULL DEFAULT 0, 
    HR integer NOT NULL DEFAULT 0, GIDP integer NOT NULL DEFAULT 0, BB integer NOT NULL DEFAULT 0, HBP integer NOT NULL DEFAULT 0, SO integer NOT NULL DEFAULT 0, 
    SAC integer NOT NULL DEFAULT 0, SF integer NOT NULL DEFAULT 0, SB integer NOT NULL DEFAULT 0, CS integer NOT NULL DEFAULT 0, E integer NOT NULL DEFAULT 0, AVG decimal NOT NULL DEFAULT 0
    )DEFAULT CHARSET=utf8;

USE cpbl_data;
CREATE TABLE matchPoint(
	year integer NOT NULL DEFAULT 0,
    ID integer NOT NULL DEFAULT 0,
    AwayTeam text,
    HomeTeam text,
    Away_Score integer NOT NULL DEFAULT 0,
    Home_Score integer NOT NULL DEFAULT 0
)DEFAULT CHARSET=utf8;



/*
 Cleaning Date
*/

-- All30_Battings
-- TRIM the Chinese Names
USE cpbl_data;
UPDATE All30_Battings
SET Name = TRIM(REPLACE(Name, char(32), ''));
UPDATE All30_Battings
SET Name = REPLACE(Name, '*', '')
WHERE Name LIKE '*%';
UPDATE All30_Battings
SET Name = REPLACE(Name, '#', '')
WHERE Name LIKE '#%';  

-- All30_Battings
-- Rename the Home and Away Name
UPDATE All30_Battings
SET HA = CASE 
	WHEN HA = 'Home' THEN 'H'
	WHEN HA = 'Away' THEN 'A'
    else 'F' 
    END;

-- All30_Battings
-- Adding Column GameID Into Table
ALTER TABLE All30_Battings
ADD COLUMN GameID INTEGER;
ALTER TABLE All30_Battings
MODIFY GameID TEXT;
UPDATE All30_Battings
SET GameID = CONCAT( year, LPAD(ID, 3, 0), HA, Batting);  
ALTER Table All30_Battings
ADD COLUMN MatchID INTEGER NOT NULL DEFAULT 0;
UPDATE All30_Battings
SET MatchID = CONCAT( year, LPAD(ID, 3, 0));  

-- matchpoint
-- Adding Column WinTeam Into Table
USE cpbl_data;
ALTER Table matchpoint
ADD COLUMN WinTeam TEXT;
UPDATE matchpoint
SET WinTeam = CASE 
	WHEN Away_Score >  Home_Score THEN 'A'
	WHEN Away_Score <  Home_Score THEN 'H'
    else 'T' 
    END;

-- Adding Column WinTeam Into Table
ALTER Table matchpoint
ADD COLUMN MatchID INTEGER NOT NULL DEFAULT 0;
UPDATE matchpoint
SET MatchID = CONCAT( year, LPAD(ID, 3, 0));  



-- Creating Team_Dim
USE cpbl_data;
CREATE TABLE Team_Dim(
	Team text
)DEFAULT CHARSET=utf8;
INSERT INTO Team_Dim
SELECT DISTINCT Team
FROM All30_Battings;
ALTER TABLE Team_Dim
ADD COLUMN Team_id serial PRIMARY KEY;
ALTER TABLE Team_Dim 
MODIFY COLUMN Team_id INTEGER NOT NULL ;

-- Creating Player_Dim
USE cpbl_data;
CREATE TABLE Player_Dim(
	Team Text,
    Name text    
)DEFAULT CHARSET=utf8;
INSERT INTO Player_Dim
SELECT DISTINCT Team, Name
FROM All30_Battings
ORDER BY Team, Name;
ALTER TABLE Player_Dim
ADD COLUMN Player_id serial PRIMARY KEY;

-- Creating Match_Dim
USE cpbl_data;
CREATE TABLE Match_Dim(
	Match_ID INTEGER  PRIMARY KEY,
    AwayTeam Text,
    HomeTeam Text,
    WinTeam text    
)DEFAULT CHARSET=utf8;
INSERT INTO Match_Dim
SELECT MatchID, AwayTeam, HomeTeam, WinTeam
FROM matchpoint
ORDER BY MatchID;




-- Creating Score_Fact
-- Left Join into 
USE cpbl_data;
CREATE TABLE Score_Fact(
	GameID varchar(10) PRIMARY KEY,
    year INTEGER, MatchID INTEGER, Team_id INTEGER, Player_id INTEGER, HA TEXT, Batting INTEGER, 
    AB integer NOT NULL DEFAULT 0, R integer NOT NULL DEFAULT 0, H integer NOT NULL DEFAULT 0, 
    RBI integer NOT NULL DEFAULT 0, 2B integer NOT NULL DEFAULT 0, 3B integer NOT NULL DEFAULT 0, 
    HR integer NOT NULL DEFAULT 0, GIDP integer NOT NULL DEFAULT 0, BB integer NOT NULL DEFAULT 0, 
    HBP integer NOT NULL DEFAULT 0, SO integer NOT NULL DEFAULT 0, SAC integer NOT NULL DEFAULT 0, 
    SF integer NOT NULL DEFAULT 0, SB integer NOT NULL DEFAULT 0, CS integer NOT NULL DEFAULT 0, 
    E integer NOT NULL DEFAULT 0
);
INSERT INTO Score_Fact
SELECT  all30_battings.GameID, year, MatchID, Team_Dim.Team_id, Player_Dim.Player_id, HA, all30_battings.Batting, 
		AB, R, H, RBI, 2B, 3B, HR, GIDP, BB, HBP, SO, SAC, SF, SB, CS, E
FROM all30_battings
LEFT JOIN Team_Dim
	ON All30_Battings.Team = Team_Dim.Team
LEFT JOIN Player_Dim
	ON All30_Battings.Team = Player_Dim.Team AND All30_Battings.Name = Player_Dim.Name
LEFT JOIN Match_Dim
	ON All30_Battings.MatchID  = Match_Dim.Match_ID
ORDER BY GameID;

ALTER TABLE Team_Dim 
MODIFY COLUMN Team_id INTEGER NOT NULL ;
ALTER TABLE Score_Fact
ADD CONSTRAINT ScoreTeam_fkeys FOREIGN KEY (Team_id) REFERENCES Team_Dim (Team_id);
ALTER TABLE Player_Dim 
MODIFY COLUMN Player_id INTEGER NOT NULL ;
ALTER TABLE Score_Fact
ADD CONSTRAINT ScorePlayer_fkeys FOREIGN KEY (Player_id) REFERENCES Player_Dim (Player_id);
ALTER TABLE Score_Fact
ADD CONSTRAINT ScoreMatch_fkeys FOREIGN KEY (MatchID) REFERENCES Match_Dim (Match_ID);


SELECT Score_Fact.Batting, Score_Fact.Player_id, Player_Dim.Name, COUNT(Player_Dim.Name) AS Times
FROM Score_Fact 
INNER JOIN Player_Dim
ON Score_Fact.Player_id = Player_Dim.Player_id
WHERE Batting IN (3, 4, 5) 
GROUP BY Batting, Player_id
HAVING COUNT(Player_Dim.Name) > 200 
ORDER BY Batting, Times DESC, Player_id; 

SELECT Score_Fact.Batting, Score_Fact.Player_id, Player_Dim.Name, COUNT(Player_Dim.Name) AS Times
FROM Score_Fact 
INNER JOIN Player_Dim
ON Score_Fact.Player_id = Player_Dim.Player_id
INNER JOIN Match_Dim
ON Score_Fact.MatchID = Match_Dim.Match_ID
WHERE Batting IN (3, 4, 5) 
AND Score_Fact.HA = Match_Dim.WinTeam 
GROUP BY Batting, Player_id
ORDER BY Batting, Times DESC, Player_id; 



-- Check the Foreign Key
SELECT constraint_name, table_name, constraint_type
FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY';


