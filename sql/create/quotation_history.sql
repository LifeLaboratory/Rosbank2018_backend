-- Table: public.quotation_history

-- DROP TABLE public.quotation_history;

CREATE TABLE public.quotation_history
(
  id_quotation_to integer,
  id_quotation_from integer,
  cost numeric(32,6),
  name text,
  coefficient_sales numeric(32,6),
  coefficient_purchare numeric(32,6),
  quant timestamp without time zone DEFAULT now()
)
WITH (
  OIDS=FALSE
);

-- Index: public.quotation_history_quant_index

-- DROP INDEX public.quotation_history_quant_index;

CREATE INDEX quotation_history_quant_index
  ON public.quotation_history
  USING btree
  (quant DESC);


-- Trigger: update_trade on public.quotation_history

-- DROP TRIGGER update_trade ON public.quotation_history;

CREATE TRIGGER update_trade
  AFTER INSERT
  ON public.quotation_history
  FOR EACH ROW
  EXECUTE PROCEDURE public.create_ts_partition();

