-- ============================================
-- Voice Viva Database Schema Fix
-- ============================================
-- Run this in your MySQL client (phpMyAdmin, MySQL Workbench, or command line)

USE voice_viva_db;

-- 1. Add generation_status column to subjects table
ALTER TABLE subjects 
ADD COLUMN generation_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending';

-- 2. Rename 'subject' to 'subject_id' in questions table
ALTER TABLE questions 
CHANGE COLUMN subject subject_id INT;

-- 3. Rename 'question' to 'question_text' in questions table
ALTER TABLE questions 
CHANGE COLUMN question question_text TEXT;

-- 4. Verify the changes
SELECT 'Subjects table structure:' AS info;
SHOW COLUMNS FROM subjects;

SELECT 'Questions table structure:' AS info;
SHOW COLUMNS FROM questions;
