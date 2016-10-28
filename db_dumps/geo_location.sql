--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: geo_location; Type: TABLE; Schema: public; Owner: hera_test; Tablespace: 
--

CREATE TABLE geo_location (
    station_name character varying(64) NOT NULL,
    station_number integer,
    future_station_number integer,
    datum character varying(64),
    tile character varying(64),
    northing double precision,
    easting double precision,
    elevation double precision
);


ALTER TABLE geo_location OWNER TO hera_test;

--
-- Data for Name: geo_location; Type: TABLE DATA; Schema: public; Owner: hera_test
--

COPY geo_location (station_name, station_number, future_station_number, datum, tile, northing, easting, elevation) FROM stdin;
0	80	0	WGS84	34J	540901.599999999977	6601070.74000000022	1052.63000000000011
1	104	1	WGS84	34J	540916.199999999953	6601070.74000000022	1052.61999999999989
11	64	11	WGS84	34J	540894.300000000047	6601083.37999999989	1052.48000000000002
12	53	12	WGS84	34J	540908.900000000023	6601083.37999999989	1052.41000000000008
13	31	13	WGS84	34J	540923.5	6601083.37999999989	1052.34999999999991
14	65	14	WGS84	34J	540938.099999999977	6601083.37999999989	1052.49000000000001
2	96	2	WGS84	34J	540930.800000000047	6601070.74000000022	1052.6099999999999
23	88	23	WGS84	34J	540887	6601096.03000000026	1052.33999999999992
24	9	24	WGS84	34J	540901.599999999977	6601096.03000000026	1052.3599999999999
25	20	25	WGS84	34J	540916.199999999953	6601096.03000000026	1052.34999999999991
26	89	26	WGS84	34J	540930.800000000047	6601096.03000000026	1052.33999999999992
27	43	27	WGS84	34J	540945.400000000023	6601096.03000000026	1052.44000000000005
37	105	37	WGS84	34J	540894.300000000047	6601108.66999999993	1052.25999999999999
38	22	38	WGS84	34J	540908.900000000023	6601108.66999999993	1052.25
39	81	39	WGS84	34J	540923.5	6601108.66999999993	1052.22000000000003
40	10	40	WGS84	34J	540938.099999999977	6601108.66999999993	1052.24000000000001
52	72	52	WGS84	34J	540901.599999999977	6601121.3200000003	1052.09999999999991
53	112	53	WGS84	34J	540916.199999999953	6601121.3200000003	1052.06999999999994
54	97	54	WGS84	34J	540930.800000000047	6601121.3200000003	1052.07999999999993
PH00	44	-1	WGS84	34J	541018.400000000023	6601070.70999999996	1052.57999999999993
PH01	14	-1	WGS84	34J	541033	6601070.70999999996	1052.50999999999999
PH02	86	-1	WGS84	34J	541047.599999999977	6601070.70999999996	1052.65000000000009
PH11	69	-1	WGS84	34J	541011.099999999977	6601083.36000000034	1052.40000000000009
PH12	40	-1	WGS84	34J	541025.699999999953	6601083.36000000034	1052.42000000000007
PH13	101	-1	WGS84	34J	541040.300000000047	6601083.36000000034	1052.45000000000005
PH14	102	-1	WGS84	34J	541054.900000000023	6601083.36000000034	1052.5
PH23	125	-1	WGS84	34J	541003.800000000047	6601096	1052.34999999999991
PH24	84	-1	WGS84	34J	541018.400000000023	6601096	1052.26999999999998
PH25	100	-1	WGS84	34J	541033	6601096	1052.28999999999996
PH26	85	-1	WGS84	34J	541047.599999999977	6601096	1052.27999999999997
PH27	54	-1	WGS84	34J	541062.199999999953	6601096	1052.31999999999994
PH37	17	-1	WGS84	34J	541011.099999999977	6601108.63999999966	1052.19000000000005
PH38	68	-1	WGS84	34J	541025.699999999953	6601108.63999999966	1052.26999999999998
PH39	62	-1	WGS84	34J	541040.300000000047	6601108.63999999966	1052.15000000000009
PH40	0	-1	WGS84	34J	541054.900000000023	6601108.63999999966	1052.21000000000004
PH52	2	-1	WGS84	34J	541018.400000000023	6601121.29000000004	1052.03999999999996
PH53	21	-1	WGS84	34J	541033	6601121.29000000004	1052.05999999999995
PH54	45	-1	WGS84	34J	541047.599999999977	6601121.29000000004	1052.03999999999996
PI1	61	-1	WGS84	34J	541025.459999999963	6601297.98000000045	1050.46000000000004
PI10	70	-1	WGS84	34J	541051.489999999991	6601269.6799999997	1050.8599999999999
PI11	56	-1	WGS84	34J	541062.699999999953	6601264.29999999981	1051
PI12	71	-1	WGS84	34J	541066.530000000028	6601256.15000000037	1051.00999999999999
PI13	59	-1	WGS84	34J	541075.189999999944	6601248.00999999978	1051.13000000000011
PI14	23	-1	WGS84	34J	541070.589999999967	6601238.91000000015	1051.05999999999995
PI15	50	-1	WGS84	34J	541080.709999999963	6601233.80999999959	1051.15000000000009
PI16	38	-1	WGS84	34J	541065.709999999963	6601227.86000000034	1051.16000000000008
PI17	26	-1	WGS84	34J	541064.079999999958	6601223.65000000037	1051.28999999999996
PI18	87	-1	WGS84	34J	541047.599999999977	6601218.44000000041	1051.20000000000005
PI19	103	-1	WGS84	34J	541048.010000000009	6601210.08999999985	1051.42000000000007
PI2	63	-1	WGS84	34J	541014.050000000047	6601293.37000000011	1050.67000000000007
PI20	42	-1	WGS84	34J	541024.569999999949	6601194.45000000019	1051.34999999999991
PI21	15	-1	WGS84	34J	541014.75	6601188.30999999959	1051.43000000000006
PI22	99	-1	WGS84	34J	540989.199999999953	6601197.15000000037	1051.34999999999991
PI23	1	-1	WGS84	34J	541004.199999999953	6601202.08999999985	1051.41000000000008
PI24	47	-1	WGS84	34J	540991.939999999944	6601208.5	1051.20000000000005
PI25	83	-1	WGS84	34J	540998.569999999949	6601212.70000000019	1051.31999999999994
PI26	37	-1	WGS84	34J	540982.910000000033	6601214.54999999981	1051.15000000000009
PI27	4	-1	WGS84	34J	540981.560000000056	6601219.62999999989	1051.1099999999999
PI28	90	-1	WGS84	34J	540978.849999999977	6601232.05999999959	1051.16000000000008
PI29	82	-1	WGS84	34J	540979.689999999944	6601237.61000000034	1051.1099999999999
PI3	67	-1	WGS84	34J	541012.140000000014	6601285.50999999978	1050.58999999999992
PI30	98	-1	WGS84	34J	540974.050000000047	6601239.30999999959	1051
PI31	74	-1	WGS84	34J	540986.5	6601243.03000000026	1051.04999999999995
PI32	106	-1	WGS84	34J	540982.979999999981	6601250.36000000034	1050.82999999999993
PI33	122	-1	WGS84	34J	540926.630000000005	6601277.5	1050.52999999999997
PI34	123	-1	WGS84	34J	540880.689999999944	6601256.70000000019	1050.68000000000006
PI35	124	-1	WGS84	34J	540877.880000000005	6601235.90000000037	1050.86999999999989
PI36	-1	-1	WGS84	34J	540875.069999999949	6601215.09999999963	1051.04999999999995
PI37	126	-1	WGS84	34J	540872.25	6601194.29999999981	1051.25
PI38	127	-1	WGS84	34J	540869.439999999944	6601173.5	1051.45000000000005
PI39	41	-1	WGS84	34J	540930.800000000047	6601167.86000000034	1051.52999999999997
PI4	58	-1	WGS84	34J	541018.800000000047	6601279.5	1050.6099999999999
PI40	16	-1	WGS84	34J	540981.900000000023	6601133.9299999997	1051.94000000000005
PI41	13	-1	WGS84	34J	541041.839999999967	6601158	1051.79999999999995
PI42	46	-1	WGS84	34J	541091.400000000023	6601121.29000000004	1052.03999999999996
PI43	114	-1	WGS84	34J	541142.5	6601083.36000000034	1052.44000000000005
PI44	115	-1	WGS84	34J	541149.800000000047	6601146.58000000007	1051.86999999999989
PI45	116	-1	WGS84	34J	541103.180000000051	6601171.90000000037	1051.61999999999989
PI46	57	-1	WGS84	34J	541098.699999999953	6601184.50999999978	1051.59999999999991
PI47	117	-1	WGS84	34J	541100.709999999963	6601192.70000000019	1051.36999999999989
PI48	118	-1	WGS84	34J	541100.069999999949	6601213.5	1051.20000000000005
PI49	119	-1	WGS84	34J	541098.189999999944	6601234.29999999981	1050.99000000000001
PI5	3	-1	WGS84	34J	541029.510000000009	6601276.86000000034	1050.75
PI50	120	-1	WGS84	34J	541095.680000000051	6601259.09999999963	1050.82999999999993
PI6	73	-1	WGS84	34J	541035.739999999991	6601285.12000000011	1050.72000000000003
PI7	66	-1	WGS84	34J	541043.319999999949	6601284.88999999966	1050.58999999999992
PI8	121	-1	WGS84	34J	541042.880000000005	6601279.90000000037	1050.6099999999999
PI9	49	-1	WGS84	34J	541056.5	6601280.54000000004	1050.70000000000005
PPA10	28	-1	WGS84	34J	541024.089999999967	6601156.75	1051.65000000000009
PPA12	34	-1	WGS84	34J	541054.130000000005	6601156.80999999959	1051.70000000000005
PPA14	51	-1	WGS84	34J	541084.089999999967	6601156.86000000034	1051.74000000000001
PPA6	19	-1	WGS84	34J	540964.089999999967	6601156.78000000026	1051.68000000000006
PPA8	29	-1	WGS84	34J	540994.089999999967	6601156.8200000003	1051.66000000000008
PPE10	93	-1	WGS84	34J	541024.109999999986	6601140.79999999981	1051.81999999999994
PPE12	94	-1	WGS84	34J	541054.099999999977	6601140.8200000003	1051.86999999999989
PPE14	95	-1	WGS84	34J	541084.150000000023	6601140.83000000007	1051.84999999999991
PPE6	91	-1	WGS84	34J	540964.109999999986	6601140.80999999959	1051.8599999999999
PPE8	92	-1	WGS84	34J	540994.130000000005	6601140.80999999959	1051.80999999999995
SA11	55	-1	WGS84	34J	541039.089999999967	6601156.75	1051.70000000000005
SA13	27	-1	WGS84	34J	541069.130000000005	6601156.80999999959	1051.69000000000005
SA5	25	-1	WGS84	34J	540949.119999999995	6601156.75999999978	1051.69000000000005
SA7	48	-1	WGS84	34J	540979.089999999967	6601156.78000000026	1051.61999999999989
SA9	24	-1	WGS84	34J	541009.089999999967	6601156.8200000003	1051.66000000000008
SC10	77	-1	WGS84	34J	541024.109999999986	6601148.76999999955	1051.71000000000004
SC11	32	-1	WGS84	34J	541039.109999999986	6601148.76999999955	1051.83999999999992
SC12	78	-1	WGS84	34J	541054.079999999958	6601148.79999999981	1051.76999999999998
SC13	30	-1	WGS84	34J	541069.079999999958	6601148.79999999981	1051.80999999999995
SC14	79	-1	WGS84	34J	541084.109999999986	6601148.83999999985	1051.77999999999997
SC5	35	-1	WGS84	34J	540949.140000000014	6601148.76999999955	1051.77999999999997
SC6	75	-1	WGS84	34J	540964.109999999986	6601148.75	1051.73000000000002
SC7	18	-1	WGS84	34J	540979.109999999986	6601148.75	1051.72000000000003
SC8	76	-1	WGS84	34J	540994.130000000005	6601148.79999999981	1051.74000000000001
SC9	5	-1	WGS84	34J	541009.130000000005	6601148.79999999981	1051.72000000000003
SE11	7	-1	WGS84	34J	541039.109999999986	6601140.79999999981	1051.86999999999989
SE13	12	-1	WGS84	34J	541069.099999999977	6601140.8200000003	1051.79999999999995
SE5	33	-1	WGS84	34J	540949.130000000005	6601140.78000000026	1051.79999999999995
SE7	6	-1	WGS84	34J	540979.109999999986	6601140.80999999959	1051.81999999999994
SE9	52	-1	WGS84	34J	541009.130000000005	6601140.80999999959	1051.81999999999994
SG10	109	-1	WGS84	34J	541024.089999999967	6601132.83000000007	1051.8900000000001
SG11	60	-1	WGS84	34J	541039.089999999967	6601132.83000000007	1051.91000000000008
SG12	110	-1	WGS84	34J	541054.099999999977	6601132.83999999985	1051.93000000000006
SG13	39	-1	WGS84	34J	541069.099999999977	6601132.83999999985	1051.91000000000008
SG14	111	-1	WGS84	34J	541084.130000000005	6601132.83999999985	1051.90000000000009
SG5	8	-1	WGS84	34J	540949.119999999995	6601132.78000000026	1051.91000000000008
SG6	107	-1	WGS84	34J	540964.130000000005	6601132.80999999959	1051.96000000000004
SG7	11	-1	WGS84	34J	540979.130000000005	6601132.80999999959	1051.92000000000007
SG8	108	-1	WGS84	34J	540994.119999999995	6601132.83999999985	1051.8900000000001
SG9	36	-1	WGS84	34J	541009.119999999995	6601132.83999999985	1051.90000000000009
\.


--
-- Name: geo_location_pkey; Type: CONSTRAINT; Schema: public; Owner: hera_test; Tablespace: 
--

ALTER TABLE ONLY geo_location
    ADD CONSTRAINT geo_location_pkey PRIMARY KEY (station_name);


--
-- PostgreSQL database dump complete
--

