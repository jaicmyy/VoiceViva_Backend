-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 08, 2026 at 04:15 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

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
  `subject_id` int(11) NOT NULL,
  `difficulty` enum('easy','medium','hard') NOT NULL,
  `question_text` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `concepts` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `subject_id`, `difficulty`, `question_text`, `created_at`, `concepts`) VALUES
(1, 1, 'easy', 'Can you provide an example of a simple introduction to formal proof in mathematics?', '2026-01-04 14:55:38', NULL),
(2, 1, 'medium', 'Can you explain the process of constructing a direct proof for a given statement, using an example related to Topology?', '2026-01-04 14:58:09', NULL),
(3, 1, 'hard', 'Can you explain the process of constructing a direct proof for a given statement, and provide an example where this method is applied to prove that if \'n\' is an integer and n^2 is odd, then n must be odd?', '2026-01-04 14:58:53', NULL),
(4, 1, 'easy', 'Can you explain the different types of additional evidence that can be used to support a Total Cost of Ownership (TOC) analysis, and provide an example for each type?', '2026-01-04 14:59:25', NULL),
(5, 1, 'hard', 'Ask a hard difficulty level viva question about additional forms of proof in legal proceedings.', '2026-01-04 15:09:47', NULL),
(6, 1, 'easy', 'Can you explain the basic principles behind finite automata and how they are used to recognize patterns in strings?', '2026-01-04 15:11:58', NULL),
(7, 1, 'medium', 'Can you explain the significance of deterministic finite automata (DFA) in the context of language recognition and provide an example where DFA is used to recognize a specific pattern within strings?', '2026-01-04 15:13:43', NULL),
(8, 1, 'hard', 'Can you explain the significance of deterministic finite automata (DFA) in the context of language recognition and provide an example where DFA is used to solve a problem?', '2026-01-04 15:14:20', NULL),
(9, 1, 'easy', 'Can you explain the process of converting a regular expression to an equivalent Finite Automaton, and provide an example with its corresponding FA diagram?', '2026-01-04 15:15:01', NULL),
(10, 1, 'medium', 'Can you explain how a deterministic finite automaton (DFA) can be used to recognize patterns in strings, and provide an example of such a pattern?', '2026-01-04 15:16:55', NULL),
(11, 1, 'hard', 'Can you explain the process of converting a given regular expression into an equivalent Finite Automaton, and discuss how this conversion impacts the computational power of FA?', '2026-01-04 15:17:51', NULL),
(12, 1, 'easy', 'Can you explain how a Deterministic Finite Automaton (DFA) processes an input string and determine whether it is accepted by the automaton? Please provide an example with a simple DFA diagram and corresponding transition table.', '2026-01-04 15:19:04', NULL),
(13, 1, 'medium', 'Can you explain how a Deterministic Finite Automaton (DFA) can be used to recognize patterns in strings, and provide an example of such a pattern recognition?', '2026-01-04 15:19:34', NULL),
(14, 1, 'hard', 'Explain how a Deterministic Finite Automaton can be used to recognize the language of all strings over the alphabet {a, b} that contain an even number of \'a\'s. Provide both the state diagram and the transition table for your DFA.', '2026-01-04 15:20:05', NULL),
(15, 1, 'easy', 'Can you explain the process of converting a deterministic finite automaton (DFA) into a non-deterministic finite automaton (NFA), and provide an example to illustrate this conversion?', '2026-01-04 15:20:35', NULL),
(16, 1, 'medium', 'Can you explain the process of converting a deterministic finite automaton (DFA) into an equivalent non-deterministic finite automaton (NFA), and discuss any potential advantages or disadvantages of using NFAs over DFAs in certain scenarios?', '2026-01-04 15:21:02', NULL),
(17, 1, 'easy', 'Can you explain the concept of equivalence between Non-deterministic Finite Automata (NFA) and Deterministic Finite Automata (DFA), particularly in terms of their computational power?', '2026-01-04 15:22:13', NULL),
(18, 1, 'medium', 'Can you explain the process by which a Non-deterministic Finite Automaton (NFA) can be converted into an equivalent Deterministic Finite Automaton (DFA), and discuss any potential challenges or limitations that may arise during this conversion?', '2026-01-04 15:22:45', NULL),
(19, 1, 'easy', 'Ask a viva question about Finite Automata with Epsilon transitions', '2026-01-04 15:30:28', NULL),
(20, 1, 'medium', 'Can you explain the role of epsilon transitions in converting a non-deterministic finite automaton (NFA) to its equivalent deterministic finite automaton (DFA), and provide an example where such a transition is crucial for maintaining the language equivalence?', '2026-01-04 15:31:12', NULL),
(21, 1, 'hard', 'Can you explain the role of epsilon transitions in converting a nondeterministic finite automaton (NFA) to its equivalent deterministic finite automaton (DFA), and provide an example where this conversion is applied?', '2026-01-04 15:31:50', NULL),
(22, 1, 'easy', 'Can you explain how a deterministic finite automaton (DFA) can be represented using regular expressions, and provide an example to illustrate this equivalence?', '2026-01-04 15:34:46', NULL),
(23, 1, 'medium', 'Can you explain how the equivalence between deterministic finite automata (DFA) and regular expressions is established, particularly focusing on the construction of a DFA from a given regular expression? Please provide an example to illustrate your explanation.', '2026-01-04 15:35:46', NULL),
(24, 1, 'hard', 'Can you explain the process to demonstrate that a given Deterministic Finite Automaton (DFA) is equivalent to a specific regular expression, and discuss any potential challenges or limitations in this equivalence?', '2026-01-04 15:36:43', NULL),
(25, 1, 'easy', 'Can you explain the Pumping Lemma for regular sets and provide an example of how it can be used to prove that a given language is not regular?', '2026-01-04 15:37:19', NULL),
(26, 1, 'medium', 'Can you explain the Pumping Lemma for regular languages and demonstrate how it can be used to prove that a given language is not regular? Please provide an example with your explanation.', '2026-01-04 15:37:42', NULL),
(27, 1, 'easy', 'Explain the concept of Pumping Lemma and how it can be used to prove that a given language is not regular. Provide an example with a specific non-regular language, demonstrating its application.', '2026-01-04 15:39:48', NULL),
(28, 1, 'medium', 'Can you explain how the Pumping Lemma for regular languages can be used to prove that a given language is not regular? Please provide an example with your explanation.', '2026-01-04 15:40:34', NULL),
(29, 1, 'hard', 'Given a regular language L, explain how you would use the Pumping Lemma to prove that it is not context-free. Provide an example of such a language and demonstrate the application of the Pumping Lemma in your explanation.', '2026-01-04 15:42:16', NULL),
(30, 1, 'easy', 'Can you explain the difference between active and passive voice in English grammar, providing examples for each?', '2026-01-04 15:43:02', NULL),
(31, 1, 'easy', 'Can you explain the difference between a context-free grammar (CFG) and a regular grammar, and provide an example of each?', '2026-01-04 15:46:59', NULL),
(32, 1, 'medium', 'Can you explain the process of converting a given context-free grammar into its corresponding Chomsky Normal Form (CNF) and discuss how this transformation can affect the complexity of parsing algorithms?', '2026-01-04 15:47:38', NULL),
(33, 1, 'hard', 'Can you explain the process of converting a given context-free grammar into Chomsky Normal Form (CNF) and discuss its significance in parsing algorithms?', '2026-01-04 15:48:40', NULL),
(34, 1, 'easy', 'Can you explain the process and benefits of simplifying a Context-Free Grammar (CFG) in terms of parsing efficiency?', '2026-01-04 15:51:28', NULL),
(35, 1, 'medium', 'Can you explain the process and challenges involved in simplifying a Context-Free Grammar (CFG) while ensuring that the simplified grammar still accurately represents the original language?', '2026-01-04 15:52:11', NULL),
(36, 1, 'hard', 'Can you explain the process and challenges involved in simplifying a Context-Free Grammar (CFG) while ensuring that it still generates the same language as the original CFG?', '2026-01-04 15:53:20', NULL),
(37, 1, 'easy', 'Can you explain the concept of Greibach Normal Form and its significance in context-free grammar?', '2026-01-04 15:53:56', NULL),
(38, 1, 'medium', 'Can you explain the concept of Greibach Normal Form and its significance in context-free grammar? Please provide an example to illustrate your explanation.', '2026-01-04 15:54:26', NULL),
(39, 1, 'hard', 'Can you explain the process of transforming a given non-linear programming problem into its Greibach Normal Form and discuss how this transformation can aid in solving complex optimization problems?', '2026-01-04 15:55:09', NULL),
(40, 1, 'easy', 'Can you explain the process of converting a context-free grammar into Chomsky normal form and discuss its significance in parsing algorithms?', '2026-01-04 15:55:39', NULL),
(41, 1, 'easy', 'Can you explain the difference between Conjunctive Normal Form (CNF) and Generalized Normal Form (GNF), and provide an example of converting a given Boolean expression into both CNF and GNF?', '2026-01-04 15:58:20', NULL),
(42, 1, 'medium', 'Can you explain the process of converting a given propositional logic formula into Conjunctive Normal Form (CNF) and then to Generalized Conjunctive Normal Form (GNF), and discuss any potential challenges or limitations that may arise during this conversion?', '2026-01-04 15:59:56', NULL),
(43, 1, 'hard', 'Can you explain the process of converting a given propositional logic formula into Conjunctive Normal Form (CNF) and then to Generalized Conjunctive Normal Form (GNF), highlighting any potential challenges or complexities that may arise during this transformation?', '2026-01-04 16:00:39', NULL),
(44, 1, 'easy', 'Can you explain how context can be applied in everyday communication to enhance understanding and avoid misinterpretation?', '2026-01-04 16:01:09', NULL),
(45, 1, 'medium', 'Can you explain how the concept of context can be applied in improving natural language processing algorithms, particularly in understanding and generating human-like text?', '2026-01-04 16:01:32', NULL),
(46, 1, 'hard', 'Discuss the role and significance of context in Total Cost Management (TOC) practices, particularly how it influences decision-making processes within an organization. Provide examples to illustrate your points.', '2026-01-04 16:02:00', NULL),
(47, 1, 'easy', 'Can you explain the closure properties of context-free languages under union, concatenation, and Kleene star operations?', '2026-01-04 16:02:36', NULL),
(48, 1, 'medium', 'Can you explain how the closure properties apply to context-free languages, specifically under union and concatenation operations? Please provide examples illustrating these properties.', '2026-01-04 16:03:09', NULL),
(49, 1, 'hard', 'Can you explain how the closure properties apply to context-free languages, specifically under union and concatenation operations? Please provide examples demonstrating these properties.', '2026-01-04 16:03:31', NULL),
(50, 1, 'easy', 'Can you explain the Pumping Lemma for Context-Free Languages (CFL) and provide an example of how it can be used to prove that a given language is not context-free?', '2026-01-04 16:04:00', NULL),
(51, 1, 'hard', 'Can you explain the Pumping Lemma for Context-Free Languages (CFL) and demonstrate how it can be used to prove that a given language is not context-free? Please provide an example with your explanation.', '2026-01-04 16:05:00', NULL),
(52, 1, 'easy', 'Can you explain the basic principles behind the language used in Programming for Personal Digital Assistants (PDAs) and how it differs from general-purpose programming languages?', '2026-01-04 16:05:34', NULL),
(53, 1, 'medium', 'Can you explain the role and significance of Post-Principal Diagram (PDA) notation in representing the syntax of a programming language, particularly focusing on its application to context-free grammars?', '2026-01-04 16:06:11', NULL),
(54, 1, 'hard', 'Can you explain the role and significance of Post Operational Conditions (POCs) in the context of a PDA, particularly how they influence system behavior and decision-making processes?', '2026-01-04 16:06:45', NULL),
(55, 1, 'easy', 'Can you explain the concept of equivalence between pushdown automata (PDA) and context-free grammars (CFG), particularly how a PDA can be used to recognize the language generated by a given CFG?', '2026-01-04 16:07:18', NULL),
(56, 1, 'medium', 'Can you explain the equivalence between context-free grammars (CFG) and pushdown automata (PDA), particularly how a PDA can be used to recognize languages generated by CFGs?', '2026-01-04 16:07:46', NULL),
(57, 1, 'hard', 'Can you explain the relationship between context-free grammars (CFG) and pushdown automata (PDA), particularly how a CFG can be converted into an equivalent PDA, and vice versa? Please provide examples to illustrate your explanation.', '2026-01-04 16:08:31', NULL),
(58, 1, 'easy', 'Can you explain the basic components of a Turing machine and how they interact during computation?', '2026-01-04 16:09:03', NULL),
(59, 1, 'medium', 'Can you explain the process of how a Turing machine reads and writes symbols on its tape, including the role of the head movement?', '2026-01-04 16:09:28', NULL),
(60, 1, 'hard', 'Can you explain the process of how a Turing machine computes a function, and provide an example where it demonstrates its computational power by solving a problem that is not feasible for a conventional computer?', '2026-01-04 16:09:56', NULL),
(61, 1, 'easy', 'Can you explain the concept of a Turing machine and how it relates to programming techniques, particularly in terms of its theoretical foundation for modern computing?', '2026-01-04 16:10:32', NULL),
(62, 1, 'medium', 'Can you explain how the concept of \'programs\' in a Turing machine relates to modern programming techniques, and provide an example where this relationship is evident?', '2026-01-04 16:11:31', NULL),
(63, 1, 'hard', 'Can you explain the process of converting a given non-deterministic finite automaton (NFA) into an equivalent deterministic finite automaton (DFA), and discuss the potential challenges that may arise during this conversion?', '2026-01-04 16:12:50', NULL),
(64, 1, 'easy', 'Can you explain the concept of finite control storage and its application in a simple real-world scenario?', '2026-01-04 16:13:40', NULL),
(65, 1, 'medium', 'Can you explain the concept of finite control storage and its significance in the context of Total Ordering (TOC) systems?', '2026-01-04 16:14:19', NULL),
(66, 1, 'hard', 'Can you explain the concept of finite control storage and its significance in real-time systems, particularly focusing on how it affects system performance and reliability?', '2026-01-04 16:14:53', NULL),
(67, 1, 'easy', 'Can you explain the concept of \'checking off symbols\' in TOC and provide an example where this technique is applied?', '2026-01-04 16:15:59', NULL),
(68, 1, 'medium', 'Can you explain the process of checking off symbols in TOC and its significance in ensuring accurate data representation?', '2026-01-04 16:16:50', NULL),
(69, 1, 'hard', 'Can you explain the process and significance of checking symbols in Topological Condensate (TOC) theory, particularly how it contributes to our understanding of quantum states?', '2026-01-04 16:17:26', NULL);

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

--
-- Dumping data for table `student_assignments`
--

INSERT INTO `student_assignments` (`id`, `student_id`, `subject_id`, `assigned_at`) VALUES
(4, 4, 1, '2026-01-05 16:44:24');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `syllabus_pdf` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `generation_status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`id`, `name`, `code`, `syllabus_pdf`, `created_at`, `generation_status`) VALUES
(1, 'TOC', 'CSA06', '813a4e7e-eb06-471f-8749-2153c633c56b_CSA13_TOC_-_Syllabus_-Template.docx.pdf', '2026-01-04 14:49:15', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `registration_number` varchar(50) NOT NULL,
  `role` enum('admin','student') NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `registration_number`, `role`, `name`, `created_at`, `password`) VALUES
(1, 'ADMIN001', 'admin', 'Admin User', '2026-01-04 06:58:48', 'admin123'),
(4, '192224144', 'student', '192224144', '2026-01-05 16:44:24', 'STUXADQOXSB');

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
  `answered_at` datetime DEFAULT NULL,
  `feedback` text DEFAULT NULL,
  `evaluation_method` varchar(20) DEFAULT NULL,
  `llm_status` varchar(20) DEFAULT NULL,
  `evaluated_at` datetime DEFAULT NULL,
  `confidence` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `viva_answers`
--

INSERT INTO `viva_answers` (`id`, `session_id`, `question_id`, `audio_path`, `transcript`, `score`, `max_score`, `answered_at`, `feedback`, `evaluation_method`, `llm_status`, `evaluated_at`, `confidence`) VALUES
(6, 30, 4, 'uploads/audio_answers\\30_4.webm', '� moyīīīīīīīīīīīīī � bebīĜīČąăąăĎĎĎĎēĎčĎĎĊįĜĥĨđĄČĶĊđęĵČČĎ� bütün īīĜĭĽĵīĨīīīįĽīīīīĪīīīıįīīīīīīīıđĚęıďĄđĎđĎ� WORĮīį� Quick insertingđĸęıĵīıĦ diamond plate � various encara� independonly geography', 0.8, 2, '2026-01-05 10:59:31', NULL, NULL, NULL, NULL, NULL),
(7, 51, 47, 'uploads/audio_answers/51_47.webm', 'Hello, hello, hello.', 0, 2, '2026-01-05 17:00:08', NULL, NULL, NULL, NULL, NULL),
(31, 66, 52, 'uploads/audio_answers/66_52.webm', '', 0, 2, '2026-01-05 22:27:17', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(32, 65, 61, 'uploads/audio_answers/65_61.webm', 'a  a  r  n  aw  m  o  n  r  n  r  n', 0.8, 2, '2026-01-05 22:25:42', 'Auto-evaluated (fallback).', 'llm', 'completed', NULL, NULL),
(33, 67, 27, 'uploads/audio_answers/67_27.webm', '', 0, 2, '2026-01-05 22:29:11', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(43, 68, 64, 'uploads/audio_answers/68_64.webm', 'Thanks for watching!', 0, 2, '2026-01-05 22:41:00', 'Auto-evaluated (fallback).', 'llm', 'completed', NULL, NULL),
(46, 69, 41, 'uploads/audio_answers/69_41.webm', '', 0, 2, '2026-01-05 23:08:44', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(58, 70, 47, 'uploads/audio_answers/70_47_c2da38f9.webm', 'Thank you for watching.', 0, 2, '2026-01-05 23:38:13', 'Answer too short or unclear.', 'llm', 'completed', NULL, NULL),
(68, 71, 9, 'uploads/audio_answers/71_9_2b8f23f022c2451a977aa325db662973.webm', '', 0, 2, '2026-01-06 08:23:29', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(81, 72, 15, 'uploads/audio_answers/72_15_d656ca0e71c244b2af530898f7bcfbba.webm', 'Thank you for watching!', 0, 2, '2026-01-06 08:36:05', 'Answer too short or unclear.', 'llm', 'completed', NULL, NULL),
(82, 72, 31, 'uploads/audio_answers/72_31_367e0f10ee3d485abbec8f87209e3889.webm', '् satisfied  ् satisfied  ् satisfied', 0, 2, '2026-01-06 08:36:15', 'Answer does not address the question.', 'llm', 'completed', NULL, NULL),
(83, 72, 6, 'uploads/audio_answers/72_6_daeefd4bf20a4c4ba9cabf4b8f37abee.webm', '', 0, 2, '2026-01-06 08:37:12', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(84, 72, 53, 'uploads/audio_answers/72_53_3698f85bc28246e19a0d9e18f7d5c4ff.webm', '', 0, 4, '2026-01-06 08:37:53', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(85, 72, 59, 'uploads/audio_answers/72_59_d80f9e43010242f2a54ffeeb7a6b820f.webm', 'सोंब खर भाडनी Away  ओर तो विखी', 0, 4, '2026-01-06 08:40:19', 'Answer does not address the question.', 'llm', 'completed', NULL, NULL),
(86, 72, 4, 'uploads/audio_answers/72_4_d51818ef94474da7a77361ca8b6a1eac.webm', 'MCU ๏ ๏ ๏ ๏ ๏ ๏ ๏ ๏ ๏ ๏ ๏ ๏ ๏ ๏ Burma Gauri Hama   Crystal\", class 5th year in Tiger King.   ๏ ๏ ๏ ๏ The one who played in Hama.  ๏ ๏ ๏ ๏ ๏ Raibhan  ๏ ๏ ๏ Hama, the one who played in Hama,  ๏ ๏ ๏ ๏ The one who played in Hama.', 2, 2, '2026-01-06 08:39:14', 'Correct answer.', 'llm', 'completed', NULL, NULL),
(87, 72, 11, 'uploads/audio_answers/72_11_52d51b3682b74f719d08052dd5e39db3.webm', '', 0, 6, '2026-01-06 08:39:38', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(88, 72, 34, 'uploads/audio_answers/72_34_88590ed5ac234a04bd7c1030cf7acbf8.webm', '너무 다 먹었으면 좋겠지  롱블루  롱블루  롱블루  롱블루  롱블루  롱블루', 0, 2, '2026-01-06 08:39:40', 'Answer does not address the question.', 'llm', 'completed', NULL, NULL),
(89, 72, 63, 'uploads/audio_answers/72_63_4d2120b95d654aea9b06baf3fc73e4ce.webm', '', 0, 6, '2026-01-06 08:39:41', 'No answer provided.', 'llm', 'completed', NULL, NULL),
(91, 73, 30, 'uploads/audio_answers/73_30_c7b6120c62b74b01b81c975d7c94a72e.webm', '', 0, 2, '2026-01-06 09:03:00', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(92, 73, 19, 'uploads/audio_answers/73_19_288d77c63e7c400291aadc2ffaf9b33f.webm', '', 0, 2, '2026-01-06 09:04:29', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(94, 73, 4, 'uploads/audio_answers/73_4_443c5c1937cd4d01b344a446e37a49c0.webm', 'Thank you very much.', 0, 2, '2026-01-06 09:04:46', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(95, 73, 61, 'uploads/audio_answers/73_61_002c45d5b95e42ffa28bbf35616b2247.webm', 'I want to do it.', 0.4, 2, '2026-01-06 09:04:46', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(96, 73, 41, 'uploads/audio_answers/73_41_e77f17eea6d64dd0aa706e26f83f423e.webm', 'Thank you for watching.', 0, 2, '2026-01-06 09:04:46', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(97, 73, 56, 'uploads/audio_answers/73_56_ee97a1707f7d4ff2a983c679d7ca0430.webm', 'Come on.', 0, 4, '2026-01-06 09:04:58', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(98, 73, 65, 'uploads/audio_answers/73_65_a5b719a68900455f9cb2cc918a422548.webm', 'Dragon  Ok.  Let me fight, Dragon.', 0.8, 4, '2026-01-06 09:11:12', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(99, 73, 62, 'uploads/audio_answers/73_62_02c56f1df47a4c1a8caf83ffdaf1a66c.webm', 'He\'s on fire.', 0, 4, '2026-01-06 09:05:19', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(100, 73, 38, 'uploads/audio_answers/73_38_f575378a22b84e0da2d4f1652ea33115.webm', 'You', 0, 4, '2026-01-06 09:05:33', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(101, 73, 21, 'uploads/audio_answers/73_21_94bd533db80c4762820edf8d51b8183c.webm', 'GORDON  ඏ දම Allāh වළි වන්ව මස් දමටඩි ආ blat  ටම එරදු පමටය  අල අපිය', 0, 6, '2026-01-06 09:09:05', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(102, 73, 66, 'uploads/audio_answers/73_66_4eff45ea87564e129198cc60b86c6771.webm', '', 0, 6, '2026-01-06 09:09:59', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(104, 74, 58, 'uploads/audio_answers/74_58_5fac3ca0851e40cb8f0d71047094c83d.webm', 'आप, अज़े पनु आप', 0, 2, '2026-01-06 09:19:38', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(105, 74, 9, 'uploads/audio_answers/74_9_f6fe6500b28e440f84c925558dfced40.webm', '너무 맞아', 0, 2, '2026-01-06 09:19:56', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(106, 74, 6, 'uploads/audio_answers/74_6_52f8b99890724e4fa2de600beec6445e.webm', 'You', 0, 2, '2026-01-06 09:19:56', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(107, 74, 64, 'uploads/audio_answers/74_64_ad88d76f15b744e698230b8b8bf44e28.webm', 'I can\'t do it for you now.', 0.4, 2, '2026-01-06 09:20:10', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(108, 74, 67, 'uploads/audio_answers/74_67_d0e74e63f3fa43f1a922064e6f5f6b2f.webm', 'Just see if you can stay down.', 0.4, 2, '2026-01-06 09:20:23', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(109, 74, 10, 'uploads/audio_answers/74_10_65d7e99fa5454099aa3f835eea28a860.webm', '', 0, 4, '2026-01-06 09:20:28', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(110, 74, 42, 'uploads/audio_answers/74_42_34f2180c9582496bbff0869ea4644018.webm', '', 0, 4, '2026-01-06 09:22:11', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(111, 74, 68, 'uploads/audio_answers/74_68_2c4c63550280428886b59e6157e37137.webm', '', 0, 4, '2026-01-06 09:22:16', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(112, 74, 65, 'uploads/audio_answers/74_65_7b5b7b578d874cfca5c2956136dc969c.webm', 'Oh, you did it!', 0, 4, '2026-01-06 09:23:11', 'Auto-evaluated (limited confidence).', 'llm', 'completed', NULL, 50),
(113, 74, 5, 'uploads/audio_answers/74_5_81028bfb4c7848ceac38909d0aad3213.webm', '', 0, 6, '2026-01-06 09:23:23', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50),
(114, 74, 14, 'uploads/audio_answers/74_14_1ce9bd19721e40e5b7ae2c10125dda35.webm', '', 0, 6, '2026-01-06 09:23:53', 'Answer too short to evaluate.', 'llm', 'completed', NULL, 50);

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

--
-- Dumping data for table `viva_config`
--

INSERT INTO `viva_config` (`id`, `subject_id`, `duration_minutes`, `total_marks`, `easy_marks`, `easy_questions`, `medium_marks`, `medium_questions`, `hard_marks`, `hard_questions`, `created_at`) VALUES
(2, 1, 10, 50, 10, 5, 20, 4, 20, 2, '2026-01-05 03:34:24');

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
  `generated_at` datetime DEFAULT current_timestamp(),
  `pdf_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `viva_reports`
--

INSERT INTO `viva_reports` (`id`, `session_id`, `student_id`, `subject_id`, `total_questions`, `total_score`, `max_total_score`, `percentage`, `grade`, `generated_at`, `pdf_path`) VALUES
(1, 74, 4, 1, NULL, NULL, NULL, NULL, NULL, '2026-01-06 09:29:57', 'reports/generated_reports\\viva_report_23a0e32e7c984b61be29303bbae23a0f.pdf');

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
  `completed_at` timestamp NULL DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `is_submitted` tinyint(1) DEFAULT 0,
  `report_path` varchar(255) DEFAULT NULL,
  `final_score` float DEFAULT NULL,
  `grade` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `viva_sessions`
--

INSERT INTO `viva_sessions` (`id`, `student_id`, `subject_id`, `easy_q_ids`, `medium_q_ids`, `hard_q_ids`, `current_index`, `started_at`, `completed_at`, `submitted_at`, `is_submitted`, `report_path`, `final_score`, `grade`) VALUES
(64, 4, 1, NULL, NULL, NULL, 0, '2026-01-05 16:44:39', NULL, NULL, 0, NULL, NULL, NULL),
(65, 4, 1, NULL, NULL, NULL, 0, '2026-01-05 16:54:09', NULL, NULL, 0, NULL, NULL, NULL),
(66, 4, 1, NULL, NULL, NULL, 0, '2026-01-05 16:55:05', NULL, NULL, 0, NULL, NULL, NULL),
(67, 4, 1, NULL, NULL, NULL, 0, '2026-01-05 16:55:52', NULL, NULL, 0, NULL, NULL, NULL),
(68, 4, 1, NULL, NULL, NULL, 0, '2026-01-05 17:06:14', NULL, NULL, 0, NULL, NULL, NULL),
(69, 4, 1, NULL, NULL, NULL, 0, '2026-01-05 17:32:46', NULL, NULL, 0, NULL, NULL, NULL),
(70, 4, 1, NULL, NULL, NULL, 0, '2026-01-05 18:03:15', NULL, NULL, 0, NULL, NULL, NULL),
(71, 4, 1, NULL, NULL, NULL, 0, '2026-01-06 02:45:38', NULL, NULL, 0, NULL, NULL, NULL),
(72, 4, 1, NULL, NULL, NULL, 0, '2026-01-06 03:03:36', NULL, NULL, 0, NULL, NULL, NULL),
(73, 4, 1, NULL, NULL, NULL, 0, '2026-01-06 03:32:45', NULL, NULL, 0, NULL, NULL, NULL),
(74, 4, 1, NULL, NULL, NULL, 0, '2026-01-06 03:48:02', NULL, '2026-01-06 09:29:57', 1, NULL, NULL, NULL),
(75, 4, 1, NULL, NULL, NULL, 0, '2026-01-08 02:01:40', NULL, NULL, 0, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_question_subject` (`subject_id`);

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
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_answer` (`session_id`,`question_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `student_assignments`
--
ALTER TABLE `student_assignments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `viva_answers`
--
ALTER TABLE `viva_answers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- AUTO_INCREMENT for table `viva_config`
--
ALTER TABLE `viva_config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `viva_reports`
--
ALTER TABLE `viva_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `viva_sessions`
--
ALTER TABLE `viva_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `fk_question_subject` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;

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
