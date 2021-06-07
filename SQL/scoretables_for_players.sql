-- QI
USE cpbl_data;
SELECT score_fact.Batting, player_dim.Name, COUNT(player_dim.Name) AS Times
FROM score_fact
INNER JOIN player_dim 
ON score_fact.Player_id = player_dim.Player_id
WHERE Batting IN (3, 4, 5) 
GROUP BY player_dim.Name
ORDER BY Times DESC
LIMIT 30;

-- GROUP BY score_fact.Batting, player_dim.Name
-- ORDER BY score_fact.Batting, Times DESC;

USE cpbl_data;
DROP TABLE StaticsScore;

USE cpbl_data;
CREATE TABLE StaticsScore(
	year INTEGER, Batting INTEGER, 
    Team TEXT, Name TEXT,
    Total_PA INTEGER, 
    Total_AB INTEGER,
    Total_H INTEGER, 
    Total_HR INTEGER, 
    KK DECIMAL(5,2), BB DECIMAL(5,2),
	AVG DECIMAL(4,3), OBP DECIMAL(4,3), 
    SLG DECIMAL(4,3), OPS DECIMAL(4,3)
)DEFAULT CHARSET=utf8;
INSERT INTO StaticsScore
SELECT year, Batting, Team, Name, 
			Total_PA, Total_AB,Total_H, Total_HR, KK, BB,
            AVG, OBP, SLG, OPS
FROM 
(
	SELECT year, Score_Fact.Batting, team_dim.Team, Player_Dim.Name, 
		SUM(AB) +(SUM(BB) + SUM(SF) + SUM(SAC)) AS Total_PA,
		SUM(AB) AS Total_AB, SUM(H) AS Total_H, 
		SUM(HR) AS Total_HR, 
		ROUND((SUM(SO)*1.00 / (SUM(AB) +SUM(BB) + SUM(SF) + SUM(SAC)))*100, 2) AS KK,
		ROUND((SUM(BB)*1.00 / (SUM(AB) +SUM(BB) + SUM(SF) + SUM(SAC)))*100, 2) AS BB,
		ROUND(SUM(H)*1.0/SUM(AB) ,3) AS AVG,
		ROUND(((SUM(H) + SUM(BB) + SUM(HBP))*1.0 / (SUM(AB) + SUM(BB) + SUM(SF) + SUM(HBP))) , 3) AS OBP,
		ROUND((SUM(H)+ SUM(2B) + 2*SUM(3B) + 3*SUM(HR))*1.0 / SUM(AB) ,3)AS SLG,
		ROUND(((SUM(H) + SUM(BB) + SUM(HBP))*1.0 / (SUM(AB) + SUM(BB) + SUM(SF) + SUM(HBP))) + (SUM(H)+ SUM(2B) + 2*SUM(3B) + 3*SUM(HR))*1.0 / SUM(AB) ,3)AS OPS
	FROM Score_Fact 
	INNER JOIN player_dim
	ON Score_Fact.Player_id = player_dim.Player_id
	INNER JOIN team_dim
	ON Score_Fact.Team_id = team_dim.Team_id
	GROUP BY year, Batting, Name 
	ORDER BY year, Batting, Name
) AS ori
GROUP BY year, Batting, Name 
ORDER BY year, Batting, Name ;


-- QII
USE cpbl_data;
CREATE TABLE statPlayerScore(
	Batting INTEGER , 
    Name TEXT,
    Total_PA INTEGER, 
    Total_AB INTEGER,
    Total_H INTEGER, 
    Total_HR INTEGER, 
    KK DECIMAL(5,2), BB DECIMAL(5,2),
	AVG DECIMAL(4,3), OBP DECIMAL(4,3), 
    SLG DECIMAL(4,3), OPS DECIMAL(4,3)
)DEFAULT CHARSET=utf8;

INSERT INTO statPlayerScore
SELECT Batting, Name, 
		Total_PA, Total_AB,Total_H, Total_HR, KK, BB,
		AVG, OBP, SLG, OPS
FROM 
(
	SELECT Score_Fact.Batting, Player_Dim.Name, 
		SUM(AB) +(SUM(BB) + SUM(SF) + SUM(SAC)) AS Total_PA,
		SUM(AB) AS Total_AB, SUM(H) AS Total_H, 
		SUM(HR) AS Total_HR, 
		ROUND((SUM(SO)*1.00 / (SUM(AB) +SUM(BB) + SUM(SF) + SUM(SAC)))*100, 2) AS KK,
		ROUND((SUM(BB)*1.00 / (SUM(AB) +SUM(BB) + SUM(SF) + SUM(SAC)))*100, 2) AS BB,
		ROUND(SUM(H)*1.0/SUM(AB) ,3) AS AVG,
		ROUND(((SUM(H) + SUM(BB) + SUM(HBP))*1.0 / (SUM(AB) + SUM(BB) + SUM(SF) + SUM(HBP))) , 3) AS OBP,
		ROUND((SUM(H)+ SUM(2B) + 2*SUM(3B) + 3*SUM(HR))*1.0 / SUM(AB) ,3)AS SLG,
		ROUND(((SUM(H) + SUM(BB) + SUM(HBP))*1.0 / (SUM(AB) + SUM(BB) + SUM(SF) + SUM(HBP))) + (SUM(H)+ SUM(2B) + 2*SUM(3B) + 3*SUM(HR))*1.0 / SUM(AB) ,3)AS OPS
	FROM Score_Fact 
	INNER JOIN player_dim
	ON Score_Fact.Player_id = player_dim.Player_id
	INNER JOIN team_dim
	ON Score_Fact.Team_id = team_dim.Team_id
	GROUP BY Batting, Name 
	ORDER BY Batting, Name
) AS ori
GROUP BY Batting, Name 
ORDER BY Batting, Name ;






