-- Advance Schema for Voice Viva
ALTER TABLE questions ADD COLUMN concepts TEXT AFTER question_text;

ALTER TABLE viva_answers ADD COLUMN feedback TEXT AFTER max_score;
ALTER TABLE viva_answers ADD COLUMN confidence FLOAT AFTER feedback;

ALTER TABLE viva_sessions ADD COLUMN is_submitted BOOLEAN DEFAULT FALSE AFTER current_index;
ALTER TABLE viva_sessions ADD COLUMN submitted_at DATETIME AFTER is_submitted;
