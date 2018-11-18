-- Table: public.quotation_users

-- DROP TABLE public.quotation_users;

CREATE TABLE public.quotation_users
(
  id_user integer,
  id_quotation integer,
  cost numeric(32,6)
)
WITH (
  OIDS=FALSE
);

-- Index: public.quotation_users_id_user_id_quotation_uindex

-- DROP INDEX public.quotation_users_id_user_id_quotation_uindex;

CREATE UNIQUE INDEX quotation_users_id_user_id_quotation_uindex
  ON public.quotation_users
  USING btree
  (id_user, id_quotation);

