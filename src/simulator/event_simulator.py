from datetime import datetime, timedelta
import random
import uuid


class SecurityEventSimulator:

    def __init__(
        self,
        num_users=5000,
        num_devices=6000,
        num_applications=100,
        seed=42
    ):
        self.num_users = num_users
        self.num_devices = num_devices
        self.num_applications = num_applications
        self.seed = seed

        random.seed(self.seed)

        self.first_names = [
            "Aarav", "Aditi", "Arjun", "Ananya", "Kabir",
            "Meera", "Rohan", "Sneha", "Rahul", "Priya",
            "Vikram", "Neha", "Karan", "Pooja", "Amit",
            "Riya", "Nikhil", "Isha", "Varun", "Kavya"
        ]

        self.last_names = [
            "Sharma", "Patel", "Mehta", "Shah", "Gupta",
            "Joshi", "Verma", "Iyer", "Reddy", "Kapoor",
            "Mishra", "Desai", "Nair", "Malhotra", "Bansal"
        ]

        self.departments = [
            "Finance",
            "HR",
            "Engineering",
            "IT",
            "Sales",
            "Marketing",
            "Operations",
            "Legal"
        ]

        self.roles = [
            "Analyst",
            "Senior Analyst",
            "Manager",
            "Senior Manager",
            "Developer",
            "Administrator"
        ]

        self.locations = [
            ("Pune", "India"),
            ("Mumbai", "India"),
            ("Bengaluru", "India"),
            ("Delhi", "India"),
            ("Hyderabad", "India"),
            ("Chennai", "India"),
            ("London", "UK"),
            ("Singapore", "Singapore"),
            ("New York", "USA")
        ]

        self.os_types = [
            "Windows",
            "macOS",
            "Linux",
            "Android",
            "iOS"
        ]

        self.device_types = [
            "Laptop",
            "Desktop",
            "Mobile",
            "Tablet"
        ]

        self.auth_methods = [
            "PASSWORD",
            "MFA",
            "SSO",
            "VPN"
        ]

        self.auth_statuses = [
            "SUCCESS",
            "FAILED"
        ]

        self.access_actions = [
            "LOGIN",
            "VIEW",
            "DOWNLOAD",
            "UPLOAD",
            "UPDATE",
            "DELETE"
        ]

        self.access_statuses = [
            "SUCCESS",
            "DENIED"
        ]

        self.applications = [
            ("HR Portal", "HR", "HIGH"),
            ("Payroll Portal", "HR", "CRITICAL"),
            ("CRM", "Sales", "MEDIUM"),
            ("Jira", "Engineering", "MEDIUM"),
            ("GitHub", "Engineering", "HIGH"),
            ("AWS Console", "IT", "CRITICAL"),
            ("VPN Portal", "IT", "HIGH"),
            ("Finance Portal", "Finance", "CRITICAL"),
            ("Email", "Corporate", "MEDIUM"),
            ("Data Warehouse", "IT", "CRITICAL")
        ]

        self.users = []
        self.devices = []
        self.application_catalog = []

        self.user_devices = {}

    # --------------------------------------------------
    # USERS
    # --------------------------------------------------

    def generate_users(self):

        users = []

        start_date = datetime(2018, 1, 1)
        end_date = datetime(2025, 1, 1)

        for i in range(1, self.num_users + 1):

            user_id = f"U{i:06d}"

            first_name = random.choice(
                self.first_names
            )

            last_name = random.choice(
                self.last_names
            )

            city, country = random.choice(
                self.locations
            )

            join_date = (
                start_date +
                timedelta(
                    days=random.randint(
                        0,
                        (end_date - start_date).days
                    )
                )
            ).date()

            user = {
                "user_id": user_id,
                "employee_id": f"EMP{i:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "department": random.choice(
                    self.departments
                ),
                "role": random.choice(
                    self.roles
                ),
                "city": city,
                "country": country,
                "employment_type": random.choice([
                    "FULL_TIME",
                    "CONTRACTOR"
                ]),
                "user_status": random.choice([
                    "ACTIVE",
                    "ACTIVE",
                    "ACTIVE",
                    "INACTIVE"
                ]),
                "join_date": join_date
            }

            users.append(user)

        self.users = users

        return users

    # --------------------------------------------------
    # DEVICES
    # --------------------------------------------------

    def generate_devices(self):
        if not self.users:
            raise ValueError("Users must be generated before devices.")

        if self.num_devices < self.num_users:
            raise ValueError(
                "num_devices must be greater than or equal to num_users."
            )

        devices = []

        # First: guarantee at least one device per user
        for i, user in enumerate(self.users, start=1):
            device = {
                "device_id": f"D{i:06d}",
                "user_id": user["user_id"],
                "device_type": random.choice(self.device_types),
                "os": random.choice(self.os_types),
                "hostname": f"DEVICE-{i:06d}",
                "is_managed": random.choice([
                    True, True, True, False
                ]),
                "first_seen": datetime.now() - timedelta(
                    days=random.randint(1, 1000)
                )
            }

            devices.append(device)

        # Second: distribute remaining devices randomly
        for i in range(
            self.num_users + 1,
            self.num_devices + 1
        ):
            user = random.choice(self.users)

            device = {
                "device_id": f"D{i:06d}",
                "user_id": user["user_id"],
                "device_type": random.choice(self.device_types),
                "os": random.choice(self.os_types),
                "hostname": f"DEVICE-{i:06d}",
                "is_managed": random.choice([
                    True, True, True, False
                ]),
                "first_seen": datetime.now() - timedelta(
                    days=random.randint(1, 1000)
                )
            }

            devices.append(device)

        self.devices = devices
        self._build_user_device_mapping()

        return devices

    # --------------------------------------------------
    # USER → DEVICE MAPPING
    # --------------------------------------------------

    def _build_user_device_mapping(self):

        self.user_devices = {}

        for device in self.devices:

            self.user_devices.setdefault(
                device["user_id"],
                []
            ).append(device)

    # --------------------------------------------------
    # APPLICATIONS
    # --------------------------------------------------

    def generate_applications(self):

        applications = []

        for i in range(1, self.num_applications + 1):

            base_app = random.choice(
                self.applications
            )

            application = {
                "application_id": f"APP{i:04d}",
                "application_name": (
                    f"{base_app[0]}-{i:03d}"
                ),
                "application_category": base_app[1],
                "sensitivity_level": base_app[2],
                "owner_department": random.choice(
                    self.departments
                )
            }

            applications.append(application)

        self.application_catalog = applications

        return applications

    # --------------------------------------------------
    # AUTHENTICATION EVENTS
    # --------------------------------------------------

    def generate_authentication_events(
        self,
        num_events=100000
    ):

        if not self.users:
            raise ValueError(
                "Users must be generated first."
            )

        if not self.devices:
            raise ValueError(
                "Devices must be generated first."
            )

        events = []

        start_time = datetime(2026, 9, 1)

        for _ in range(num_events):

            user = random.choice(self.users)

            available_devices = self.user_devices.get(
                user["user_id"],
                []
            )

            device = (
                random.choice(available_devices)
                if available_devices
                else random.choice(self.devices)
            )

            timestamp = start_time + timedelta(
                minutes=random.randint(
                    0,
                    30 * 24 * 60
                )
            )

            status = random.choices(
                self.auth_statuses,
                weights=[95, 5]
            )[0]

            city, country = random.choice(
                self.locations
            )

            event = {
                "event_id": str(uuid.uuid4()),
                "user_id": user["user_id"],
                "timestamp": timestamp,
                "ip_address": (
                    f"{random.randint(10, 223)}."
                    f"{random.randint(0, 255)}."
                    f"{random.randint(0, 255)}."
                    f"{random.randint(1, 254)}"
                ),
                "country": country,
                "city": city,
                "device_id": device["device_id"],
                "authentication_method": random.choice(
                    self.auth_methods
                ),
                "login_status": status,
                "failure_reason": (
                    random.choice([
                        "INVALID_PASSWORD",
                        "MFA_FAILED",
                        "ACCOUNT_LOCKED"
                    ])
                    if status == "FAILED"
                    else None
                )
            }

            events.append(event)

        return events

    # --------------------------------------------------
    # ACCESS EVENTS
    # --------------------------------------------------

    def generate_access_events(
        self,
        num_events=150000
    ):

        if not self.users:
            raise ValueError(
                "Users must be generated first."
            )

        if not self.devices:
            raise ValueError(
                "Devices must be generated first."
            )

        if not self.application_catalog:
            raise ValueError(
                "Applications must be generated first."
            )

        events = []

        start_time = datetime(2026, 9, 1)

        for _ in range(num_events):

            user = random.choice(self.users)

            available_devices = self.user_devices.get(
                user["user_id"],
                []
            )

            device = (
                random.choice(available_devices)
                if available_devices
                else random.choice(self.devices)
            )

            application = random.choice(
                self.application_catalog
            )

            timestamp = start_time + timedelta(
                minutes=random.randint(
                    0,
                    30 * 24 * 60
                )
            )

            action = random.choice(
                self.access_actions
            )

            status = random.choices(
                self.access_statuses,
                weights=[97, 3]
            )[0]

            events.append({
                "event_id": str(uuid.uuid4()),
                "user_id": user["user_id"],
                "timestamp": timestamp,
                "application_id": application[
                    "application_id"
                ],
                "resource": (
                    f"{application['application_name']}_"
                    f"RESOURCE"
                ),
                "action": action,
                "device_id": device["device_id"],
                "ip_address": (
                    f"{random.randint(10, 223)}."
                    f"{random.randint(0, 255)}."
                    f"{random.randint(0, 255)}."
                    f"{random.randint(1, 254)}"
                ),
                "access_status": status
            })

        return events

    # --------------------------------------------------
    # PRIVILEGE EVENTS
    # --------------------------------------------------

    def generate_privilege_events(
        self,
        num_events=5000
    ):

        if not self.users:
            raise ValueError(
                "Users must be generated first."
            )

        events = []

        privilege_roles = [
            "Analyst",
            "Senior Analyst",
            "Manager",
            "Administrator"
        ]

        start_time = datetime(2026, 9, 1)

        for _ in range(num_events):

            user = random.choice(self.users)

            old_role = random.choice(
                privilege_roles
            )

            new_role = random.choice(
                privilege_roles
            )

            events.append({
                "event_id": str(uuid.uuid4()),
                "user_id": user["user_id"],
                "timestamp": start_time + timedelta(
                    minutes=random.randint(
                        0,
                        30 * 24 * 60
                    )
                ),
                "old_role": old_role,
                "new_role": new_role,
                "changed_by": random.choice(
                    self.users
                )["user_id"],
                "approval_status": random.choice([
                    "APPROVED",
                    "APPROVED",
                    "PENDING",
                    "REJECTED"
                ])
            })

        return events