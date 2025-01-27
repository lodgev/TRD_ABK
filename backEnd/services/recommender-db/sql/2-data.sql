INSERT INTO user_actions (club_id, user_id, action, timestamp) VALUES
(1, 'f928c455-d2f3-4e30-bf58-178ae041e8c2', 'liked', '2025-01-23 10:15:00'),
(2, 'f928c455-d2f3-4e30-bf58-178ae041e8c2', 'disliked', '2025-01-23 10:20:00'),
(3, 'f928c455-d2f3-4e30-bf58-178ae041e8c2', 'liked', '2025-01-23 10:25:00');

INSERT INTO feedback (timestamp, user_id, news_id, action, rating) VALUES
('2025-01-23T20:06:12.449722', 'd275b8cf-7e9a-458f-a4ad-f77a35c57381', 'A22F8CCDD1E49ADC580862AA628391F5', 'not_interested', NULL),
('2025-01-23T20:29:38.860240', 'd275b8cf-7e9a-458f-a4ad-f77a35c57381', '56E6C7BB11876B6737032E9FA205B7CE', 'rated', 1),
('2025-01-23T20:29:45.028578', 'd275b8cf-7e9a-458f-a4ad-f77a35c57381', '56E6C7BB11876B6737032E9FA205B7CE', 'rated', 3);

