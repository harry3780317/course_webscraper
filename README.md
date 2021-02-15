# MountainMadness2021
MountainMadness2021 hackathon project
Contributors: moleratirl (me), muvda

A webscraper that integrates sfu course outline and rate my prof ratings into a single search on cli. Uses selenium and beautifulsoup.


git pull project with chromedriver.exe in same dir as smallscrape.py

run smallscrape.py and input in the format ---> year/term/dept/coursenum (i.e 2019/spring/cmpt/300)

output:

```yaml
{
   [
    {
        "course-times": [
            "COURSE TIMES + LOCATION:\nMo, We, Fr 1:30 PM \u2013 2:20 PM\nSSCB 9201, Burnaby"
        ],
        "exam-times": [
            "EXAM TIMES + LOCATION:\nApr 15, 2019\n12:00 PM \u2013 3:00 PM\nSSCB 9201, Burnaby"
        ],
        "instructors": [
            {
                "name": "Janice Regan",
                "score": "2.5",
                "take_again": "20%",
                "difficulty": "4",
                "tags": [
                    "Tough grader",
                    "Lots of homework",
                    "Get ready to read",
                    "Lecture heavy",
                    "Test heavy"
                ],
                "url": "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=246300",
                "email": "jregan@sfu.ca",
                "phone": "1 778 782-6911"
            }
        ],
        "prereq": [
            "PREREQUISITES:\nCMPT 225 and (MACM 101 or (ENSC 251 and ENSC 252))."
        ],
        "calenderdesc": "This course aims to give the student an understanding of what a modern operating system is, and the services it provides. It also discusses some basic issues in operating systems and provides solutions. Topics include multiprogramming, process management, memory management, and file systems.",
        "coursedet": "Operating systems, being a fundamental part of any computer system, provide an environment in which users can execute their programs on the underlying computer hardware. This course explores the field of operating systems with an emphasis on basic operating systems concepts and design principles. We will cover fundamentals of operating systems such as processes, scheduling, synchronization, multiprogramming, memory management, file system and protection. Additionally, we will briefly touch on a few advanced topics like virtual machines. Students will also get a hands-on experience via multiple programming exercises. This is a programming-heavy course and basic knowledge of C and C++ programming and the UNIX environment is assumed.",
        "topics": [
            "Operating System Structures",
            "Processes and Threads",
            "CPU Scheduling and Process Coordination",
            "Memory Management",
            "File Systems",
            "I/O Systems",
            "Protection"
        ],
        "grading": [],
        "notes": [
            "",
            "assignments 25%, quizzes 35%, final 40% details will be discussed in the first class, and posted on the class website",
            "Students must attain an overall passing grade on the weighted average of exams in the course in order to obtain a clear pass (C- or better).",
            ""
        ],
        "materials": "Modern Operating Systems\nAndrew S. Tanenbaum\nPrentice Hall\n2015\n9780133591620",
        "requiredreading": ""
    },
    {
        "course-times": [
            "COURSE TIMES + LOCATION:\nMo, Fr 10:30 AM \u2013 11:20 AM\nAQ 3149, Burnaby\nWe 10:30 AM \u2013 11:20 AM\nAQ 3154, Burnaby"
        ],
        "exam-times": [
            "EXAM TIMES + LOCATION:\nApr 23, 2019\n12:00 PM \u2013 3:00 PM\nAQ 3182, Burnaby"
        ],
        "instructors": [
            {
                "name": "Tianzheng Wang",
                "score": "4",
                "take_again": "80%",
                "difficulty": "3.7",
                "tags": [
                    "Lots of homework",
                    "Gives good feedback",
                    "Respected",
                    "Accessible outside class",
                    "Group projects"
                ],
                "url": "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2449196",
                "email": "tzwang@sfu.ca",
                "phone": ""
            }
        ],
        "prereq": [
            "PREREQUISITES:\nCMPT 225 and (MACM 101 or (ENSC 251 and ENSC 252))."
        ],
        "calenderdesc": "This course aims to give the student an understanding of what a modern operating system is, and the services it provides. It also discusses some basic issues in operating systems and provides solutions. Topics include multiprogramming, process management, memory management, and file systems.",
        "coursedet": "Operating systems, being a fundamental part of any computer system, provide an environment in which users can execute their programs on the underlying computer hardware. This course explores the field of operating systems with an emphasis on basic operating systems concepts and design principles. We will cover fundamentals of operating systems such as processes, scheduling, synchronization, multiprogramming, memory management, file system and protection. Additionally, we will briefly touch on a few advanced topics like virtual machines. Students will also get a hands-on experience via multiple programming exercises. This is a programming-heavy course and basic knowledge of C and C++ programming and the UNIX environment is assumed.",
        "topics": [
            "Operating System Structures",
            "Processes and Threads",
            "CPU Scheduling and Process Coordination",
            "Memory Management",
            "File Systems",
            "I/O Systems",
            "Protection"
        ],
        "grading": [],
        "notes": [
            "There will be five/six programming assignments, one/two midterms, and one final exam.\nDetails about grading will be discussed in the first week of class"
        ],
        "materials": "Modern Operating Systems\nAndrew S. Tanenbaum\nPrentice Hall\n2014\n9780133591620",
        "requiredreading": "Operating System Concepts , 9th Edition\nAbraham Silberschatz, Peter Baer Galvin, Greg Gagne\nJ. Wiley & Sons\n2012\nISBN: 9781118063330"
    }
]
}
