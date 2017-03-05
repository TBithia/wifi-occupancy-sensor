create table dhcp_log as(
	ts timestamp not null,
	dhcp_ack char not null,
	ip char,
	host_name char
);