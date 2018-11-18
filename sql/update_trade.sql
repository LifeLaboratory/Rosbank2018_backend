CREATE OR REPLACE FUNCTION create_ts_partition()
  RETURNS TRIGGER AS  $$
BEGIN
  update quotation_trade
   set cost = new.cost
  where id_quotation_from = new.id_quotation_from
    and id_quotation_to = new.id_quotation_to;
  return new;
END;
$$ LANGUAGE 'plpgsql';
