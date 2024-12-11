CREATE OR REPLACE FUNCTION calculate_leaderboard(
    start_date DATE,
    end_date DATE,
    filter_type VARCHAR
)
RETURNS TABLE (username VARCHAR, value NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        auth_user.username,
        CASE
            WHEN filter_type = 'distance' THEN COALESCE(SUM(runningapp_activity.distance), 0)
            WHEN filter_type = 'time' THEN COALESCE(SUM(EXTRACT(EPOCH FROM runningapp_activity.duration)), 0)
            WHEN filter_type = 'activities' THEN COALESCE(COUNT(runningapp_activity.id), 0)
        END AS value
    FROM 
        auth_user
    LEFT JOIN 
        runningapp_activity ON auth_user.id = runningapp_activity.user_id
    WHERE 
        (runningapp_activity.date >= start_date OR start_date IS NULL) AND
        (runningapp_activity.date <= end_date OR end_date IS NULL)
    GROUP BY 
        auth_user.username
    ORDER BY 
        value DESC;
END;
$$
 LANGUAGE plpgsql;