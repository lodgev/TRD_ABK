INSERT INTO bets (user_id, match_id, amount, bet_type, selected_team, status, created_at)
VALUES 
    (1, 1, 100.00, 'win', 'Man City', 'pending', '2024-09-15 10:00:00'),
    (2, 1, 50.00, 'lose', 'Real Madrid', 'pending', '2024-09-15 10:05:00'),
    (3, 2, 200.00, 'draw', 'Man City', 'pending', '2024-09-16 12:00:00'),
    (2, 3, 150.00, 'win', 'Arsenal', 'pending', '2024-09-17 14:30:00'),
    (1, 4, 75.00, 'lose', 'Inter', 'pending', '2024-09-18 16:15:00'),
    (3, 2, 300.00, 'win', 'Man City', 'pending', '2024-09-19 18:45:00');
