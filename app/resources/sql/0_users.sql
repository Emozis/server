INSERT INTO users (user_email, user_password, user_name, user_profile, user_created_at, user_is_active, user_gender, user_birthdate) 
VALUES 
('admin@example.com', '$2b$12$61erR2SQzWEW0y1DiyAKmeSrGFguq33/GiXE3fNJCSStGdfly9JAa', 'admin', 'admin.jpg', NOW(), true, 'other', '2024-01-01'),
('test@example.com', '$2b$12$61erR2SQzWEW0y1DiyAKmeSrGFguq33/GiXE3fNJCSStGdfly9JAa', 'Test User', 'test.jpg', NOW(), true, 'other', '2024-01-01')
;