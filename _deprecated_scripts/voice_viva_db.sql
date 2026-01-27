-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 07, 2026 at 06:10 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `voice_viva_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `topic` varchar(255) DEFAULT NULL,
  `question` text DEFAULT NULL,
  `difficulty` enum('easy','medium','hard') DEFAULT NULL,
  `source` enum('ai','human') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `student_assignments`
--

CREATE TABLE `student_assignments` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `assigned_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `syllabus_pdf` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `registration_number` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','student') NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `registration_number`, `password`, `role`, `name`, `created_at`) VALUES
(1, 'admin', 'Admin', 'admin', 'John Student', '2026-01-05 04:50:06'),
(2, 'admin02', 'admin123', 'admin', 'Second Admin', '2026-01-06 04:53:42'),
(3, 'CS2021001', 'stu123', 'student', 'Ravi Kumar', '2026-01-06 14:13:30');

-- --------------------------------------------------------

--
-- Table structure for table `viva_answers`
--

CREATE TABLE `viva_answers` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `audio_path` varchar(255) DEFAULT NULL,
  `transcript` text DEFAULT NULL,
  `score` float DEFAULT 0,
  `max_score` float DEFAULT 5,
  `answered_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `viva_config`
--

CREATE TABLE `viva_config` (
  `id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `duration_minutes` int(11) NOT NULL,
  `total_marks` int(11) NOT NULL,
  `easy_marks` int(11) DEFAULT 0,
  `easy_questions` int(11) DEFAULT 0,
  `medium_marks` int(11) DEFAULT 0,
  `medium_questions` int(11) DEFAULT 0,
  `hard_marks` int(11) DEFAULT 0,
  `hard_questions` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `viva_reports`
--

CREATE TABLE `viva_reports` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `total_questions` int(11) DEFAULT NULL,
  `total_score` float DEFAULT NULL,
  `max_total_score` float DEFAULT NULL,
  `percentage` float DEFAULT NULL,
  `grade` varchar(5) DEFAULT NULL,
  `generated_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `viva_sessions`
--

CREATE TABLE `viva_sessions` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `easy_q_ids` text DEFAULT NULL,
  `medium_q_ids` text DEFAULT NULL,
  `hard_q_ids` text DEFAULT NULL,
  `current_index` int(11) DEFAULT 0,
  `started_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `completed_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student_assignments`
--
ALTER TABLE `student_assignments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_student` (`student_id`),
  ADD KEY `fk_subject` (`subject_id`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `registration_number` (`registration_number`);

--
-- Indexes for table `viva_answers`
--
ALTER TABLE `viva_answers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `viva_config`
--
ALTER TABLE `viva_config`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_viva_subject` (`subject_id`);

--
-- Indexes for table `viva_reports`
--
ALTER TABLE `viva_reports`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_session` (`session_id`);

--
-- Indexes for table `viva_sessions`
--
ALTER TABLE `viva_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_viva_student` (`student_id`),
  ADD KEY `fk_viva_subject2` (`subject_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student_assignments`
--
ALTER TABLE `student_assignments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `viva_answers`
--
ALTER TABLE `viva_answers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `viva_config`
--
ALTER TABLE `viva_config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `viva_reports`
--
ALTER TABLE `viva_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `viva_sessions`
--
ALTER TABLE `viva_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `student_assignments`
--
ALTER TABLE `student_assignments`
  ADD CONSTRAINT `fk_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_subject` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `viva_config`
--
ALTER TABLE `viva_config`
  ADD CONSTRAINT `fk_viva_subject` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `viva_sessions`
--
ALTER TABLE `viva_sessions`
  ADD CONSTRAINT `fk_viva_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_viva_subject2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
