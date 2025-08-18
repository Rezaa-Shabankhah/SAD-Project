CREATE DATABASE IF NOT EXISTS university_association;
USE university_association;

CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_number VARCHAR(20) NOT NULL UNIQUE,
  name VARCHAR(150) NOT NULL,
  role ENUM('STUDENT','MEMBER','ADMIN') NOT NULL DEFAULT 'STUDENT'
);

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  email VARCHAR(150) UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE article (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(300) NOT NULL,
  content LONGTEXT NOT NULL,
  status ENUM('DRAFT','PENDING','APPROVED','REJECTED') NOT NULL DEFAULT 'PENDING',
  published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE article_authors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  article_id INT NOT NULL,
  users_id INT NOT NULL,
  UNIQUE (article_id, users_id),
  FOREIGN KEY (article_id) REFERENCES article(id) ON DELETE CASCADE,
  FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE announcement (
  id INT AUTO_INCREMENT PRIMARY KEY,
  author_id INT NOT NULL,
  title VARCHAR(300) NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE event (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  capacity INT NOT NULL DEFAULT 0,
  registered_count INT NOT NULL DEFAULT 0,
  start_at DATETIME NULL,
  end_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event_registration (
  id INT AUTO_INCREMENT PRIMARY KEY,
  event_id INT NOT NULL,
  users_id INT NOT NULL,
  registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (event_id, users_id),
  FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
  FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE comments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  author_id INT,
  target_type ENUM('ARTICLE','ANNOUNCEMENT','EVENT') NOT NULL,
  target_id INT NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NULL,
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);


-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


INSERT INTO students (student_number, name, role) VALUES
('1','Reza','ADMIN'),
('2','Behnam','MEMBER'),
('3','Jack','STUDENT'),
('4','Arian','STUDENT'),
('5','Ali','STUDENT');

INSERT INTO users (student_id, email, password) VALUES
(1, 'admin', '0'),
(2, 'member', '0');

INSERT INTO announcement (author_id, title, content) VALUES
(1, 'Welcome Week', 'Welcome week schedule posted. Please check rooms and times.'),
(2, 'Coding is Fun!', 'Association bootcamp updated. Read before events.');

INSERT INTO article (title, content, status) VALUES
('How to join clubs', 'Steps and benefits of joining student clubs.', 'APPROVED'),
('Student Project Showcase', 'Sample project descriptions from students.', 'PENDING');

INSERT INTO article_authors (article_id, users_id) VALUES
(1, 1),
(2, 2);

INSERT INTO event (title, description, capacity, registered_count) VALUES
('Intro to Python', 'Beginner-friendly Python workshop.', 30, 1),
('Spring Picnic', 'Outdoor picnic with games and snacks.', 50, 0);

INSERT INTO event_registration (event_id, users_id) VALUES
(1, 2);
