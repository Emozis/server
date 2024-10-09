INSERT INTO users (user_id, user_email, user_password, user_name, user_profile, user_join_date, user_is_active, user_gender, user_birthdate) 
VALUES 
(1, 'john.doe@example.com', 'hashed_password_123', 'John Doe', 'profile_pic_1.jpg', NOW(), true, 'male', '1990-05-15'), 
(2, 'jane.doe@example.com', 'hashed_password_456', 'Jane Doe', 'profile_pic_2.jpg', NOW(), true, 'female', '1988-08-25')
;
