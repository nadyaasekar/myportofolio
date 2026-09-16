import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # Ganti 'your_project' dengan nama folder project-mu
django.setup()

from main.models import Experience
from datetime import date

experiences = [
    {
        "title": "Staff of Human Resources Division (DDP 0)",
        "description": "Assisted in human resource management, member engagement, and team coordination for DDP 0. Monitored member performance, facilitated internal communication, and supported overall group dynamics.",
        "category": "Volunteer",
        "thumbnail": "",
        "started_at": date(2026, 4, 1),
        "ended_at": None
    },
    {
        "title": "Mentor Open House Fasilkom UI",
        "description": "Guided high school students in exploring Faculty of Computer Science (Fasilkom UI), providing insights into campus life, academic culture, and computer science study programs.",
        "category": "Volunteer",
        "thumbnail": "",
        "started_at": date(2025, 11, 1),
        "ended_at": date(2025, 11, 30)
    },
    {
        "title": "Partnership Staff of Business IT Case Competition",
        "description": "COMPFEST. Managed corporate partnerships, established external outreach, and maintained relationships with media partners and sponsors for the Business IT Case Competition.",
        "category": "Volunteer",
        "thumbnail": "",
        "started_at": date(2026, 4, 1),
        "ended_at": None
    },
    {
        "title": "Partnership Staff",
        "description": "BETIS Fasilkom UI. Handled sponsorship proposals, built strategic relationships with potential partners, and supported external collaboration initiatives.",
        "category": "Volunteer",
        "thumbnail": "",
        "started_at": date(2026, 2, 1),
        "ended_at": None
    },
    {
        "title": "Coordinator of the Health and Humanity Division",
        "description": "Student Representative Council, Labschool Kebayoran. Served in a legislative student organization responsible for evaluating and overseeing the Student Council's performance, health activities, and organizational standards.",
        "category": "Part-Time",
        "thumbnail": "",
        "started_at": date(2023, 8, 1),
        "ended_at": date(2024, 8, 31)
    },
    {
        "title": "Coordinator of Paramedics",
        "description": "SKYWALK. Prepared first aid protocols, coordinated medical personnel, and maintained responsiveness in handling sick participants or spectators during events.",
        "category": "Volunteer",
        "thumbnail": "",
        "started_at": date(2023, 6, 1),
        "ended_at": date(2024, 6, 30)
    },
    {
        "title": "Executive Supervisor for Troops For Humanity",
        "description": "Evaluated program effectiveness, identified areas for improvement, and provided feedback to organizers and volunteers. Guided and supervised volunteers, fostering teamwork and responsibility.",
        "category": "Volunteer",
        "thumbnail": "",
        "started_at": date(2023, 8, 1),
        "ended_at": date(2024, 5, 31)
    },
    {
        "title": "Executive Supervisor for SKYCARE",
        "description": "Supervised social service and community outreach initiatives, including visits to orphanages. Oversee program implementation, volunteer coordination, and donation distribution.",
        "category": "Volunteer",
        "thumbnail": "",
        "started_at": date(2023, 8, 1),
        "ended_at": date(2024, 6, 30)
    },
    {
        "title": "Secretary of Student Council",
        "description": "SMP An-Nisaa. Managed documentation, agendas, and communication for council activities. Assisted in organizing school-wide programs and maintaining administrative records.",
        "category": "Part-Time",
        "thumbnail": "",
        "started_at": date(2021, 1, 1),
        "ended_at": date(2021, 1, 31)
    }
]

for exp in experiences:
    Experience.objects.create(**exp)

print("Berhasil memasukkan semua data experience!")