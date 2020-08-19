--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actors; Type: TABLE; Schema: public; Owner: ommi
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying,
    age integer,
    gender character varying(15)
);


ALTER TABLE public.actors OWNER TO ommi;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: ommi
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO ommi;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ommi
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ommi
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ommi;

--
-- Name: movie_cast; Type: TABLE; Schema: public; Owner: ommi
--

CREATE TABLE public.movie_cast (
    id integer NOT NULL,
    actor_id integer NOT NULL,
    movie_id integer NOT NULL
);


ALTER TABLE public.movie_cast OWNER TO ommi;

--
-- Name: movie_cast_id_seq; Type: SEQUENCE; Schema: public; Owner: ommi
--

CREATE SEQUENCE public.movie_cast_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movie_cast_id_seq OWNER TO ommi;

--
-- Name: movie_cast_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ommi
--

ALTER SEQUENCE public.movie_cast_id_seq OWNED BY public.movie_cast.id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: ommi
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying,
    release_date date
);


ALTER TABLE public.movies OWNER TO ommi;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: ommi
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO ommi;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ommi
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movie_cast id; Type: DEFAULT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.movie_cast ALTER COLUMN id SET DEFAULT nextval('public.movie_cast_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: ommi
--

COPY public.actors (id, name, age, gender) FROM stdin;
1	Harrison Ford	78	Male
2	Russell Crowe	53	Male
3	Lucy Liu	51	Female
4	Emma Watson	30	Female
5	Samuel L. Jackson	71	Male
6	Lynda Carter	69	Female
7	Ian McKellen	81	Male
8	Jodie Foster	57	Female
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: ommi
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: movie_cast; Type: TABLE DATA; Schema: public; Owner: ommi
--

COPY public.movie_cast (id, actor_id, movie_id) FROM stdin;
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: ommi
--

COPY public.movies (id, title, release_date) FROM stdin;
1	The Dark Knight	2008-07-14
2	Krull	1983-07-29
3	Pulp Fiction	1994-10-14
4	Little Women	2019-12-07
5	the silence of the lambs	1991-01-30
6	Kill Bill: Volume 1	2003-11-28
7	Last Action Hero	1993-06-18
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ommi
--

SELECT pg_catalog.setval('public.actors_id_seq', 8, true);


--
-- Name: movie_cast_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ommi
--

SELECT pg_catalog.setval('public.movie_cast_id_seq', 1, false);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ommi
--

SELECT pg_catalog.setval('public.movies_id_seq', 7, true);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: movie_cast movie_cast_pkey; Type: CONSTRAINT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.movie_cast
    ADD CONSTRAINT movie_cast_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: movie_cast movie_cast_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.movie_cast
    ADD CONSTRAINT movie_cast_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id);


--
-- Name: movie_cast movie_cast_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ommi
--

ALTER TABLE ONLY public.movie_cast
    ADD CONSTRAINT movie_cast_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


--
-- PostgreSQL database dump complete
--

