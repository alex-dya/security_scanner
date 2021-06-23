CREATE TYPE taskstatus AS ENUM ('Idle', 'Wait', 'Running');
CREATE TYPE controlstatus AS ENUM ('NotChecked', 'Compliance', 'NotCompliance', 'NotApplicable', 'Error');
CREATE TABLE users (
	id SERIAL NOT NULL, 
	username VARCHAR(64), 
	email VARCHAR(128), 
	password_hash VARCHAR(128), 
	language VARCHAR(2), 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE TABLE control (
	id SERIAL NOT NULL, 
	number INTEGER, 
	language VARCHAR(4) DEFAULT 'en', 
	name VARCHAR(128) NOT NULL, 
	description VARCHAR(2048) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_control_language ON control (language);
CREATE INDEX ix_control_number ON control (number);
CREATE TABLE account_credential (
	id SERIAL NOT NULL, 
	name VARCHAR(64), 
	username VARCHAR(64), 
	password VARCHAR(128), 
	owner_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT account_cred_uniq UNIQUE (name, owner_id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);
CREATE INDEX ix_account_credential_name ON account_credential (name);
CREATE INDEX ix_account_credential_owner_id ON account_credential (owner_id);
CREATE INDEX ix_account_credential_username ON account_credential (username);
CREATE TABLE scan_profile (
	id SERIAL NOT NULL, 
	name VARCHAR, 
	owner_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT scan_profile_uniq UNIQUE (name, owner_id), 
	CONSTRAINT scan_profile_fk FOREIGN KEY(owner_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE TABLE task (
	id SERIAL NOT NULL, 
	name VARCHAR(64), 
	status taskstatus DEFAULT 'Idle' NOT NULL, 
	uid VARCHAR(128), 
	owner_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT task_uniq UNIQUE (name, owner_id), 
	CONSTRAINT task_fk FOREIGN KEY(owner_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE INDEX ix_task_name ON task (name);
CREATE TABLE profile_setting (
	id SERIAL NOT NULL, 
	transport VARCHAR NOT NULL, 
	setting VARCHAR NOT NULL, 
	value VARCHAR NOT NULL, 
	profile_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT profile_setting_uniq UNIQUE (transport, setting, profile_id), 
	CONSTRAINT profile_setting_fk FOREIGN KEY(profile_id) REFERENCES scan_profile (id) ON DELETE CASCADE
);
CREATE INDEX ix_profile_setting_profile_id ON profile_setting (profile_id);
CREATE TABLE task_setting (
	id SERIAL NOT NULL, 
	hostname VARCHAR(128), 
	profile_id INTEGER NOT NULL, 
	task_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT task_setting_uniq UNIQUE (hostname, profile_id, task_id), 
	CONSTRAINT task_setting_fk FOREIGN KEY(profile_id) REFERENCES scan_profile (id) ON DELETE SET NULL, 
	CONSTRAINT task_setting_fk2 FOREIGN KEY(task_id) REFERENCES task (id) ON DELETE CASCADE
);
CREATE TABLE task_result (
	id SERIAL NOT NULL, 
	task_id INTEGER NOT NULL, 
	owner_id INTEGER NOT NULL, 
	started TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
	finished TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	CONSTRAINT task_result_fk FOREIGN KEY(task_id) REFERENCES task (id) ON DELETE SET NULL, 
	CONSTRAINT task_fk FOREIGN KEY(owner_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE TABLE host_result (
	id SERIAL NOT NULL, 
	task_id INTEGER NOT NULL, 
	config VARCHAR, 
	hostname VARCHAR, 
	PRIMARY KEY (id), 
	CONSTRAINT host_result_fk FOREIGN KEY(task_id) REFERENCES task_result (id) ON DELETE CASCADE
);
CREATE TABLE control_result (
	id SERIAL NOT NULL, 
	host_result_id INTEGER NOT NULL, 
	control_number INTEGER NOT NULL, 
	status controlstatus NOT NULL, 
	result VARCHAR, 
	PRIMARY KEY (id), 
	CONSTRAINT control_result_fk FOREIGN KEY(host_result_id) REFERENCES host_result (id) ON DELETE CASCADE
);
INSERT INTO control (id, number, language, name, description) VALUES (1, 1, 'en', 'Ensure mounting of forbidden filesystems is disabled', 'Removing support for unneeded filesystem types reduces the local attack surface of the server.');
INSERT INTO control (id, number, language, name, description) VALUES (2, 1, 'ru', 'Убедитесь, что монтирование запрещенных файловых систем отключено', 'Отключите поддержку ненужных типов файловых систем для того чтобы уменьшить площадь атаки на сервер.');
INSERT INTO control (id, number, language, name, description) VALUES (3, 2, 'en', 'Ensure permissions on bootloader config are configured', 'The grub configuration file contains information on boot settings and passwords for unlocking boot options. The grub configuration is usually grub.conf, grub.cfg, or menu.lst stored in either /boot/grub or /boot/grub2. It is commonly symlinked as /etc/grub.conf as well. Setting the permissions to read and write for root only prevents non-root users from seeing the boot parameters or changing them. Non-root users who read the boot parameters may be able to identify weaknesses in security upon boot and be able to exploit them.');
INSERT INTO control (id, number, language, name, description) VALUES (4, 2, 'ru', 'Удостоверьтесь, что разрешения на конфиг загрузчика настроены корректно', 'Конфигурационный файл содержит информацию о настройках загрузки и паролях для разблокировки опций загрузки. Настройки grub - grub.conf, grub.cfg, или menu.lst - обычно храняться либо в каталоге /boot/grub либо /boot/grub2. В основном, он является символической ссылкой на /etc/grub.conf. Настройте права доступа на чтение и запись только пользователю root, для предотвращения просмотра параметров загрузки или их изменения другими пользователями. Не-root пользователи, кто может читать параметры загрузки, могут быть способны обнаружить слабые места в защите во время загрузки системы и проэксплуатировать их');
INSERT INTO control (id, number, language, name, description) VALUES (5, 3, 'en', 'Ensure separate partition exists for /var', 'The /var directory is used by daemons and other system services to temporarily store dynamic data. Some directories created by these processes may be world-writable.');
INSERT INTO control (id, number, language, name, description) VALUES (6, 3, 'ru', 'Удостоверьтесь, что существует отдельный раздел диска для /var', 'Директория /var обычно используется демонами и другими службами для временного хранения изменяемых данных. Некоторые директории созданные этими процессами могут иметь права на запись для всех пользователей.');
INSERT INTO control (id, number, language, name, description) VALUES (7, 4, 'en', 'Ensure nodev option set on /tmp partition', 'The nodev mount option specifies that the filesystem cannot contain special devices.');
INSERT INTO control (id, number, language, name, description) VALUES (8, 4, 'ru', 'Опция nodev должна быть установлена на мониторивание раздела /tmp', 'Опция монтирования nodev указывает, что эта файловая система не может содержать специальных устройств');
INSERT INTO control (id, number, language, name, description) VALUES (9, 6, 'en', 'Ensure root is the only UID 0 account', 'Any account with UID 0 has superuser privileges on the system. This access must be limited to only the default root account and only from the system console. Administrative access must be through an unprivileged account using an approved mechanism. Ensure access to the su command is restricted.');
INSERT INTO control (id, number, language, name, description) VALUES (10, 6, 'ru', 'Пользователь root должен быть единственным пользователем с UID 0', 'Любой аккаунт с UID 0 имеет права суперпользователя на системе. Этот доступ должен быть ограничен единственным пользователем root в системе и только из системной консоли. Административный доступ для непривилегированных аккаунтов должен осуществляться только через надежные механизмы поднятия привелегий. Доступ для выполнения команды su должен быть ограничен');
INSERT INTO control (id, number, language, name, description) VALUES (11, 7, 'en', 'Ensure bootloader password is set', 'Setting the boot loader password will require that anyone rebooting the system must enter a password before being able to set command line boot parameters. Requiring a boot password upon execution of the boot loader will prevent an unauthorized user from entering boot parameters or changing the boot partition. This prevents users from weakening security (e.g. turning off SELinux at boot time).');
INSERT INTO control (id, number, language, name, description) VALUES (12, 7, 'ru', 'Установите пароль на загрузчик системы', 'Установка пароля на загрузчик системы требуется, чтобы любому пользователю, перезагружающему систему, необходимо было ввести пароль перед тем как получить доступ к настройкам параметров загрузочной командной строки. Требование пароля на загрузчике системы запрещает неавторизованному пользователю изменять параметры загрузки или загрузочный раздел. Это предотвратит ослабление защиты пользователем (например, отключение системы защиты SELinux во время загрузки системы).');
INSERT INTO control (id, number, language, name, description) VALUES (13, 8, 'en', 'Ensure authentication required for single user mode', 'Single user mode is used for recovery when the system detects an issue during boot or by manual selection from the bootloader. Requiring authentication in single user mode prevents an unauthorized user from rebooting the system into single user to gain root privileges without credentials.');
INSERT INTO control (id, number, language, name, description) VALUES (14, 8, 'ru', 'Включите аутентификацию для режима single user', 'Режим single user используется для восстановления, когда системы обнаружила неполадки во время загрузки, или при выборе этого режима в меню загрузчика. Требование аутентификации в режиме single user предотвращает неавторизованным пользователям доступ к режиму single user для получения привилегия root без запроса пароля.');
INSERT INTO control (id, number, language, name, description) VALUES (15, 9, 'en', 'Ensure cron daemon is enabled', 'The cron daemon is used to execute batch jobs on the system. While there may not be user jobs that need to be run on the system, the system does have maintenance jobs that may include security monitoring that have to run, and cron is used to execute them.');
INSERT INTO control (id, number, language, name, description) VALUES (16, 9, 'ru', 'Демон cron должен быть включен.', 'Демон cron используется для выполнения набора задач на системе по расписанию. Даже если нет пользовательских задач, которые необходимо выполнять на системе, самой системе необходимо поддерживать задачи, которые могут включать мониторинг безопасности. И cron используется для их выполнения.');
INSERT INTO control (id, number, language, name, description) VALUES (17, 10, 'en', 'Ensure system accounts are secured.', 'There are a number of accounts provided with most distributions that are used to manage applications and are not intended to provide an interactive shell.');
INSERT INTO control (id, number, language, name, description) VALUES (18, 10, 'ru', 'Убедитесь, что системные учетные записи защищены.', 'В большинстве дистрибутивов имеется ряд учетных записей, которые используются для управления приложениями и не предназначены для предоставления интерактивной оболочки.');
