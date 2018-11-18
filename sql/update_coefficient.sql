CREATE OR REPLACE FUNCTION update_coefficient_user()
  RETURNS TRIGGER AS  $$
BEGIN
  if new.status_pack = 'Премиум' and new.status_pack <> old.status_pack then
    new.pack_standart = 0.005;
  end if;

  if new.status_pack = 'Стандарт' and new.status_pack <> old.status_pack then
    new.pack_standart = 0.05;
  end if;

  if new.rating <> old.rating or new.pack_standart <> old.pack_standart then
    new.pack = new.rating + new.pack_standart;
  end if;
  return new;
END;
$$ LANGUAGE 'plpgsql';
