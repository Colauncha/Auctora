--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+1)
-- Dumped by pg_dump version 16.4 (Debian 16.4-1.pgdg120+1)

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

--
-- Name: auctora_dev; Type: SCHEMA; Schema: -; Owner: iyanu
--

CREATE SCHEMA auctora_dev;


ALTER SCHEMA auctora_dev OWNER TO iyanu;

--
-- Name: auction_status; Type: TYPE; Schema: auctora_dev; Owner: iyanu
--

CREATE TYPE auctora_dev.auction_status AS ENUM (
    'ACTIVE',
    'COMPLETED',
    'CANCLED',
    'PENDING'
);


ALTER TYPE auctora_dev.auction_status OWNER TO iyanu;

--
-- Name: transaction_status; Type: TYPE; Schema: auctora_dev; Owner: iyanu
--

CREATE TYPE auctora_dev.transaction_status AS ENUM (
    'PENDING',
    'COMPLETED',
    'FAILED'
);


ALTER TYPE auctora_dev.transaction_status OWNER TO iyanu;

--
-- Name: transaction_types; Type: TYPE; Schema: auctora_dev; Owner: iyanu
--

CREATE TYPE auctora_dev.transaction_types AS ENUM (
    'FUNDING',
    'WITHDRAWAL',
    'CREDIT',
    'DEBIT'
);


ALTER TYPE auctora_dev.transaction_types OWNER TO iyanu;

--
-- Name: userroles; Type: TYPE; Schema: auctora_dev; Owner: iyanu
--

CREATE TYPE auctora_dev.userroles AS ENUM (
    'CLIENT',
    'ADMIN'
);


ALTER TYPE auctora_dev.userroles OWNER TO iyanu;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: auctora_dev; Owner: iyanu
--

CREATE TABLE auctora_dev.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE auctora_dev.alembic_version OWNER TO iyanu;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: auctora_dev; Owner: iyanu
--

COPY auctora_dev.alembic_version (version_num) FROM stdin;
582b687a4f7a
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: auctora_dev; Owner: iyanu
--

ALTER TABLE ONLY auctora_dev.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- PostgreSQL database dump complete
--

