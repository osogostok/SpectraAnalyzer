DROP TABLE IF EXISTS table_spectr;

CREATE TABLE IF NOT EXISTS table_spectr (
    id SERIAL PRIMARY KEY,
    name_file VARCHAR(255),
    type_spectr VARCHAR(8),
    date TIMESTAMP
);

CREATE OR REPLACE FUNCTION fun_check_exist_file()
    RETURNS TRIGGER
    AS $$ 
    BEGIN
        IF (SELECT name_file
        FROM table_spectr
        WHERE name_file = NEW.name_file) IS NOT NULL THEN
            RETURN OLD;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_exist_file
BEFORE INSERT ON table_spectr FOR EACH ROW EXECUTE FUNCTION fun_check_exist_file();

CREATE OR REPLACE FUNCTION fun_add_date()
    RETURNS TRIGGER
    AS $$ 
    BEGIN
        IF NEW.name_file LIKE '%.txt' THEN
            NEW.type_spectr := 'NMR';
        ELSIF NEW.name_file LIKE '%.xlsx' THEN
            NEW.type_spectr := 'IR';
        END IF;
        NEW.date := CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_add_date
BEFORE INSERT ON table_spectr FOR EACH ROW EXECUTE FUNCTION fun_add_date();


