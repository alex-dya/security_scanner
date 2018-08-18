--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Debian 10.4-2.pgdg90+1)
-- Dumped by pg_dump version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.task_setting DROP CONSTRAINT task_setting_fk2;
ALTER TABLE ONLY public.task_setting DROP CONSTRAINT task_setting_fk;
ALTER TABLE ONLY public.task_result DROP CONSTRAINT task_result_fk;
ALTER TABLE ONLY public.task_result DROP CONSTRAINT task_fk;
ALTER TABLE ONLY public.task DROP CONSTRAINT task_fk;
ALTER TABLE ONLY public.scan_profile DROP CONSTRAINT scan_profile_fk;
ALTER TABLE ONLY public.profile_setting DROP CONSTRAINT profile_setting_fk;
ALTER TABLE ONLY public.host_result DROP CONSTRAINT host_result_fk;
ALTER TABLE ONLY public.control_result DROP CONSTRAINT control_result_fk;
ALTER TABLE ONLY public.account_credential DROP CONSTRAINT account_credential_owner_id_fkey;
DROP INDEX public.ix_user_username;
DROP INDEX public.ix_user_email;
DROP INDEX public.ix_task_name;
DROP INDEX public.ix_profile_setting_profile_id;
DROP INDEX public.ix_control_number;
DROP INDEX public.ix_control_language;
DROP INDEX public.ix_account_credential_username;
DROP INDEX public.ix_account_credential_owner_id;
DROP INDEX public.ix_account_credential_name;
ALTER TABLE ONLY public."user" DROP CONSTRAINT user_pkey;
ALTER TABLE ONLY public.task DROP CONSTRAINT task_uniq;
ALTER TABLE ONLY public.task_setting DROP CONSTRAINT task_setting_uniq;
ALTER TABLE ONLY public.task_setting DROP CONSTRAINT task_setting_pkey;
ALTER TABLE ONLY public.task_result DROP CONSTRAINT task_result_pkey;
ALTER TABLE ONLY public.task DROP CONSTRAINT task_pkey;
ALTER TABLE ONLY public.scan_profile DROP CONSTRAINT scan_profile_uniq;
ALTER TABLE ONLY public.scan_profile DROP CONSTRAINT scan_profile_pkey;
ALTER TABLE ONLY public.profile_setting DROP CONSTRAINT profile_setting_uniq;
ALTER TABLE ONLY public.profile_setting DROP CONSTRAINT profile_setting_pkey;
ALTER TABLE ONLY public.host_result DROP CONSTRAINT host_result_pkey;
ALTER TABLE ONLY public.control_result DROP CONSTRAINT control_result_pkey;
ALTER TABLE ONLY public.control DROP CONSTRAINT control_pkey;
ALTER TABLE ONLY public.celery_tasksetmeta DROP CONSTRAINT celery_tasksetmeta_taskset_id_key;
ALTER TABLE ONLY public.celery_tasksetmeta DROP CONSTRAINT celery_tasksetmeta_pkey;
ALTER TABLE ONLY public.celery_taskmeta DROP CONSTRAINT celery_taskmeta_task_id_key;
ALTER TABLE ONLY public.celery_taskmeta DROP CONSTRAINT celery_taskmeta_pkey;
ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
ALTER TABLE ONLY public.account_credential DROP CONSTRAINT account_credential_pkey;
ALTER TABLE ONLY public.account_credential DROP CONSTRAINT account_cred_uniq;
ALTER TABLE public."user" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.task_setting ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.task_result ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.task ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.scan_profile ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.profile_setting ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.host_result ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.control_result ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.control ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.account_credential ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.user_id_seq;
DROP TABLE public."user";
DROP SEQUENCE public.taskset_id_sequence;
DROP SEQUENCE public.task_setting_id_seq;
DROP TABLE public.task_setting;
DROP SEQUENCE public.task_result_id_seq;
DROP TABLE public.task_result;
DROP SEQUENCE public.task_id_sequence;
DROP SEQUENCE public.task_id_seq;
DROP TABLE public.task;
DROP SEQUENCE public.scan_profile_id_seq;
DROP TABLE public.scan_profile;
DROP SEQUENCE public.profile_setting_id_seq;
DROP TABLE public.profile_setting;
DROP SEQUENCE public.host_result_id_seq;
DROP TABLE public.host_result;
DROP SEQUENCE public.control_result_id_seq;
DROP TABLE public.control_result;
DROP SEQUENCE public.control_id_seq;
DROP TABLE public.control;
DROP TABLE public.celery_tasksetmeta;
DROP TABLE public.celery_taskmeta;
DROP TABLE public.alembic_version;
DROP SEQUENCE public.account_credential_id_seq;
DROP TABLE public.account_credential;
DROP TYPE public.taskstatus;
DROP TYPE public.controlstatus;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: controlstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.controlstatus AS ENUM (
    'NotChecked',
    'Compliance',
    'NotCompliance',
    'NotApplicable',
    'Error'
);


ALTER TYPE public.controlstatus OWNER TO postgres;

--
-- Name: taskstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.taskstatus AS ENUM (
    'Idle',
    'Wait',
    'Running'
);


ALTER TYPE public.taskstatus OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account_credential; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_credential (
    id integer NOT NULL,
    username character varying(64),
    password character varying(128),
    owner_id integer NOT NULL,
    name character varying(64)
);


ALTER TABLE public.account_credential OWNER TO postgres;

--
-- Name: account_credential_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_credential_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_credential_id_seq OWNER TO postgres;

--
-- Name: account_credential_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_credential_id_seq OWNED BY public.account_credential.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: celery_taskmeta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.celery_taskmeta (
    id integer NOT NULL,
    task_id character varying(155),
    status character varying(50),
    result bytea,
    date_done timestamp without time zone,
    traceback text
);


ALTER TABLE public.celery_taskmeta OWNER TO postgres;

--
-- Name: celery_tasksetmeta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.celery_tasksetmeta (
    id integer NOT NULL,
    taskset_id character varying(155),
    result bytea,
    date_done timestamp without time zone
);


ALTER TABLE public.celery_tasksetmeta OWNER TO postgres;

--
-- Name: control; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.control (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    description character varying(2048) NOT NULL,
    language character varying(4) DEFAULT 'en'::character varying,
    number integer
);


ALTER TABLE public.control OWNER TO postgres;

--
-- Name: control_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.control_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.control_id_seq OWNER TO postgres;

--
-- Name: control_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.control_id_seq OWNED BY public.control.id;


--
-- Name: control_result; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.control_result (
    id integer NOT NULL,
    status public.controlstatus NOT NULL,
    result character varying,
    control_number integer NOT NULL,
    host_result_id integer NOT NULL
);


ALTER TABLE public.control_result OWNER TO postgres;

--
-- Name: control_result_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.control_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.control_result_id_seq OWNER TO postgres;

--
-- Name: control_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.control_result_id_seq OWNED BY public.control_result.id;


--
-- Name: host_result; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.host_result (
    id integer NOT NULL,
    task_id integer NOT NULL,
    config character varying,
    hostname character varying
);


ALTER TABLE public.host_result OWNER TO postgres;

--
-- Name: host_result_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.host_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.host_result_id_seq OWNER TO postgres;

--
-- Name: host_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.host_result_id_seq OWNED BY public.host_result.id;


--
-- Name: profile_setting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profile_setting (
    id integer NOT NULL,
    transport character varying NOT NULL,
    setting character varying NOT NULL,
    value character varying NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.profile_setting OWNER TO postgres;

--
-- Name: profile_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.profile_setting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.profile_setting_id_seq OWNER TO postgres;

--
-- Name: profile_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.profile_setting_id_seq OWNED BY public.profile_setting.id;


--
-- Name: scan_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scan_profile (
    id integer NOT NULL,
    name character varying,
    owner_id integer NOT NULL
);


ALTER TABLE public.scan_profile OWNER TO postgres;

--
-- Name: scan_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.scan_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.scan_profile_id_seq OWNER TO postgres;

--
-- Name: scan_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.scan_profile_id_seq OWNED BY public.scan_profile.id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task (
    id integer NOT NULL,
    name character varying(64),
    owner_id integer NOT NULL,
    status public.taskstatus NOT NULL,
    uid character varying(128)
);


ALTER TABLE public.task OWNER TO postgres;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_id_seq OWNER TO postgres;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: task_id_sequence; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_id_sequence OWNER TO postgres;

--
-- Name: task_result; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_result (
    id integer NOT NULL,
    task_id integer NOT NULL,
    started timestamp without time zone DEFAULT now(),
    finished timestamp without time zone,
    owner_id integer NOT NULL
);


ALTER TABLE public.task_result OWNER TO postgres;

--
-- Name: task_result_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_result_id_seq OWNER TO postgres;

--
-- Name: task_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_result_id_seq OWNED BY public.task_result.id;


--
-- Name: task_setting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_setting (
    id integer NOT NULL,
    hostname character varying(128),
    profile_id integer NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.task_setting OWNER TO postgres;

--
-- Name: task_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_setting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_setting_id_seq OWNER TO postgres;

--
-- Name: task_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_setting_id_seq OWNED BY public.task_setting.id;


--
-- Name: taskset_id_sequence; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taskset_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taskset_id_sequence OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(64),
    email character varying(128),
    password_hash character varying(128)
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: account_credential id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credential ALTER COLUMN id SET DEFAULT nextval('public.account_credential_id_seq'::regclass);


--
-- Name: control id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.control ALTER COLUMN id SET DEFAULT nextval('public.control_id_seq'::regclass);


--
-- Name: control_result id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.control_result ALTER COLUMN id SET DEFAULT nextval('public.control_result_id_seq'::regclass);


--
-- Name: host_result id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.host_result ALTER COLUMN id SET DEFAULT nextval('public.host_result_id_seq'::regclass);


--
-- Name: profile_setting id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile_setting ALTER COLUMN id SET DEFAULT nextval('public.profile_setting_id_seq'::regclass);


--
-- Name: scan_profile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scan_profile ALTER COLUMN id SET DEFAULT nextval('public.scan_profile_id_seq'::regclass);


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Name: task_result id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_result ALTER COLUMN id SET DEFAULT nextval('public.task_result_id_seq'::regclass);


--
-- Name: task_setting id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_setting ALTER COLUMN id SET DEFAULT nextval('public.task_setting_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: account_credential account_cred_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credential
    ADD CONSTRAINT account_cred_uniq UNIQUE (name, owner_id);


--
-- Name: account_credential account_credential_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credential
    ADD CONSTRAINT account_credential_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: celery_taskmeta celery_taskmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.celery_taskmeta
    ADD CONSTRAINT celery_taskmeta_pkey PRIMARY KEY (id);


--
-- Name: celery_taskmeta celery_taskmeta_task_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.celery_taskmeta
    ADD CONSTRAINT celery_taskmeta_task_id_key UNIQUE (task_id);


--
-- Name: celery_tasksetmeta celery_tasksetmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.celery_tasksetmeta
    ADD CONSTRAINT celery_tasksetmeta_pkey PRIMARY KEY (id);


--
-- Name: celery_tasksetmeta celery_tasksetmeta_taskset_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.celery_tasksetmeta
    ADD CONSTRAINT celery_tasksetmeta_taskset_id_key UNIQUE (taskset_id);


--
-- Name: control control_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.control
    ADD CONSTRAINT control_pkey PRIMARY KEY (id);


--
-- Name: control_result control_result_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.control_result
    ADD CONSTRAINT control_result_pkey PRIMARY KEY (id);


--
-- Name: host_result host_result_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.host_result
    ADD CONSTRAINT host_result_pkey PRIMARY KEY (id);


--
-- Name: profile_setting profile_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile_setting
    ADD CONSTRAINT profile_setting_pkey PRIMARY KEY (id);


--
-- Name: profile_setting profile_setting_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile_setting
    ADD CONSTRAINT profile_setting_uniq UNIQUE (transport, setting, profile_id);


--
-- Name: scan_profile scan_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scan_profile
    ADD CONSTRAINT scan_profile_pkey PRIMARY KEY (id);


--
-- Name: scan_profile scan_profile_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scan_profile
    ADD CONSTRAINT scan_profile_uniq UNIQUE (name, owner_id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- Name: task_result task_result_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_result
    ADD CONSTRAINT task_result_pkey PRIMARY KEY (id);


--
-- Name: task_setting task_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_setting
    ADD CONSTRAINT task_setting_pkey PRIMARY KEY (id);


--
-- Name: task_setting task_setting_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_setting
    ADD CONSTRAINT task_setting_uniq UNIQUE (hostname, profile_id, task_id);


--
-- Name: task task_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_uniq UNIQUE (name, owner_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_account_credential_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_account_credential_name ON public.account_credential USING btree (name);


--
-- Name: ix_account_credential_owner_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_account_credential_owner_id ON public.account_credential USING btree (owner_id);


--
-- Name: ix_account_credential_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_account_credential_username ON public.account_credential USING btree (username);


--
-- Name: ix_control_language; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_control_language ON public.control USING btree (language);


--
-- Name: ix_control_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_control_number ON public.control USING btree (number);


--
-- Name: ix_profile_setting_profile_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_profile_setting_profile_id ON public.profile_setting USING btree (profile_id);


--
-- Name: ix_task_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_task_name ON public.task USING btree (name);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_username ON public."user" USING btree (username);


--
-- Name: account_credential account_credential_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credential
    ADD CONSTRAINT account_credential_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- Name: control_result control_result_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.control_result
    ADD CONSTRAINT control_result_fk FOREIGN KEY (host_result_id) REFERENCES public.host_result(id) ON DELETE CASCADE;


--
-- Name: host_result host_result_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.host_result
    ADD CONSTRAINT host_result_fk FOREIGN KEY (task_id) REFERENCES public.task_result(id) ON DELETE CASCADE;


--
-- Name: profile_setting profile_setting_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile_setting
    ADD CONSTRAINT profile_setting_fk FOREIGN KEY (profile_id) REFERENCES public.scan_profile(id) ON DELETE CASCADE;


--
-- Name: scan_profile scan_profile_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scan_profile
    ADD CONSTRAINT scan_profile_fk FOREIGN KEY (owner_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: task task_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_fk FOREIGN KEY (owner_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: task_result task_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_result
    ADD CONSTRAINT task_fk FOREIGN KEY (owner_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: task_result task_result_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_result
    ADD CONSTRAINT task_result_fk FOREIGN KEY (task_id) REFERENCES public.task(id) ON DELETE SET NULL;


--
-- Name: task_setting task_setting_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_setting
    ADD CONSTRAINT task_setting_fk FOREIGN KEY (profile_id) REFERENCES public.scan_profile(id) ON DELETE SET NULL;


--
-- Name: task_setting task_setting_fk2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_setting
    ADD CONSTRAINT task_setting_fk2 FOREIGN KEY (task_id) REFERENCES public.task(id) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

