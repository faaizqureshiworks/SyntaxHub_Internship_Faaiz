import json
import os

class Student:
    """Represents an individual student record."""
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        """Converts student object properties to a dictionary for JSON saving."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }

class StudentManager:
    """Manages the student records and file operations."""
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = {}  # Format: {student_id: Student Object}
        self.load_data()

    def load_data(self):
        """Loads student data from the JSON file on startup."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for key, val in data.items():
                        self.students[key] = Student(val['student_id'], val['name'], val['grade'])
            except json.JSONDecodeError:
                print("[System Info] Data file was empty or corrupted. Starting fresh.")

    def save_data(self):
        """Saves current student data back to the JSON file."""
        with open(self.filename, 'w') as file:
            # Convert all Student objects into standard dictionaries before saving
            json_ready_data = {sid: obj.to_dict() for sid, obj in self.students.items()}
            json.dump(json_ready_data, file, indent=4)

    def add_student(self, student_id, name, grade):
        """Adds a new student with validation for unique ID."""
        if student_id in self.students:
            print(f"\n❌ Error: A student with ID '{student_id}' already exists!")
            return False
        
        self.students[student_id] = Student(student_id, name, grade)
        self.save_data()
        print(f"\n✅ Student '{name}' added successfully!")
        return True

    def view_students(self):
        """Displays all student records in a clean table layout."""
        if not self.students:
            print("\n📂 No student records found.")
            return

        print("\n" + "="*45)
        print(f"{'ID':<10} | {'Name':<20} | {'Grade':<10}")
        print("="*45)
        for sid, student in self.students.items():
            print(f"{student.student_id:<10} | {student.name:<20} | {student.grade:<10}")
        print("="*45)

    def update_student(self, student_id, new_name, new_grade):
        """Updates name and grade for an existing student ID."""
        if student_id not in self.students:
            print(f"\n❌ Error: Student ID '{student_id}' not found.")
            return False

        if new_name.strip():
            self.students[student_id].name = new_name
        if new_grade.strip():
            self.students[student_id].grade = new_grade
            
        self.save_data()
        print(f"\n🔄 Student ID '{student_id}' updated successfully!")
        return True

    def delete_student(self, student_id):
        """Deletes a student record by ID."""
        if student_id in self.students:
            deleted_name = self.students[student_id].name
            del self.students[student_id]
            self.save_data()
            print(f"\n🗑️ Student '{deleted_name}' removed successfully.")
            return True
        else:
            print(f"\n❌ Error: Student ID '{student_id}' not found.")
            return False

def main():
    manager = StudentManager()

    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            sid = input("Enter Student ID: ").strip()
            if not sid:
                print("❌ ID cannot be empty.")
                continue
            name = input("Enter Student Name: ").strip()
            grade = input("Enter Student Grade: ").strip()
            manager.add_student(sid, name, grade)

        elif choice == "2":
            manager.view_students()

        elif choice == "3":
            sid = input("Enter Student ID to update: ").strip()
            print("Leave blank if you do not want to change a specific value.")
            name = input("Enter New Name: ").strip()
            grade = input("Enter New Grade: ").strip()
            manager.update_student(sid, name, grade)

        elif choice == "4":
            sid = input("Enter Student ID to delete: ").strip()
            manager.delete_student(sid)

        elif choice == "5":
            print("\n👋 Exiting system. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()