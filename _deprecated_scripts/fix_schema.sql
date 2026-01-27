-- Fix database schema for Voice Viva

-- 1. Add generation_status to subjects table
ALTER TABLE subjects 
ADD COLUMN IF NOT EXISTS generation_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending';

-- 2. Rename subject to subject_id in questions table (if exists)
-- Note: MySQL doesn't support IF EXISTS for column changes, so this may error if already done
-- ALTER TABLE questions CHANGE COLUMN subject subject_id INT;

-- 3. Rename question to question_text in questions table (if exists)
-- ALTER TABLE questions CHANGE COLUMN question question_text TEXT;

-- Check if columns need renaming
SELECT 'Checking questions table structure...' AS status;
SHOW COLUMNS FROM questions;
