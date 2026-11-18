SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS jingcaixing DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE jingcaixing;
CREATE TABLE IF NOT EXISTS attractions (
  attraction_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category ENUM('历史人文','自然风光','美食探店') NOT NULL,
  description TEXT NOT NULL,
  duration INT UNSIGNED NOT NULL,
  opening_hours VARCHAR(100) NOT NULL,
  latitude DECIMAL(10,7) NOT NULL,
  longitude DECIMAL(10,7) NOT NULL,
  image_path VARCHAR(255) DEFAULT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_attractions_category (category), INDEX idx_attractions_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
