create materialized view present_mac as (
	select mac 
	from mac_activity 
	where final_request_ts is null
);