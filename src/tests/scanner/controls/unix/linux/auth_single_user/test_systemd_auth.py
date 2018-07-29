from scanner.types import ControlStatus
from scanner.controls.unix.linux.auth_single_user import systemd_auth
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestSystemdAuth(BaseUnixControlTest):
    origin = systemd_auth
    case_list = [
        (
            (
                '',

                '''
                #  This file is part of systemd.
                #
                #  systemd is free software; you can redistribute it and/or modify it
                #  under the terms of the GNU Lesser General Public License as published by
                #  the Free Software Foundation; either version 2.1 of the License, or
                #  (at your option) any later version.

                [Unit]
                Description=Emergency Shell
                Documentation=man:sulogin(8)
                DefaultDependencies=no
                Conflicts=shutdown.target
                Conflicts=rescue.service
                Before=shutdown.target

                [Service]
                Environment=HOME=/root
                WorkingDirectory=/root
                ExecStartPre=-/bin/plymouth quit
                ExecStartPre=-/bin/echo -e 'Welcome to emergency mode! After logging in, type "journalctl -xb" to view\\nsystem logs, "systemctl reboot" to reboot, "systemctl default" or ^D to\\ntry again to boot into default mode.'
                ExecStart=-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --fail --no-block default"
                Type=idle
                StandardInput=tty-force
                StandardOutput=inherit
                StandardError=inherit
                KillMode=process
                IgnoreSIGPIPE=no
                SendSIGHUP=yes
                ''',
                '',
                '''
                [Unit]
                Description=Rescue Shell
                Documentation=man:sulogin(8)
                DefaultDependencies=no
                Conflicts=shutdown.target
                After=sysinit.target plymouth-start.service
                Before=shutdown.target

                [Service]
                Environment=HOME=/root
                WorkingDirectory=/root
                ExecStartPre=-/bin/plymouth quit
                ExecStartPre=-/bin/echo -e 'Welcome to emergency mode! After logging in, type "journalctl -xb" to view\\nsystem logs, "systemctl reboot" to reboot, "systemctl default" or ^D to\\nboot into default mode.'
                ExecStart=-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --fail --no-block default"
                Type=idle
                StandardInput=tty-force
                StandardOutput=inherit
                StandardError=inherit
                KillMode=process
                IgnoreSIGPIPE=no
                SendSIGHUP=yes
                ''',
                '',
            ),
            ControlStatus.Compliance,
            '''
            emergency.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --fail --no-block default""
            rescue.service has right value = "-/bin/sh -c "/usr/sbin/sulogin; /usr/bin/systemctl --fail --no-block default""
            '''
        ),
        (
            (
                '',

                '''
                #  SPDX-License-Identifier: LGPL-2.1+
                #
                #  This file is part of systemd.
                #
                #  systemd is free software; you can redistribute it and/or modify it
                #  under the terms of the GNU Lesser General Public License as published by
                #  the Free Software Foundation; either version 2.1 of the License, or
                #  (at your option) any later version.

                [Unit]
                Description=Emergency Shell
                Documentation=man:sulogin(8)
                DefaultDependencies=no
                Conflicts=shutdown.target
                Conflicts=rescue.service
                Before=shutdown.target
                Before=rescue.service

                [Service]
                Environment=HOME=/root
                WorkingDirectory=-/root
                ExecStartPre=-/bin/plymouth --wait quit
                ExecStart=-/lib/systemd/systemd-sulogin-shell emergency
                Type=idle
                StandardInput=tty-force
                StandardOutput=inherit
                StandardError=inherit
                KillMode=process
                IgnoreSIGPIPE=no
                SendSIGHUP=yes
                ''',
                '',
                                '''
                #  SPDX-License-Identifier: LGPL-2.1+
                #
                #  This file is part of systemd.
                #
                #  systemd is free software; you can redistribute it and/or modify it
                #  under the terms of the GNU Lesser General Public License as published by
                #  the Free Software Foundation; either version 2.1 of the License, or
                #  (at your option) any later version.

                [Unit]
                Description=Rescue Shell
                Documentation=man:sulogin(8)
                DefaultDependencies=no
                Conflicts=shutdown.target
                After=sysinit.target plymouth-start.service
                Before=shutdown.target

                [Service]
                Environment=HOME=/root
                WorkingDirectory=-/root
                ExecStartPre=-/bin/plymouth --wait quit
                ExecStart=-/lib/systemd/systemd-sulogin-shell rescue
                Type=idle
                StandardInput=tty-force
                StandardOutput=inherit
                StandardError=inherit
                KillMode=process
                IgnoreSIGPIPE=no
                SendSIGHUP=yes
                ''',
                '',
            ),
            ControlStatus.Compliance,
            '''
            emergency.service has right value = "-/lib/systemd/systemd-sulogin-shell emergency"
            rescue.service has right value = "-/lib/systemd/systemd-sulogin-shell rescue"
            '''
        ),
        (
            (
                '',

                '''
                #  SPDX-License-Identifier: LGPL-2.1+
                #
                #  This file is part of systemd.
                #
                #  systemd is free software; you can redistribute it and/or modify it
                #  under the terms of the GNU Lesser General Public License as published by
                #  the Free Software Foundation; either version 2.1 of the License, or
                #  (at your option) any later version.

                [Unit]
                Description=Emergency Shell
                Documentation=man:sulogin(8)
                DefaultDependencies=no
                Conflicts=shutdown.target
                Conflicts=rescue.service
                Before=shutdown.target
                Before=rescue.service

                [Service]
                Environment=HOME=/root
                WorkingDirectory=-/root
                ExecStartPre=-/bin/plymouth --wait quit
                ExecStart=-/lib/systemd/systemd-login-shell emergency
                Type=idle
                StandardInput=tty-force
                StandardOutput=inherit
                StandardError=inherit
                KillMode=process
                IgnoreSIGPIPE=no
                SendSIGHUP=yes
                ''',
                '',
                                '''
                #  SPDX-License-Identifier: LGPL-2.1+
                #
                #  This file is part of systemd.
                #
                #  systemd is free software; you can redistribute it and/or modify it
                #  under the terms of the GNU Lesser General Public License as published by
                #  the Free Software Foundation; either version 2.1 of the License, or
                #  (at your option) any later version.

                [Unit]
                Description=Rescue Shell
                Documentation=man:sulogin(8)
                DefaultDependencies=no
                Conflicts=shutdown.target
                After=sysinit.target plymouth-start.service
                Before=shutdown.target

                [Service]
                Environment=HOME=/root
                WorkingDirectory=-/root
                ExecStartPre=-/bin/plymouth --wait quit
                ExecStart=-/lib/systemd/systemd-login-shell rescue
                Type=idle
                StandardInput=tty-force
                StandardOutput=inherit
                StandardError=inherit
                KillMode=process
                IgnoreSIGPIPE=no
                SendSIGHUP=yes
                ''',
                '',
            ),
            ControlStatus.NotCompliance,
            '''
            emergency.service has wrong "ExecStart" value = "-/lib/systemd/systemd-login-shell emergency"
            rescue.service has wrong "ExecStart" value = "-/lib/systemd/systemd-login-shell rescue"
            '''
        ),
        (
            (
                '',
                '',
                '',
                '',
                '',
                '',
            ),
            ControlStatus.NotCompliance,
            '''
            There are not files emergency.service, rescue.service
            '''
        ),
    ]
