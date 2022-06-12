create table if not exists users(
    id varchar(255) primary key,
    name varchar(255) not null,
    email varchar(255) not null, 
    encrypted_password varchar(255),
    deleted boolean default false
);

create table if not exists todo_lists (
    id varchar(255) primary key,
    user_id varchar(255) references users(id) on delete cascade, 
    title varchar(255) not null,
    description varchar(255) not null,
    priority integer not null,
    status varchar(255) not null default 'OPEN',
    created_at timestamp not null,
    updated_at timestamp,
    deleted boolean default false,
    status_changed_on timestamp
);