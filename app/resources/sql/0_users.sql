INSERT INTO users (user_email, user_password, user_name, user_profile, user_created_at, user_is_active, user_gender, user_role, user_birthdate) 
VALUES 
('emozis001@gmail.com', '$2b$12$YZwC71f1PSrKo2S.fU1ttuCZOD1Vb/TPUiZFhrhk8pvCP4yjzGnB6', 'emogi-admin', Null, NOW(), true, 'other','admin' ,'2024-01-01'),
('test@example.com', '$2b$12$61erR2SQzWEW0y1DiyAKmeSrGFguq33/GiXE3fNJCSStGdfly9JAa', 'Test User', 'test.jpg', NOW(), true, 'other','user', '2024-01-01')
;