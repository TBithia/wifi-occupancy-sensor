/*
Items in lease table
-Expiration time of current lease
-Mac Address of leaseholder
-IP Addres that is being leased
-Host name, if supplied
*/

create table dhcp_log (
	expir_ts text not null,
	mac_address text not null,
	ip text,
	host_name text
	);