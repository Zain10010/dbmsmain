-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS alumni_db;
USE alumni_db;

-- Drop existing table if it exists
DROP TABLE IF EXISTS alumni;

-- Create the alumni table
CREATE TABLE IF NOT EXISTS alumni (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    
    -- Education Details
    degree VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    graduation_year INT NOT NULL,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    
    -- Professional Information
    current_employer VARCHAR(100),
    job_title VARCHAR(100),
    industry VARCHAR(100),
    years_of_experience INT,
    linkedin TEXT,  -- Changed from VARCHAR(200) to TEXT to accommodate longer URLs
    
    -- Location
    current_city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    
    -- Skills and Interests
    technical_skills TEXT,
    languages_known TEXT,
    areas_of_interest TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_email ON alumni(email);
CREATE INDEX idx_student_id ON alumni(student_id);
CREATE INDEX idx_graduation_year ON alumni(graduation_year);
CREATE INDEX idx_department ON alumni(department); 