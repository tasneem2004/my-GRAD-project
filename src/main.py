from adaptive_logic import AdaptiveTutor, update_student_csv, export_student_report
from quiz_reader import QuizReader
import json

def main():
    # Initialize components
    student_id = "student_001"  # In real app, this would come from user login
    tutor = AdaptiveTutor(student_id)
    quiz_reader = QuizReader()
    
    print(f"Welcome, {student_id}!")
    print(f"Current difficulty level: {tutor.difficulty_level}")
    print(f"Your current accuracy: {tutor.performance_history['average_score']:.1%}")
    
    # Get recommended questions
    questions = quiz_reader.get_questions_by_difficulty(
        tutor.difficulty_level, 
        limit=3
    )
    
    # Simulate answering questions
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question['question']}")
        print(f"Options: {question['options']}")
        print(f"Topic: {question['topic']}")
        
        # Simulate user answer (in real app, get from UI)
        # For demo, randomly determine if answer is correct
        import random
        user_correct = random.choice([True, False])
        time_spent = random.randint(10, 60)  # seconds
        
        if user_correct:
            print("✓ Correct!")
        else:
            print("✗ Incorrect")
        
        # Update adaptive system
        new_difficulty = tutor.update_performance(
            question, 
            user_correct, 
            time_spent, 
            question['topic']
        )
        
        print(f"New difficulty level: {new_difficulty}")
    
    # Update CSV record
    update_student_csv(student_id, tutor.performance_history)
    
    # Show recommendations
    print("\n--- Learning Recommendations ---")
    for rec in tutor.get_recommendations():
        print(f"• {rec}")
    
    # Generate report
    report = export_student_report(student_id)
    if report:
        print(f"\nReport generated: data/student_{student_id}_report.json")

if __name__ == "__main__":
    main()
