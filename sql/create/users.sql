-- Table: public.users

-- DROP TABLE public.users;

CREATE TABLE public.users
(
  id_user integer NOT NULL DEFAULT nextval('users_id_user_seq'::regclass),
  name text,
  login text,
  password text,
  status text,
  privilege integer DEFAULT 0,
  pack numeric(32,6),
  status_pack text DEFAULT 'Стандарт'::text,
  day_update date,
  pack_standart numeric(32,6),
  rating numeric(32,6),
  CONSTRAINT users_pkey PRIMARY KEY (id_user)
)
WITH (
  OIDS=FALSE
);

-- Index: public.users_login_uindex

-- DROP INDEX public.users_login_uindex;

CREATE UNIQUE INDEX users_login_uindex
  ON public.users
  USING btree
  (login COLLATE pg_catalog."default");


-- Trigger: update_coefficient on public.users

-- DROP TRIGGER update_coefficient ON public.users;

CREATE TRIGGER update_coefficient
  BEFORE UPDATE
  ON public.users
  FOR EACH ROW
  EXECUTE PROCEDURE public.update_coefficient_user();

