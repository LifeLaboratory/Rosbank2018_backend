-- Table: public.quotation

-- DROP TABLE public.quotation;

CREATE TABLE public.quotation
(
  id_quotation integer NOT NULL DEFAULT nextval('"quotation_id_quotation _seq"'::regclass),
  name text
)
WITH (
  OIDS=FALSE
);
