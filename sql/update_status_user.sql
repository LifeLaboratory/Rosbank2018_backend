CREATE OR REPLACE FUNCTION update_status_user()
  RETURNS TRIGGER AS  $$
DECLARE
  sun text;
  sum_user numeric(32, 6);
BEGIN
  sun = (select status_pack from users where id_user = new.id_user);
  sum_user = (select sum((cost-cost_bank) * count_send) from history_billing where id_user = new.id_user);
  if sum_user >= 100 then
    update users
      set status_pack = 'Премиум'
    where id_user = new.id_user;
  end if;

  if sum_user < 100 and (SELECT (date_trunc('MONTH', current_date) + INTERVAL '1 MONTH - 1 day')::DATE) = current_date then
    update users
      set status_pack = 'Стандарт'
    where id_user = new.id_user;
  end if;
  return new;
END;
$$ LANGUAGE 'plpgsql';
