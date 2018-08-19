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
-- Data for Name: account_credential; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_credential (id, username, password, owner_id, name) FROM stdin;
3	vmuser	P@ssw0rd	1	vmuser_P@ssw0rd
5	vmuser	vmuser	1	vmuser_P@ssw0rd1
6	vmuser	vmuser	2	vmuser_P@ssw0rd
7	test	test	1	test-test
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
36fde64c65aa
\.


--
-- Data for Name: celery_taskmeta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.celery_taskmeta (id, task_id, status, result, date_done, traceback) FROM stdin;
229	889b85fa-2122-45f8-ad1b-266d68a0bfe3	FAILURE	\\x80049585000000000000007d94288c086578635f74797065948c0e4174747269627574654572726f72948c0b6578635f6d657373616765948c396d6f64756c6520277363616e6e65722e636f6e74726f6c732720686173206e6f2061747472696275746520276765745f636f6e74726f6c73279485948c0a6578635f6d6f64756c65948c086275696c74696e7394752e	2018-08-12 17:51:54.452206	Traceback (most recent call last):\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/celery/app/trace.py", line 382, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File "/home/wolf/git/security_scanner/src/web/__init__.py", line 22, in __call__\n    return self.run(*args, **kwargs)\n  File "/home/wolf/git/security_scanner/src/web/functions.py", line 51, in run_scan\n    total = len(controls.get_controls())\nAttributeError: module 'scanner.controls' has no attribute 'get_controls'\n
237	7504efe0-67f2-4cc0-a064-5948f46ce504	SUCCESS	\N	2018-08-18 13:35:56.872606	\N
230	4642d63d-3cb7-4666-8a5c-2b6728d3a2dc	FAILURE	\\x8004959a000000000000007d94288c086578635f74797065948c1050726f6772616d6d696e674572726f72948c0b6578635f6d657373616765948c4628707379636f7067322e50726f6772616d6d696e674572726f72292063616e277420616461707420747970652027636f6c6c656374696f6e732e64656661756c7464696374279485948c0a6578635f6d6f64756c65948c0e73716c616c6368656d792e65786394752e	2018-08-12 17:53:11.423646	Traceback (most recent call last):\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1193, in _execute_context\n    context)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/default.py", line 509, in do_execute\n    cursor.execute(statement, parameters)\npsycopg2.ProgrammingError: can't adapt type 'collections.defaultdict'\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/celery/app/trace.py", line 382, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File "/home/wolf/git/security_scanner/src/web/__init__.py", line 22, in __call__\n    return self.run(*args, **kwargs)\n  File "/home/wolf/git/security_scanner/src/web/functions.py", line 67, in run_scan\n    **setting.profile.to_dict()\n  File "/home/wolf/git/security_scanner/src/web/models.py", line 97, in to_dict\n    for item in self.settings:\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/dynamic.py", line 241, in __iter__\n    sess = self.session\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/dynamic.py", line 233, in session\n    sess.flush()\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/session.py", line 2254, in flush\n    self._flush(objects)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/session.py", line 2380, in _flush\n    transaction.rollback(_capture_exception=True)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/util/langhelpers.py", line 66, in __exit__\n    compat.reraise(exc_type, exc_value, exc_tb)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 249, in reraise\n    raise value\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/session.py", line 2344, in _flush\n    flush_context.execute()\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/unitofwork.py", line 391, in execute\n    rec.execute(self)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/unitofwork.py", line 556, in execute\n    uow\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/persistence.py", line 181, in save_obj\n    mapper, table, insert)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/persistence.py", line 866, in _emit_insert_statements\n    execute(statement, params)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 948, in execute\n    return meth(self, multiparams, params)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/sql/elements.py", line 269, in _execute_on_connection\n    return connection._execute_clauseelement(self, multiparams, params)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1060, in _execute_clauseelement\n    compiled_sql, distilled_params\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1200, in _execute_context\n    context)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1413, in _handle_dbapi_exception\n    exc_info\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 265, in raise_from_cause\n    reraise(type(exception), exception, tb=exc_tb, cause=cause)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 248, in reraise\n    raise value.with_traceback(tb)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1193, in _execute_context\n    context)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/engine/default.py", line 509, in do_execute\n    cursor.execute(statement, parameters)\nsqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) can't adapt type 'collections.defaultdict' [SQL: 'INSERT INTO host_result (task_id, config, hostname) VALUES (%(task_id)s, %(config)s, %(hostname)s) RETURNING host_result.id'] [parameters: {'task_id': 81, 'config': defaultdict(<class 'dict'>, {'ssh': {'port': '22', 'username': 'vmuser', 'password': 'P@ssw0rd'}, 'unix': {'privilege_escalation': 'SudoLogon', 'root_password': ''}}), 'hostname': '192.168.56.10'}] (Background on this error at: http://sqlalche.me/e/f405)\n
234	2a87c474-5654-4ca6-8672-ebed8839530f	REVOKED	\\x80049561000000000000007d94288c086578635f74797065948c105461736b5265766f6b65644572726f72948c0b6578635f6d657373616765948c0a7465726d696e617465649485948c0a6578635f6d6f64756c65948c1163656c6572792e657863657074696f6e7394752e	2018-08-12 19:11:02.215925	\N
235	e3a72bca-47de-4cbe-972a-1c85ecbfa803	REVOKED	\\x80049561000000000000007d94288c086578635f74797065948c105461736b5265766f6b65644572726f72948c0b6578635f6d657373616765948c0a7465726d696e617465649485948c0a6578635f6d6f64756c65948c1163656c6572792e657863657074696f6e7394752e	2018-08-12 19:11:02.227751	\N
236	7a78e987-0cac-44d4-9036-a1170a69431a	PROGRESS	\\x8004951b000000000000007d94288c0763757272656e74944b0b8c05746f74616c944b0f752e	2018-08-12 19:11:11.965039	\N
233	568bfc73-df92-4e75-b4b4-9bc25d0f83b0	PROGRESS	\\x8004951b000000000000007d94288c0763757272656e74944b0a8c05746f74616c944b0f752e	2018-08-12 19:11:12.266482	\N
238	06a8547b-bc40-435e-a199-6f1a7ccd04f5	SUCCESS	\N	2018-08-18 14:09:28.832934	\N
231	4f6ceb72-4227-42c9-95e0-900038ae56c9	FAILURE	\\x80049581000000000000007d94288c086578635f74797065948c09547970654572726f72948c0b6578635f6d657373616765948c3a277461736b5f69642720697320616e20696e76616c6964206b6579776f726420617267756d656e7420666f7220436f6e74726f6c526573756c749485948c0a6578635f6d6f64756c65948c086275696c74696e7394752e	2018-08-12 17:54:12.928513	Traceback (most recent call last):\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/celery/app/trace.py", line 382, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File "/home/wolf/git/security_scanner/src/web/__init__.py", line 22, in __call__\n    return self.run(*args, **kwargs)\n  File "/home/wolf/git/security_scanner/src/web/functions.py", line 87, in run_scan\n    result=control.result\n  File "<string>", line 4, in __init__\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/state.py", line 417, in _initialize_instance\n    manager.dispatch.init_failure(self, args, kwargs)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/util/langhelpers.py", line 66, in __exit__\n    compat.reraise(exc_type, exc_value, exc_tb)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 249, in reraise\n    raise value\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/orm/state.py", line 414, in _initialize_instance\n    return manager.original_init(*mixed[1:], **kwargs)\n  File "/home/wolf/.venvs/security_scanner/lib/python3.6/site-packages/sqlalchemy/ext/declarative/base.py", line 699, in _declarative_constructor\n    (k, cls_.__name__))\nTypeError: 'task_id' is an invalid keyword argument for ControlResult\n
239	d32378c3-dbbe-439a-bd8c-f6a8c7577f37	SUCCESS	\N	2018-08-18 14:10:40.496865	\N
240	ba0916a3-f13a-4ca6-ac19-fe2b80d0c2e6	SUCCESS	\N	2018-08-18 14:10:53.851703	\N
241	66914b5f-7d2b-4b01-a478-d5d92bc81d0c	SUCCESS	\N	2018-08-18 14:34:16.067446	\N
242	1a2d72c9-9912-458d-861e-ce73f253e92c	SUCCESS	\N	2018-08-18 14:37:08.325879	\N
243	d1fa56f8-7dbe-4186-aff7-167b8a4df0bd	SUCCESS	\N	2018-08-18 14:37:46.553682	\N
232	631fcd57-d488-46ba-9297-177d3626f1a6	SUCCESS	\N	2018-08-12 17:58:03.838848	\N
244	dd5cf983-83cc-422f-a72d-246d905fc9fc	SUCCESS	\N	2018-08-18 14:38:00.457608	\N
245	8a305812-7130-47f0-b402-7f67729b2fba	SUCCESS	\N	2018-08-18 14:38:38.771133	\N
246	dd97a96c-76ed-41b2-928c-b22ac86e2008	SUCCESS	\N	2018-08-18 19:11:44.438406	\N
\.


--
-- Data for Name: celery_tasksetmeta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.celery_tasksetmeta (id, taskset_id, result, date_done) FROM stdin;
\.


--
-- Data for Name: control; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.control (id, name, description, language, number) FROM stdin;
7	Ensure mounting of forbidden filesystems is disabled	Removing support for unneeded filesystem types reduces the local attack surface of the server.	en	1
8	Удостоверьтесь, что мониторивани запрещенных файловых систем запрещено	Отключите поддержку ненужных типов файловых систем для того чтобы уменьшить площадь атаки на сервер.	ru	1
9	Ensure permissions on bootloader config are configured	The grub configuration file contains information on boot settings and passwords for unlocking boot options. The grub configuration is usually grub.conf, grub.cfg, or menu.lst stored in either /boot/grub or /boot/grub2. It is commonly symlinked as /etc/grub.conf as well. Setting the permissions to read and write for root only prevents non-root users from seeing the boot parameters or changing them. Non-root users who read the boot parameters may be able to identify weaknesses in security upon boot and be able to exploit them.	en	2
10	Удостоверьтесь, что разрешения на конфиг загрузчика настроены корректно	Конфигурационный файл содержит информацию о настройках загрузки и паролях для разблокировки опций загрузки. Настройки grub - grub.conf, grub.cfg, или menu.lst - обычно храняться либо в каталоге /boot/grub либо /boot/grub2. В основном, он является символической ссылкой на /etc/grub.conf. Настройте права доступа на чтение и запись только пользователю root, для предотвращения просмотра параметров загрузки или их изменения другими пользователями. Не-root пользователи, кто может читать параметры загрузки, могут быть способны обнаружить слабые места в защите во время загрузки системы и проэксплуатировать их	ru	2
11	Ensure separate partition exists for /var	The /var directory is used by daemons and other system services to temporarily store dynamic data. Some directories created by these processes may be world-writable.	en	3
12	Удостоверьтесь, что существует отдельный раздел диска для /var	Директория /var обычно используется демонами и другими службами для временного хранения изменяемых данных. Некоторые директории созданные этими процессами могут иметь права на запись для всех пользователей.	ru	3
13	Ensure nodev option set on /tmp partition	The nodev mount option specifies that the filesystem cannot contain special devices.	en	4
14	Опция nodev должна быть установлена на мониторивание раздела /tmp	Опция монтирования nodev указывает, что эта файловая система не может содержать специальных устройств	ru	4
15	Ensure root is the only UID 0 account	Any account with UID 0 has superuser privileges on the system. This access must be limited to only the default root account and only from the system console. Administrative access must be through an unprivileged account using an approved mechanism. Ensure access to the su command is restricted.	en	6
16	Пользователь root должен быть единственным пользователем с UID 0	Любой аккаунт с UID 0 имеет права суперпользователя на системе. Этот доступ должен быть ограничен единственным пользователем root в системе и только из системной консоли. Административный доступ для непривилегированных аккаунтов должен осуществляться только через надежные механизмы поднятия привелегий. Доступ для выполнения команды su должен быть ограничен	ru	6
17	Ensure bootloader password is set	Setting the boot loader password will require that anyone rebooting the system must enter a password before being able to set command line boot parameters. Requiring a boot password upon execution of the boot loader will prevent an unauthorized user from entering boot parameters or changing the boot partition. This prevents users from weakening security (e.g. turning off SELinux at boot time).	en	7
18	Установите пароль на загрузчик системы	Установка пароля на загрузчик системы требуется, чтобы любому пользователю, перезагружающему систему, необходимо было ввести пароль перед тем как получить доступ к настройкам параметров загрузочной командной строки. Требование пароля на загрузчике системы запрещает неавторизованному пользователю изменять параметры загрузки или загрузочный раздел. Это предотвратит ослабление защиты пользователем (например, отключение системы защиты SELinux во время загрузки системы).	ru	7
19	Ensure authentication required for single user mode	Single user mode is used for recovery when the system detects an issue during boot or by manual selection from the bootloader. Requiring authentication in single user mode prevents an unauthorized user from rebooting the system into single user to gain root privileges without credentials.	en	8
20	Включите аутентификацию для режима single user	Режим single user используется для восстановления, когда системы обнаружила неполадки во время загрузки, или при выборе этого режима в меню загрузчика. Требование аутентификации в режиме single user предотвращает неавторизованным пользователям доступ к режиму single user для получения привилегия root без запроса пароля.	ru	8
21	Ensure cron daemon is enabled	The cron daemon is used to execute batch jobs on the system. While there may not be user jobs that need to be run on the system, the system does have maintenance jobs that may include security monitoring that have to run, and cron is used to execute them.	en	9
22	Демон cron должен быть включен.	Демон cron используется для выполнения набора задач на системе по расписанию. Даже если нет пользовательских задач, которые необходимо выполнять на системе, самой системе необходимо поддерживать задачи, которые могут включать мониторинг безопасности. И cron используется для их выполнения.	ru	9
\.


--
-- Data for Name: control_result; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.control_result (id, status, result, control_number, host_result_id) FROM stdin;
123	NotCompliance	cramfs is not disabled\nfreevxfs is not disabled\njffs2 is not disabled\nhfs is not disabled\nhfsplus is not disabled\nsquashfs is not disabled\nudf is not disabled\nvfat is not disabled	1	15
124	NotCompliance	/boot/grub/grub.cfg root:root 444	2	15
125	NotCompliance	/tmp has been mounted on tmpfs\n/home has not been mounted on separate partition\n/var has not been mounted on separate partition\n/var/log has not been mounted on separate partition\n/var/log/audit has not been mounted on separate partition\n/var/tmp has not been mounted on separate partition	3	15
126	NotCompliance	/var/tmp has not been mounted on separated partition\n/home has not been mounted on separated partition\n/dev/shm has been mounted without options "noexec"\n/tmp has been mounted without options "noexec"	4	15
127	NotCompliance	There are 2 roots: ['root', 'toor']	6	15
128	NotCompliance	The password is not set up	7	15
129	Compliance	emergency.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""\nrescue.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""	8	15
130	Compliance	cron.service state is enabled	9	15
131	NotCompliance	cramfs is not disabled\nfreevxfs is not disabled\njffs2 is not disabled\nhfs is not disabled\nhfsplus is not disabled\nsquashfs is not disabled\nudf is not disabled\nvfat is not disabled	1	16
132	Compliance	/boot/grub2/grub.cfg root:root 600	2	16
133	NotCompliance	/home has been mounted on /dev/sda2\n/tmp has been mounted on /dev/sda2\n/var/log has been mounted on /dev/sda2\n/var/tmp has been mounted on /dev/sda2\n/var has not been mounted on separate partition\n/var/log/audit has not been mounted on separate partition	3	16
134	NotCompliance	/var/tmp has been mounted without options "nodev,nosuid,noexec"\n/home has been mounted without options "nodev"\n/dev/shm has been mounted without options "noexec"\n/tmp has been mounted without options "nodev,nosuid,noexec"	4	16
135	Compliance	There is only one root	6	16
136	NotCompliance	The password is not set up	7	16
137	Compliance	emergency.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --job-mode=fail --no-block default""\nrescue.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --job-mode=fail --no-block default""	8	16
138	Compliance	cron.service state is enabled	9	16
155	NotCompliance	cramfs is not disabled\nfreevxfs is not disabled\njffs2 is not disabled\nhfs is not disabled\nhfsplus is not disabled\nsquashfs is not disabled\nudf is not disabled\nvfat is not disabled	1	19
156	NotCompliance	/boot/grub/grub.cfg root:root 444	2	19
157	NotCompliance	/tmp has been mounted on tmpfs\n/home has not been mounted on separate partition\n/var has not been mounted on separate partition\n/var/log has not been mounted on separate partition\n/var/log/audit has not been mounted on separate partition\n/var/tmp has not been mounted on separate partition	3	19
158	NotCompliance	/var/tmp has not been mounted on separated partition\n/home has not been mounted on separated partition\n/dev/shm has been mounted without options "noexec"\n/tmp has been mounted without options "noexec"	4	19
159	NotCompliance	There are 2 roots: ['root', 'toor']	6	19
160	NotCompliance	The password is not set up	7	19
161	Compliance	emergency.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""\nrescue.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""	8	19
162	Compliance	cron.service state is enabled	9	19
163	NotCompliance	cramfs is not disabled\nfreevxfs is not disabled\njffs2 is not disabled\nhfs is not disabled\nhfsplus is not disabled\nsquashfs is not disabled\nudf is not disabled\nvfat is not disabled	1	20
164	Compliance	/boot/grub2/grub.cfg root:root 600	2	20
165	NotCompliance	/home has been mounted on /dev/sda2\n/tmp has been mounted on /dev/sda2\n/var/log has been mounted on /dev/sda2\n/var/tmp has been mounted on /dev/sda2\n/var has not been mounted on separate partition\n/var/log/audit has not been mounted on separate partition	3	20
166	NotCompliance	/var/tmp has been mounted without options "nodev,nosuid,noexec"\n/home has been mounted without options "nodev"\n/dev/shm has been mounted without options "noexec"\n/tmp has been mounted without options "nodev,nosuid,noexec"	4	20
167	Compliance	There is only one root	6	20
168	NotCompliance	The password is not set up	7	20
169	Compliance	emergency.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --job-mode=fail --no-block default""\nrescue.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --job-mode=fail --no-block default""	8	20
170	Compliance	cron.service state is enabled	9	20
139	NotCompliance	cramfs is not disabled\nfreevxfs is not disabled\njffs2 is not disabled\nhfs is not disabled\nhfsplus is not disabled\nsquashfs is not disabled\nudf is not disabled\nvfat is not disabled	1	17
140	NotCompliance	/boot/grub/grub.cfg root:root 444	2	17
141	NotCompliance	/tmp has been mounted on tmpfs\n/home has not been mounted on separate partition\n/var has not been mounted on separate partition\n/var/log has not been mounted on separate partition\n/var/log/audit has not been mounted on separate partition\n/var/tmp has not been mounted on separate partition	3	17
142	NotCompliance	/var/tmp has not been mounted on separated partition\n/home has not been mounted on separated partition\n/dev/shm has been mounted without options "noexec"\n/tmp has been mounted without options "noexec"	4	17
143	NotCompliance	There are 2 roots: ['root', 'toor']	6	17
144	NotCompliance	The password is not set up	7	17
145	Compliance	emergency.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""\nrescue.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""	8	17
146	Compliance	cron.service state is enabled	9	17
147	NotCompliance	cramfs is not disabled\nfreevxfs is not disabled\njffs2 is not disabled\nhfs is not disabled\nhfsplus is not disabled\nsquashfs is not disabled\nudf is not disabled\nvfat is not disabled	1	18
148	Compliance	/boot/grub2/grub.cfg root:root 600	2	18
149	NotCompliance	/home has been mounted on /dev/sda2\n/tmp has been mounted on /dev/sda2\n/var/log has been mounted on /dev/sda2\n/var/tmp has been mounted on /dev/sda2\n/var has not been mounted on separate partition\n/var/log/audit has not been mounted on separate partition	3	18
150	NotCompliance	/var/tmp has been mounted without options "nodev,nosuid,noexec"\n/home has been mounted without options "nodev"\n/dev/shm has been mounted without options "noexec"\n/tmp has been mounted without options "nodev,nosuid,noexec"	4	18
151	Compliance	There is only one root	6	18
152	NotCompliance	The password is not set up	7	18
153	Compliance	emergency.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --job-mode=fail --no-block default""\nrescue.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --job-mode=fail --no-block default""	8	18
154	Compliance	cron.service state is enabled	9	18
171	NotCompliance	cramfs is not disabled\nfreevxfs is not disabled\njffs2 is not disabled\nhfs is not disabled\nhfsplus is not disabled\nsquashfs is not disabled\nudf is not disabled\nvfat is not disabled	1	21
172	NotCompliance	/boot/grub/grub.cfg root:root 444	2	21
173	NotCompliance	/tmp has been mounted on tmpfs\n/home has not been mounted on separate partition\n/var has not been mounted on separate partition\n/var/log has not been mounted on separate partition\n/var/log/audit has not been mounted on separate partition\n/var/tmp has not been mounted on separate partition	3	21
174	NotCompliance	/var/tmp has not been mounted on separated partition\n/home has not been mounted on separated partition\n/dev/shm has been mounted without options "noexec"\n/tmp has been mounted without options "noexec"	4	21
175	NotCompliance	There are 2 roots: ['root', 'toor']	6	21
176	NotCompliance	The password is not set up	7	21
177	Compliance	emergency.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""\nrescue.service has right value = "-/bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default""	8	21
178	Compliance	cron.service state is enabled	9	21
\.


--
-- Data for Name: host_result; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.host_result (id, task_id, config, hostname) FROM stdin;
15	90	{"ssh": {"password": "P@ssw0rd", "port": "22", "username": "vmuser"}, "unix": {"privilege_escalation": "SudoLogon", "root_password": ""}}	192.168.56.10
16	90	{"ssh": {"password": "P@ssw0rd", "port": "22", "username": "vmuser"}, "unix": {"privilege_escalation": "SudoLogon", "root_password": ""}}	192.168.56.32
17	91	{"ssh": {"password": "P@ssw0rd", "port": "22", "username": "vmuser"}, "unix": {"privilege_escalation": "SudoLogon", "root_password": ""}}	192.168.56.10
18	91	{"ssh": {"password": "P@ssw0rd", "port": "22", "username": "vmuser"}, "unix": {"privilege_escalation": "SudoLogon", "root_password": ""}}	192.168.56.32
19	92	{"ssh": {"password": "P@ssw0rd", "port": "22", "username": "vmuser"}, "unix": {"privilege_escalation": "SudoLogon", "root_password": ""}}	192.168.56.10
20	92	{"ssh": {"password": "P@ssw0rd", "port": "22", "username": "vmuser"}, "unix": {"privilege_escalation": "SudoLogon", "root_password": ""}}	192.168.56.32
21	93	{"ssh": {"password": "P@ssw0rd", "port": "22", "username": "vmuser"}, "unix": {"privilege_escalation": "SudoLogon", "root_password": ""}}	192.168.56.10
\.


--
-- Data for Name: profile_setting; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profile_setting (id, transport, setting, value, profile_id) FROM stdin;
1	ssh	port	22	1
2	ssh	credential	3	1
4	unix	root_password		1
5	ssh	port	22	2
6	ssh	credential	7	2
7	unix	privilege_escalation	SudoLogon	2
8	unix	root_password		2
3	unix	privilege_escalation	SudoLogon	1
\.


--
-- Data for Name: scan_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scan_profile (id, name, owner_id) FROM stdin;
1	111	1
2	test	1
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task (id, name, owner_id, status, uid) FROM stdin;
10	15	1	Idle	\N
11	16	1	Idle	\N
12	17	1	Idle	\N
15	20	1	Idle	\N
13	18	1	Idle	\N
14	19	1	Idle	\N
3	1	1	Idle	\N
25	30	1	Idle	613d2d81-5b2c-4a07-b9ff-cc38b52ea02a
37	42	1	Idle	18b561e6-8246-4098-a6a1-a2564ac9621a
36	41	1	Idle	36b598e8-3b1c-4b5d-b499-fe1bd936d2de
4	2	1	Idle	\N
18	23	1	Idle	\N
19	24	1	Idle	\N
1	111	1	Idle	\N
5	3	1	Idle	\N
6	4	1	Idle	\N
7	5	1	Idle	\N
8	6	1	Idle	\N
9	7	1	Idle	\N
22	27	1	Idle	\N
16	21	1	Idle	\N
17	22	1	Idle	\N
23	28	1	Idle	\N
24	29	1	Idle	\N
26	31	1	Idle	\N
27	32	1	Idle	\N
28	33	1	Idle	\N
29	34	1	Idle	\N
30	35	1	Idle	\N
31	36	1	Idle	\N
32	37	1	Idle	\N
33	38	1	Idle	\N
34	39	1	Idle	\N
35	40	1	Idle	\N
38	43	1	Idle	\N
39	44	1	Idle	\N
40	45	1	Idle	\N
41	46	1	Idle	\N
42	47	1	Idle	\N
43	48	1	Idle	\N
44	49	1	Idle	\N
\.


--
-- Data for Name: task_result; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_result (id, task_id, started, finished, owner_id) FROM stdin;
90	1	2018-08-18 14:37:44.897448	2018-08-18 14:37:46.545115	1
91	1	2018-08-18 14:37:58.920962	2018-08-18 14:38:00.450114	1
92	1	2018-08-18 14:38:36.978006	2018-08-18 14:38:38.751627	1
93	1	2018-08-18 19:11:43.409171	2018-08-18 19:11:44.42623	1
\.


--
-- Data for Name: task_setting; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_setting (id, hostname, profile_id, task_id) FROM stdin;
4	192.168.56.10	1	1
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, email, password_hash) FROM stdin;
1	vmuser	vmuser@yahoo.com	pbkdf2:sha256:50000$5V8n80uZ$7a6af995a9f360125216fcd9002b43ddb844d11ac0ec86a1b6b30363b08eb9d7
2	test	teste@mail.ru	pbkdf2:sha256:50000$m8XbDYeT$cee07c9282fa2454a4efb8b23fa3d08e0af0de93e1e442cb0f7039935c00b421
\.


--
-- Name: account_credential_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_credential_id_seq', 7, true);


--
-- Name: control_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.control_id_seq', 22, true);


--
-- Name: control_result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.control_result_id_seq', 178, true);


--
-- Name: host_result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.host_result_id_seq', 21, true);


--
-- Name: profile_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profile_setting_id_seq', 8, true);


--
-- Name: scan_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.scan_profile_id_seq', 2, true);


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_id_seq', 44, true);


--
-- Name: task_id_sequence; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_id_sequence', 246, true);


--
-- Name: task_result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_result_id_seq', 93, true);


--
-- Name: task_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_setting_id_seq', 5, true);


--
-- Name: taskset_id_sequence; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taskset_id_sequence', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 2, true);


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

