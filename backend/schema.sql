CREATE TABLE "user"
(
    id text primary key,
    first_name text NOT NULL,
    last_name text NOT NULL,
    password text NOT NULL
);

CREATE TABLE "task"
(
    id text primary key,
    creation_time timestamp without time zone NOT NULL default current_timestamp,
    due_time text NOT NULL,
    owner_id text NOT NULL,
    description text NOT NULL,
    done bool NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES "user"(id) ON DELETE CASCADE
);

