-- Table: public.quotation_trade

-- DROP TABLE public.quotation_trade;

CREATE TABLE public.quotation_trade
(
  id_quotation_to integer,
  id_quotation_from integer,
  cost numeric(32,6),
  name text,
  coefficient_sales numeric(32,6) DEFAULT 0.001,
  coefficient_purchare numeric(32,6) DEFAULT 0.001
)
WITH (
  OIDS=FALSE
);

-- Index: public.quotation_trade_id_quotation_to_id_quotation_from_uindex

-- DROP INDEX public.quotation_trade_id_quotation_to_id_quotation_from_uindex;

CREATE UNIQUE INDEX quotation_trade_id_quotation_to_id_quotation_from_uindex
  ON public.quotation_trade
  USING btree
  (id_quotation_from, id_quotation_to);

