-- Table: public.session

-- DROP TABLE public.session;

CREATE TABLE public.session
(
  id_session integer NOT NULL DEFAULT nextval('session_id_session_seq'::regclass),
  session uuid,
  id_user integer,
  id_company integer,
  CONSTRAINT session_pkey PRIMARY KEY (id_session)
)
WITH (
  OIDS=FALSE
);
