CREATE OR REPLACE FUNCTION reset_stats()
RETURNS VOID AS $$
BEGIN
    TRUNCATE ciplay_stats;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION save_stats(_date DATE, _views BIGINT, _clicks BIGINT, _cost DECIMAL)
RETURNS INTEGER AS $$
DECLARE inserted_id INTEGER;
BEGIN
    IF EXISTS(SELECT stat_id FROM ciplay_stats WHERE date = _date) THEN
        UPDATE ciplay_stats SET
        cost = COALESCE(cost + _cost, cost, _cost),
        views = COALESCE(views + _views, views, _views),
        clicks = COALESCE(clicks + _clicks, clicks, _clicks)
        WHERE date = _date
        RETURNING stat_id INTO inserted_id;
    ELSE
        INSERT INTO ciplay_stats(date, views, clicks, cost) VALUES (_date, _views, _clicks, _cost)
        RETURNING stat_id INTO inserted_id;
    END IF;
    RETURN inserted_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_stats(from_date DATE, to_date DATE, sort_dir VARCHAR, sort_col VARCHAR)
RETURNS TABLE(
    date DATE,
    views BIGINT,
    clicks BIGINT,
    cost DECIMAL,
    cpc DECIMAL,
    cpm DECIMAL
) AS $$
BEGIN
    RETURN QUERY

        SELECT T.date, T.views, T.clicks, T.cost, T.cost/T.clicks AS cpc, T.cost*1000/T.views AS cpm
        FROM ciplay_stats AS T WHERE T.date BETWEEN from_date AND to_date
        ORDER BY
        CASE WHEN sort_dir = 'ASC' THEN
            CASE sort_col
                WHEN 'views' THEN T.views
                WHEN 'clicks' THEN T.clicks
                WHEN 'cost' THEN T.cost
                -- Cast to numeric type for Case to be able to work
                ELSE DATE_PART('day', T.date - '1970-01-01 00:00:00'::timestamp)
            END
            ELSE
                NULL
        END
        ASC,

        CASE WHEN sort_dir = 'DESC' THEN
            CASE sort_col
                WHEN 'views' THEN T.views
                WHEN 'clicks' THEN T.clicks
                WHEN 'cost' THEN T.cost
                -- Cast to numeric type for Case to be able to work
                ELSE DATE_PART('day', T.date - '1970-01-01 00:00:00'::timestamp)
            END
            ELSE
                NULL
        END
        DESC;
END;
$$ LANGUAGE plpgsql;



UPDATE ciplay_stats SET
cost = COALESCE(cost + 100, cost, 100),
views = COALESCE(views + 100, views, 100),
clicks = COALESCE(clicks + 100, clicks, 100)