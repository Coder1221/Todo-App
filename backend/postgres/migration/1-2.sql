create table users if not exists(
    id  UUID PRIMARY KEY,
    name varchar(255) ,
    email varchar(255),
    encrypted_password varchar(255) not null,
    deleted boolean default false
);

create table todo_lists if not exists(
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    title varchar(255) not null,
    description varchar(255) ,
    priority integer default 0,
    status varchar default 'OPEN',
    created_at TIMESTAMP default current_timestamp,
    updated_at TIMESTAMP,
    deleted boolean default false
);