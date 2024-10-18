import asyncio
import aiohttp
import pandas as pd
from typing import List, Dict

class StudentAPI:
    """Class to interact with the students API asynchronously"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    async def _fetch(self, endpoint: str) -> List[Dict]:
        """Fetch data from the given endpoint asynchronously"""
        url = f"{self.base_url}/{endpoint}"
        async with self.session.get(url) as response:
            return await response.json()

    async def fetch_enrolled_students(self) -> List[Dict]:
        """Fetch list of students enrolled in courses"""
        return await self._fetch("students/enrolled")

    async def fetch_not_enrolled_students(self) -> List[Dict]:
        """Fetch list of students not enrolled in any courses"""
        return await self._fetch("students/not-enrolled")

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

class StudentAnalyzer:
    """Class to analyze the student data"""
    
    def __init__(self, enrolled_students: List[Dict], not_enrolled_students: List[Dict]):
        self.enrolled_students = enrolled_students
        self.not_enrolled_students = not_enrolled_students
    
    def analyze_enrollment_statistics(self):
        """Analyze and print statistics of enrolled and not enrolled students"""
        enrolled_df = pd.DataFrame(self.enrolled_students)
        not_enrolled_df = pd.DataFrame(self.not_enrolled_students)

        print(f"Total enrolled students: {len(enrolled_df)}")
        print(f"Total not enrolled students: {len(not_enrolled_df)}")
    
    def export_to_csv(self):
        """Export the data to CSV files"""
        enrolled_df = pd.DataFrame(self.enrolled_students)
        not_enrolled_df = pd.DataFrame(self.not_enrolled_students)
        
        enrolled_df.to_csv("enrolled_students.csv", index=False)
        not_enrolled_df.to_csv("not_enrolled_students.csv", index=False)

async def main():
    base_url = 'http://localhost:3000'

    # Fetch data asynchronously
    async with StudentAPI(base_url) as api:
        enrolled_students = await api.fetch_enrolled_students()
        not_enrolled_students = await api.fetch_not_enrolled_students()

    # Analyze the data
    analyzer = StudentAnalyzer(enrolled_students, not_enrolled_students)
    analyzer.analyze_enrollment_statistics()
    analyzer.export_to_csv()

if __name__ == "__main__":
    asyncio.run(main())
