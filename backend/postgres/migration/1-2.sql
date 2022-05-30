CREATE TABLE IF NOT EXISTS users(
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL, 
    encrypted_password VARCHAR(255),
    deleted boolean DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS todo_lists (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE, 
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    priority INTEGER NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'OPEN',
    created_at TIMESTAMP not NULL,
    updated_at TIMESTAMP,
    deleted boolean DEFAULT FALSE,
    status_changed_on TIMESTAMP
);