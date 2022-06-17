CREATE TABLE "user"
(
    id text primary key,
    first_name text not null,
    last_name text not null,
    password text not null
);

CREATE TABLE "task"
(
    id text primary key,
    creation_time timestamp without time zone not null default current_timestamp,
    due_time timestamp without time zone not null,
    owner_id text not null,
    description text not null,
    done bool not null,
    foreign key (owner_id) references "user"(id) on delete cascade
);