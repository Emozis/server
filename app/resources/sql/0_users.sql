INSERT INTO users (user_email, user_password, user_name, user_profile, user_join_date, user_is_active, user_gender, user_birthdate) 
VALUES 
('admin@example.com', 'hashed_password_123', 'admin', 'admin.jpg', NOW(), true, 'other', '2024-01-01'), 
('test@example.com', 'hashed_password_456', 'test', 'test.jpg', NOW(), true, 'other', '2024-01-01')
;