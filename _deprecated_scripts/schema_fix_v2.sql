-- Add subject_id and rename question to question_text in questions table
ALTER TABLE `questions` ADD COLUMN `subject_id` INT(11) AFTER `id`;
ALTER TABLE `questions` CHANGE `question` `question_text` TEXT DEFAULT NULL;
ALTER TABLE `questions` ADD CONSTRAINT `fk_question_subject` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;
