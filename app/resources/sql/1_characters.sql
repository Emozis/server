INSERT INTO characters (character_id, character_name, character_profile, character_gender, character_personality, character_details, character_description, character_greeting, character_created_at, character_updated_at, character_is_public, character_likes, character_usage_count, character_is_active, user_id) 
VALUES 
(1, 'Alice', 'profile1.png', 'female', 'Friendly', 'Loves nature and animals', 'A friendly character with a deep love for the environment.', 'Hello! Let''s save the planet together!', NOW(), NOW(), true, 10, 5, true, 1),
(2, 'Bob', 'profile2.png', 'male', 'Brave', 'Always stands up for others', 'A brave character who never backs down from challenges.', 'Ready for adventure? Let''s go!', NOW(), NOW(), true, 15, 8, true, 1),
(3, 'Charlie', 'profile3.png', 'other', 'Curious', 'Wants to explore the world', 'A curious character who is always asking questions.', 'What are we going to discover today?', NOW(), NOW(), true, 20, 12, true, 2)
;