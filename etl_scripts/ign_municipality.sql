CREATE OR REPLACE FUNCTION get_departament(code_muncipality TEXT, OUT result TEXT) AS $$
  BEGIN
    SELECT d.in1 INTO result
    FROM ign_municipios m, ign_departamentos d
    WHERE m.in1 = code_muncipality
    ORDER BY st_area(st_intersection(m.geom, d.geom)) DESC
    LIMIT 1;
    EXCEPTION
    WHEN OTHERS
      THEN
        result := SQLERRM;
  END;
$$
LANGUAGE 'plpgsql';