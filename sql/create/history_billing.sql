-- Table: public.history_billing

-- DROP TABLE public.history_billing;

CREATE TABLE public.history_billing
(
  id_user integer,
  id_quotation_from integer,
  id_quotation_to integer,
  cost numeric(32,6),
  cost_bank numeric(32,6),
  quant timestamp without time zone DEFAULT now(),
  id_history integer NOT NULL DEFAULT nextval('history_billing_id_history_seq'::regclass),
  coefficient numeric(32,6),
  name text,
  count_send numeric(32,6)
)
WITH (
  OIDS=FALSE
);

-- Trigger: update_status_user on public.history_billing

-- DROP TRIGGER update_status_user ON public.history_billing;

CREATE TRIGGER update_status_user
  AFTER INSERT
  ON public.history_billing
  FOR EACH ROW
  EXECUTE PROCEDURE public.update_status_user();

