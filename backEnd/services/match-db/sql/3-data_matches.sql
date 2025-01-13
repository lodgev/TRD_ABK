INSERT INTO matches (home_team_id, away_team_id, start_date, end_date)
SELECT 
    c1.id AS home_team_id,
    c2.id AS away_team_id,
    GREATEST(c1.start_date, c2.start_date) AS start_date,
    LEAST(c1.end_date, c2.end_date) AS end_date
FROM 
    clubs c1
JOIN 
    clubs c2
ON 
    c1.id < c2.id -- Уникнення дублювання (A vs B і B vs A)
    AND c1.level = c2.level -- Тільки команди одного рівня
    AND c1.start_date <= c2.end_date -- Перетин дат початку/кінця
    AND c2.start_date <= c1.end_date;
