USE cpbl_data;
CREATE TABLE CountStartLines(
	Name TEXT,
    1st INTEGER NOT NULL DEFAULT 0, 
    2nd INTEGER NOT NULL DEFAULT 0, 
    3rd INTEGER NOT NULL DEFAULT 0,
    4th INTEGER NOT NULL DEFAULT 0, 
    5th INTEGER NOT NULL DEFAULT 0, 
    6th INTEGER NOT NULL DEFAULT 0,
    7th INTEGER NOT NULL DEFAULT 0, 
    8th INTEGER NOT NULL DEFAULT 0, 
    9th INTEGER NOT NULL DEFAULT 0,
    Total INTEGER NOT NULL DEFAULT 0,
    1st_Ratio DECIMAL(5,2), 2nd_Ratio DECIMAL(5,2), 3rd_Ratio DECIMAL(5,2),
    4th_Ratio DECIMAL(5,2), 5th_Ratio DECIMAL(5,2), 6th_Ratio DECIMAL(5,2),
    7th_Ratio DECIMAL(5,2), 8th_Ratio DECIMAL(5,2), 9th_Ratio DECIMAL(5,2)
)DEFAULT CHARSET=utf8;

INSERT INTO CountStartLines
SELECT 
Name,
IFNULL(SUM(CASE WHEN Batting = 1 THEN Times END), 0) AS 1st,
IFNULL(SUM(CASE WHEN Batting = 2 THEN Times END), 0) AS 2nd,
IFNULL(SUM(CASE WHEN Batting = 3 THEN Times END), 0) AS 3rd,
IFNULL(SUM(CASE WHEN Batting = 4 THEN Times END), 0) AS 4th,
IFNULL(SUM(CASE WHEN Batting = 5 THEN Times END), 0) AS 5th,
IFNULL(SUM(CASE WHEN Batting = 6 THEN Times END), 0) AS 6th,
IFNULL(SUM(CASE WHEN Batting = 7 THEN Times END), 0) AS 7th,
IFNULL(SUM(CASE WHEN Batting = 8 THEN Times END), 0) AS 8th,
IFNULL(SUM(CASE WHEN Batting = 9 THEN Times END), 0) AS 9th,
(SELECT SUM(Times) GROUP BY Name) AS Total,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 1 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2)  AS 1st_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 2 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 2nd_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 3 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 3rd_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 4 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 4th_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 5 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 5th_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 6 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 6th_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 7 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 7th_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 8 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 8th_Ratio,
ROUND(IFNULL((IFNULL(SUM(CASE WHEN Batting = 9 THEN Times END), 0)/ (SELECT SUM(Times) GROUP BY Name)*100), 0), 2) AS 9th_Ratio
FROM 
(
	SELECT score_fact.Batting, player_dim.Name, COUNT(Name) AS Times
	FROM score_fact
	JOIN player_dim
	ON  score_fact.Player_id = player_dim.Player_id
	GROUP BY Batting, Name
	ORDER BY Batting, Times DESC
) AS CB 
GROUP BY Name
ORDER BY Total DESC, Name;


-- Winning Persentage
USE cpbl_data;
CREATE TABLE WinningStartLines(
	Name TEXT,
    1stW INTEGER NOT NULL DEFAULT 0, 
    2ndW INTEGER NOT NULL DEFAULT 0, 
    3rdW INTEGER NOT NULL DEFAULT 0,
    4thW INTEGER NOT NULL DEFAULT 0, 
    5thW INTEGER NOT NULL DEFAULT 0, 
	6thW INTEGER NOT NULL DEFAULT 0,
    7thW INTEGER NOT NULL DEFAULT 0, 
    8thW INTEGER NOT NULL DEFAULT 0, 
    9thW INTEGER NOT NULL DEFAULT 0,
    TotalW INTEGER NOT NULL DEFAULT 0
)DEFAULT CHARSET=utf8;

INSERT INTO WinningStartLines
SELECT 
Name,
IFNULL(SUM(CASE WHEN Batting = 1 THEN WinTimes END), 0) AS 1stW,
IFNULL(SUM(CASE WHEN Batting = 2 THEN WinTimes END), 0) AS 2ndW,
IFNULL(SUM(CASE WHEN Batting = 3 THEN WinTimes END), 0) AS 3rdW,
IFNULL(SUM(CASE WHEN Batting = 4 THEN WinTimes END), 0) AS 4thW,
IFNULL(SUM(CASE WHEN Batting = 5 THEN WinTimes END), 0) AS 5thW,
IFNULL(SUM(CASE WHEN Batting = 6 THEN WinTimes END), 0) AS 6thW,
IFNULL(SUM(CASE WHEN Batting = 7 THEN WinTimes END), 0) AS 7thW,
IFNULL(SUM(CASE WHEN Batting = 8 THEN WinTimes END), 0) AS 8thW,
IFNULL(SUM(CASE WHEN Batting = 9 THEN WinTimes END), 0) AS 9thW,
(SELECT SUM(WinTimes) GROUP BY Name) AS TotalW
FROM 
(
	SELECT score_fact.Batting, player_dim.Name, COUNT(Name) AS WinTimes
	FROM score_fact
	JOIN player_dim
	ON  score_fact.Player_id = player_dim.Player_id
	JOIN match_dim
	ON score_fact.MatchID = match_dim.Match_ID
    WHERE Score_Fact.HA = Match_Dim.WinTeam
    GROUP BY Batting, Name
	ORDER BY Batting, WinTimes DESC
    
) AS WT
GROUP BY Name
ORDER BY TotalW DESC, Name ;

-- Create a table for Winning Ratio Menu
USE cpbl_data;
DROP TABLE WinningRatio;
USE cpbl_data;
CREATE TABLE WinningRatio(
	Batting INTEGER NOT NULL DEFAULT 0, 
    Name TEXT,
    Total_PA INTEGER NOT NULL DEFAULT 0, 
    Total_AB INTEGER NOT NULL DEFAULT 0, 
    Total_H INTEGER NOT NULL DEFAULT 0,  
    Total_HR INTEGER NOT NULL DEFAULT 0, 
    KK DECIMAL(5,2),
    BB DECIMAL(5,2),
    AVG DECIMAL(5,3),
    OBP DECIMAL(5,3),
    SLG DECIMAL(5,3),
    OPS DECIMAL(5,3),
    WinRatio DECIMAL(6,3)
)DEFAULT CHARSET=utf8;
INSERT INTO WinningRatio
SELECT Batting, statplayerscore.Name, Total_PA, Total_AB,Total_H, Total_HR, KK, BB, AVG, OBP, SLG, OPS, 
			ROUND((winningstartlines.TotalW*1.0 / countstartlines.Total)*100,3) AS WinRatio
FROM statPlayerScore 
LEFT JOIN countstartlines ON statplayerscore.Name = countstartlines.Name
LEFT JOIN winningstartlines ON statplayerscore.Name = winningstartlines.Name
GROUP BY Batting, Name
ORDER BY WinRatio DESC;






















